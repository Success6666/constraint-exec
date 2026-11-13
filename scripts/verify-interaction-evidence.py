"""Check published paired outputs, frozen reviews and cost totals without API calls."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
from run_interaction_eval import body, run_checks  # noqa: E402
from interaction_fixtures import FIXTURES  # noqa: E402

EXPERIMENTS = (
    "research-transfer-2026-11-09",
    "research-refined-2026-11-09",
    "research-grounded-2026-11-09",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify_experiment(root: Path, name: str) -> dict:
    exp = root / "evals/experiments" / name
    cases_path = root / "evals/research_combined_cases.json"
    cases = {case["id"]: case for case in read_json(cases_path)}
    results = read_json(exp / "results.json")
    rows = results["results"]
    require(results["dataset_hash"] == digest(cases_path.read_bytes()), f"{name}: dataset hash")
    require(results["fixtures_hash"] == digest(json.dumps(FIXTURES, sort_keys=True).encode()), f"{name}: fixture hash")
    expected = {(case, arm, 1) for case in cases for arm in ("compact-v3", "upgraded")}
    actual = {(r["case_id"], r["variant"], r["repeat"]) for r in rows}
    require(actual == expected and len(rows) == len(expected) == 120, f"{name}: pair coverage")
    for row in rows:
        case = cases[row["case_id"]]
        case_hash = digest(json.dumps(case, sort_keys=True, ensure_ascii=False).encode())
        instructions = body(exp / f"instructions-{row['variant']}.md")
        require(row["case_hash"] == case_hash, f"{name}: case hash {row['case_id']}")
        require(row["instructions_hash"] == digest(instructions.encode()), f"{name}: instruction hash")
        require(row["success"] and row["calls"] > 0, f"{name}: incomplete result")
        require(row["returned_models"] == [results["model"]] * row["calls"], f"{name}: model evidence")
        require(all(isinstance(v, int) and v >= 0 for v in row["usage"].values()), f"{name}: invalid usage")
        if "artifact_checks" in row:
            artifact = exp / "raw" / f"r{row['repeat']}" / row["variant"] / row["case_id"] / "app.py"
            fixture = FIXTURES[case["fixture"]]
            with tempfile.TemporaryDirectory(prefix="constraint-evidence-check-") as directory:
                workspace = Path(directory)
                (workspace / "app.py").write_bytes(artifact.read_bytes())
                (workspace / "test_contract.py").write_text(fixture["tests"], encoding="utf-8")
                require(run_checks(workspace)["passed"], f"{name}: saved workspace fails {row['case_id']}")
    frozen_path = exp / "annotations-frozen.json"
    frozen = read_json(frozen_path)
    require(digest(frozen_path.read_bytes()) == (exp / "annotations.sha256").read_text().strip(), f"{name}: review hash")
    require(frozen["independent"] is False, f"{name}: author review provenance")
    records = {r["review_packet_id"]: r for r in frozen["records"]}
    require(len(records) == len(frozen["records"]) == 120, f"{name}: review coverage")
    packets = read_json(exp / "review-packets.json")
    key = read_json(exp / "review-key.json")
    observed = set()
    for packet in packets:
        for side, answer in packet["answers"].items():
            ident = packet["id"] + side
            arm = key[ident]
            triple = (packet["case_id"], arm, packet["repeat"])
            require(triple not in observed, f"{name}: duplicate mapped answer")
            observed.add(triple)
            raw = exp / "raw" / f"r{packet['repeat']}" / arm / packet["case_id"] / "answer.md"
            require(raw.read_text(encoding="utf-8") == answer["text"], f"{name}: raw answer mismatch")
            require(digest(answer["text"].encode()) == answer["sha256"] == records[ident]["answer_hash"], f"{name}: answer hash")
            require(records[ident]["case_id"] == packet["case_id"], f"{name}: review mapping")
    require(observed == expected, f"{name}: mapped pair coverage")
    semantic = read_json(exp / "semantic-review.json")
    require(semantic["review"] == frozen, f"{name}: frozen review differs")
    capability = read_json(exp / "capability-checks.json")
    summary = {}
    for arm in ("compact-v3", "upgraded"):
        annotations = [r for ident, r in records.items() if key[ident] == arm]
        samples = [r for r in rows if r["variant"] == arm]
        defenses = [r for r in annotations if r["count_unnecessary_defense"]]
        accuracy = [r for r in annotations if r["category"] == "accuracy-control"]
        workspace = [r for r in samples if "artifact_checks" in r]
        controls = [r for ident, r in capability.items() if key[ident] == arm]
        current = dict(
            unnecessary_defense=sum(r["unnecessary_defense"] for r in defenses),
            defense_denominator=len(defenses),
            fact_errors=sum(not r["facts_supported"] for r in annotations),
            fact_error_cases=[r["case_id"] for r in annotations if not r["facts_supported"]],
            defense_cases=[r["case_id"] for r in defenses if r["unnecessary_defense"]],
            accuracy_pass=sum(r["accuracy_control_pass"] for r in accuracy), accuracy_total=len(accuracy),
            workspace_pass=sum(r["artifact_checks"]["passed"] and r["file_changed"] and r["model_ran_checks"] for r in workspace),
            workspace_total=len(workspace), calls=sum(r["calls"] for r in samples),
            input_tokens=sum(r["usage"]["input_tokens"] for r in samples),
            output_tokens=sum(r["usage"]["output_tokens"] for r in samples),
            total_tokens=sum(sum(r["usage"].values()) for r in samples),
        )
        require(current == semantic["summary"][arm], f"{name}: stale semantic summary for {arm}")
        current.update(capability_pass=sum(r["passed"] for r in controls), capability_total=len(controls))
        require(len(controls) == 4, f"{name}: capability coverage")
        summary[arm] = current
    if (exp / "summary.json").exists():
        saved = read_json(exp / "summary.json")
        require(all(saved[arm] == summary[arm] for arm in summary), f"{name}: stale final summary")
    return summary


def main() -> int:
    summaries = {name: verify_experiment(ROOT, name) for name in EXPERIMENTS}
    publication = read_json(ROOT / "research/2026-11-13-publication-data.json")
    for name, summary in summaries.items():
        require(publication["experiments"][name]["summary"] == summary, f"{name}: publication summary")
    totals = dict(paired_cases=180,
                  model_calls=sum(arm["calls"] for summary in summaries.values() for arm in summary.values()),
                  total_tokens=sum(arm["total_tokens"] for summary in summaries.values() for arm in summary.values()))
    require(publication["development_totals"] == totals, "stale development totals")
    for relative, expected in publication["evidence_sha256"].items():
        require(digest((ROOT / relative).read_bytes()) == expected, f"publication hash: {relative}")
    entry = ROOT / "skills/constraint-exec/SKILL.md"
    require(digest(entry.read_bytes()) == publication["skill"]["entry_sha256"], "published entry hash")
    require((ROOT / "VERSION").read_text().strip() == publication["repository_version"], "published version")
    print(json.dumps({"status": "pass", "experiments": len(summaries), **totals}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
