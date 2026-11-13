from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evals"))
import run_interaction_eval as runner
from interaction_fixtures import FIXTURES


class InteractionEvaluationTests(unittest.TestCase):
    def test_fixtures_expose_missing_behavior(self):
        for fixture in FIXTURES.values():
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory)
                (workspace / "app.py").write_text(fixture["source"], encoding="utf-8")
                (workspace / "test_contract.py").write_text(fixture["tests"], encoding="utf-8")
                self.assertFalse(runner.run_checks(workspace)["passed"])

    def test_file_tools_reject_other_paths_and_unknown_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            for path in ("../app.py", "/tmp/app.py", "test_contract.py"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    runner.execute_tool(workspace, "write_file", {"path": path, "content": "x"})
            with self.assertRaises(ValueError):
                runner.execute_tool(workspace, "shell", {})

    def test_real_patch_and_checks_are_independent_of_final_claim(self):
        case = {"id": "ratio-fix", "fixture": "ratio-fix", "messages": [{"role": "user", "content": "Fix ratio"}]}
        source = FIXTURES["ratio-fix"]["source"].replace("return part / total", "return part / total if total else 0.0")
        responses = [
            {"model": runner.MODEL, "output": [{"type": "function_call", "name": "write_file", "call_id": "a",
                         "arguments": json.dumps({"path": "app.py", "content": source})}]},
            {"model": runner.MODEL, "output": [{"type": "function_call", "name": "run_checks", "call_id": "b", "arguments": "{}"}]},
            {"model": runner.MODEL, "output": [{"type": "message", "content": [{"type": "output_text", "text": "Done"}]}]},
        ]
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, "request_response", side_effect=responses):
            row = runner.evaluate(case, "candidate", "", "https://example.test", "test-key", Path(directory), "medium", 10, 4, 1)
            self.assertTrue(row["success"])
            self.assertTrue(row["file_changed"])
            self.assertTrue(row["model_ran_checks"])
            self.assertTrue(row["artifact_checks"]["passed"])

    def test_false_completion_claim_does_not_pass_artifact_contract(self):
        case = {"id": "ratio-fix", "fixture": "ratio-fix", "messages": [{"role": "user", "content": "Fix ratio"}]}
        response = {"model": runner.MODEL, "output": [{"type": "message", "content": [{"type": "output_text", "text": "Fixed; tests passed"}]}]}
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, "request_response", return_value=response):
            row = runner.evaluate(case, "candidate", "", "https://example.test", "test-key", Path(directory), "medium", 10, 4, 1)
            self.assertTrue(row["success"])
            self.assertFalse(row["file_changed"])
            self.assertFalse(row["model_ran_checks"])
            self.assertFalse(row["artifact_checks"]["passed"])

    def test_answer_only_case_has_no_workspace_tools(self):
        case = {"id": "chat", "messages": [{"role": "user", "content": "Hi"}]}
        response = {"model": runner.MODEL, "output": [{"type": "message", "content": [{"type": "output_text", "text": "Hello"}]}]}
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, "request_response", return_value=response) as request:
            row = runner.evaluate(case, "candidate", "", "https://example.test", "test-key", Path(directory), "medium", 10, 1, 1)
            self.assertTrue(row["success"])
            self.assertNotIn("tools", request.call_args.args[2])
            self.assertNotIn("artifact_checks", row)

    def test_missing_final_answer_and_exhaustion_are_recorded(self):
        case = {"id": "chat", "messages": [{"role": "user", "content": "Hi"}]}
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, "request_response", return_value={"model": runner.MODEL, "output": []}):
            row = runner.evaluate(case, "candidate", "", "https://example.test", "test-key", Path(directory), "medium", 10, 1, 1)
            self.assertFalse(row["success"])
            self.assertIn("No final answer", row["error"])

    def test_provider_model_and_completion_are_verified(self):
        for result in ({"model": "gpt-6-astra", "status": "completed"}, {"model": runner.MODEL, "status": "incomplete"}):
            with self.subTest(result=result), patch.object(runner, "urlopen") as transport:
                transport.return_value.__enter__.return_value.read.return_value = json.dumps(result)
                with self.assertRaises(RuntimeError):
                    runner.request_response("https://example.test", "test-key", {}, 10)

    def test_public_transcript_removes_resource_bound_state(self):
        items = [
            {"type": "reasoning", "id": "rs_remote", "encrypted_content": "resource-bound"},
            {"type": "function_call", "id": "fc_remote", "name": "run_checks", "call_id": "call_1", "arguments": "{}"},
            {"type": "message", "id": "msg_remote", "content": [{"type": "output_text", "text": "Done"}]},
        ]
        result = runner.portable_output(items)
        self.assertEqual(result, [
            {"type": "function_call", "name": "run_checks", "call_id": "call_1", "arguments": "{}"},
            {"role": "assistant", "content": "Done"},
        ])

    def test_connection_uses_explicit_environment_without_reading_files(self):
        with patch.dict("os.environ", {"INDEPENDENT_SOL_KEY": "test-key"}), patch.object(Path, "read_text", side_effect=AssertionError("No configuration reads")):
            self.assertEqual(runner.connection("https://example.test/v1", "INDEPENDENT_SOL_KEY"), ("https://example.test/v1", "test-key"))

    def test_connection_rejects_plaintext_or_missing_credential(self):
        with patch.dict("os.environ", {"OPENAI_BASE_URL": "http://example.test", "OPENAI_API_KEY": "test-key"}):
            with self.assertRaises(ValueError): runner.connection()
        with patch.dict("os.environ", {"OPENAI_BASE_URL": "https://example.test", "OPENAI_API_KEY": ""}):
            with self.assertRaises(ValueError): runner.connection()


if __name__ == "__main__":
    unittest.main()
