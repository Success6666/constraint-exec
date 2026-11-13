"""Paired Sol evaluation of direct answers and actual coding tool use.

No semantic score is inferred from word counts. Review the saved answers against
interaction_cases.json. Workspace contracts are independently executable.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from interaction_fixtures import FIXTURES
from redaction import atomic_write_text, redact_text
from runtime_env import clean_subprocess_environment

ROOT = Path(__file__).resolve().parents[1]
MODEL = "gpt-6.1-sol"
TOOLS = [
    {"type": "function", "name": "read_file", "description": "Read app.py in the disposable workspace.",
     "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"], "additionalProperties": False}},
    {"type": "function", "name": "write_file", "description": "Replace app.py with complete source; retain unrelated user edits.",
     "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"], "additionalProperties": False}},
    {"type": "function", "name": "run_checks", "description": "Run the independent task contract tests.",
     "parameters": {"type": "object", "properties": {}, "additionalProperties": False}},
]
WORKSPACE_INSTRUCTIONS = "Tools access a disposable workspace containing app.py. Implement the requested changes there. run_checks executes independent contract tests."


def body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.split("---\n", 2)[-1].strip() if text.startswith("---\n") else text.strip()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def connection(base_url: str | None = None, api_key_env: str = "OPENAI_API_KEY") -> tuple[str, str]:
    """Use explicitly supplied endpoint/environment only; no Codex files or fallback."""
    base = base_url or os.environ.get("OPENAI_BASE_URL", "")
    key = os.environ.get(api_key_env, "")
    if not base.startswith("https://") or not key:
        raise ValueError("Supply an HTTPS --base-url/OPENAI_BASE_URL and the named API-key environment variable")
    return base.rstrip("/"), key


def request_response(base: str, key: str, payload: dict, timeout: int) -> dict:
    request = Request(base + "/responses", data=json.dumps(payload, ensure_ascii=False).encode(), headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json",
        "User-Agent": "constraint-exec-eval",
    }, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}: " + redact_text(error.read().decode(errors="replace").replace(key, "[REDACTED]"))[:1000]) from None
    if result.get("model") != MODEL:
        raise RuntimeError("Returned model differs from requested Sol: " + str(result.get("model")))
    if result.get("status") != "completed":
        raise RuntimeError("Response did not complete: " + str(result.get("status")))
    return result


def portable_output(items: list[dict]) -> list[dict]:
    """Retain public tool/text history without resource-bound response IDs."""
    portable = []
    for item in items:
        if item.get("type") == "function_call":
            portable.append({key: item[key] for key in ("type", "name", "call_id", "arguments")})
        elif item.get("type") == "message":
            text = "\n".join(c["text"] for c in item.get("content", []) if c.get("type") == "output_text")
            if text:
                portable.append({"role": "assistant", "content": text})
    return portable


def run_checks(workspace: Path) -> dict:
    result = subprocess.run([sys.executable, "-I", "-c",
        "import sys,unittest;sys.path.insert(0,'.');s=unittest.defaultTestLoader.discover('.',pattern='test_contract.py');r=unittest.TextTestRunner(verbosity=2).run(s);sys.exit(not r.wasSuccessful())"],
        cwd=workspace, env=clean_subprocess_environment(), capture_output=True, text=True, timeout=10)
    return {"passed": result.returncode == 0, "output": redact_text(result.stdout + result.stderr)}


def execute_tool(workspace: Path, name: str, arguments: dict) -> dict:
    if name == "run_checks":
        if arguments:
            raise ValueError("run_checks takes no arguments")
        return run_checks(workspace)
    if name not in {"read_file", "write_file"} or arguments.get("path") != "app.py":
        raise ValueError("Only app.py may be accessed by file tools")
    path = workspace / "app.py"
    if name == "read_file":
        return {"content": path.read_text(encoding="utf-8")}
    content = arguments.get("content")
    if not isinstance(content, str) or len(content) > 50000:
        raise ValueError("Expected bounded source text")
    path.write_text(content, encoding="utf-8")
    return {"written": "app.py"}


def evaluate(case: dict, variant: str, instructions: str, base: str, key: str,
             output: Path, effort: str, timeout: int, max_rounds: int, repeat: int) -> dict:
    started = time.perf_counter()
    artifact = output / "raw" / f"r{repeat}" / variant / case["id"]
    artifact.mkdir(parents=True, exist_ok=True)
    row = {"case_id": case["id"], "variant": variant, "repeat": repeat, "model": MODEL,
           "case_hash": digest(json.dumps(case, sort_keys=True, ensure_ascii=False)),
           "instructions_hash": digest(instructions), "success": False, "calls": 0, "returned_models": [],
           "usage": {"input_tokens": 0, "output_tokens": 0}, "tool_trace": []}
    with tempfile.TemporaryDirectory(prefix="constraint-sol-") as directory:
        workspace = Path(directory)
        fixture = FIXTURES.get(case.get("fixture"))
        if fixture:
            (workspace / "app.py").write_text(fixture["source"], encoding="utf-8")
            (workspace / "test_contract.py").write_text(fixture["tests"], encoding="utf-8")
        messages = list(case["messages"])
        if fixture:
            instructions += "\n\n" + WORKSPACE_INSTRUCTIONS
        try:
            for _ in range(max_rounds):
                payload = {"model": MODEL, "instructions": instructions, "input": messages,
                           "reasoning": {"effort": effort}, "text": {"verbosity": "low"},
                           "max_output_tokens": 4096, "store": False}
                if fixture:
                    payload["tools"] = TOOLS
                response = request_response(base, key, payload, timeout)
                row["calls"] += 1
                row["returned_models"].append(response["model"])
                for metric in row["usage"]:
                    row["usage"][metric] += response.get("usage", {}).get(metric, 0)
                items = response.get("output", [])
                calls = [item for item in items if item.get("type") == "function_call"]
                messages.extend(portable_output(items))
                if calls:
                    if not fixture:
                        raise ValueError("Unexpected function call in answer-only case")
                    for call in calls:
                        try:
                            arguments = json.loads(call["arguments"])
                            result = execute_tool(workspace, call["name"], arguments)
                        except (ValueError, KeyError, OSError, subprocess.TimeoutExpired) as error:
                            result = {"error": redact_text(str(error))}
                        row["tool_trace"].append({"name": call["name"], "result": result})
                        messages.append({"type": "function_call_output", "call_id": call["call_id"],
                                         "output": json.dumps(result, ensure_ascii=False)})
                    continue
                answer = "\n".join(content["text"] for item in items if item.get("type") == "message"
                                   for content in item.get("content", []) if content.get("type") == "output_text")
                if not answer.strip():
                    raise ValueError("No final answer")
                atomic_write_text(artifact / "answer.md", answer + "\n")
                row["success"] = True
                break
            else:
                raise RuntimeError("Tool-round budget exhausted")
        except Exception as error:
            row["error"] = redact_text(str(error).replace(key, "[REDACTED]"))[:1500]
        if fixture:
            atomic_write_text(artifact / "app.py", (workspace / "app.py").read_text(encoding="utf-8"))
            try:
                row["artifact_checks"] = run_checks(workspace)
            except Exception as error:
                row["artifact_checks"] = {"passed": False, "error": redact_text(str(error))}
            row["file_changed"] = (workspace / "app.py").read_text(encoding="utf-8") != fixture["source"]
            row["model_ran_checks"] = any(t["name"] == "run_checks" for t in row["tool_trace"])
    row["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", help="Independent HTTPS Responses endpoint; defaults to OPENAI_BASE_URL")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY", help="Name of the independent API-key environment variable")
    parser.add_argument("--output", type=Path, default=ROOT / "evals/experiments/sol-interaction")
    parser.add_argument("--case", action="append")
    parser.add_argument("--variant", choices=("rc10", "previous", "removal-v1", "tail-v2", "compact-v3", "upgraded"), action="append")
    parser.add_argument("--cases", type=Path, default=ROOT / "evals/interaction_cases.json")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--reasoning-effort", choices=("low", "medium", "high", "xhigh", "max"), default="medium")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--max-rounds", type=int, default=6)
    args = parser.parse_args()
    if min(args.jobs, args.repeats, args.timeout, args.max_rounds) < 1:
        parser.error("Budgets must be positive")
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    if args.case:
        unknown = set(args.case) - {case["id"] for case in cases}
        if unknown:
            parser.error("Unknown cases: " + ", ".join(sorted(unknown)))
        cases = [case for case in cases if case["id"] in args.case]
    base, key = connection(args.base_url, args.api_key_env)
    variants = {"rc10": body(ROOT / "evals/baselines/constraint-exec-rc10.md"),
                "previous": body(ROOT / "evals/baselines/constraint-exec-wording-only.md"),
                "removal-v1": body(ROOT / "evals/baselines/constraint-exec-removal-v1.md"),
                "tail-v2": body(ROOT / "evals/baselines/constraint-exec-tail-v2.md"),
                "compact-v3": body(ROOT / "evals/baselines/constraint-exec-compact-v3.md"),
                "upgraded": body(ROOT / "skills/constraint-exec/SKILL.md")}
    selected_variants = args.variant or ["rc10", "upgraded"]
    variants = {name: text for name, text in variants.items() if name in selected_variants}
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output / "results.json"
    if path.exists():
        parser.error("Output already contains results; select a new output directory")
    metadata = {"created_at": datetime.now(timezone.utc).isoformat(), "model": MODEL,
                "transport": "responses-public-transcript-v1", "runner_hash": digest(Path(__file__).read_text()),
                "fixtures_hash": digest(json.dumps(FIXTURES, sort_keys=True)), "reasoning_effort": args.reasoning_effort, "verbosity": "low",
                "repeats": args.repeats, "expected_rows": len(cases) * len(variants) * args.repeats,
                "dataset_hash": digest(args.cases.read_text()), "endpoint_hash": digest(base), "semantic_review": "pending", "results": []}
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = []
        for repeat in range(1, args.repeats + 1):
            for index, case in enumerate(cases):
                order = list(variants.items())
                if (index + repeat) % 2:
                    order.reverse()
                for variant, instructions in order:
                    futures.append(executor.submit(evaluate, case, variant, instructions, base, key,
                                                   args.output, args.reasoning_effort, args.timeout, args.max_rounds, repeat))
        for future in as_completed(futures):
            row = future.result()
            metadata["results"].append(row)
            metadata["results"].sort(key=lambda r: (r["repeat"], r["case_id"], r["variant"]))
            path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"{row['variant']} {row['case_id']}: generation={row['success']} artifact={row.get('artifact_checks', {}).get('passed', 'n/a')}", flush=True)
    if any(not row["success"] for row in metadata["results"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
