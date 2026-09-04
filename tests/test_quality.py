import json
from pathlib import Path


def test_quality_gate_has_structured_results():
    report = json.loads(Path("reports/quality_gate.json").read_text(encoding="utf-8"))
    assert len(report) >= 12
    assert {"rule_name", "severity", "observed_value", "expected_condition", "status"} <= set(report[0])


def test_quality_gate_has_no_critical_failures():
    report = json.loads(Path("reports/quality_gate.json").read_text(encoding="utf-8"))
    failures = [r for r in report if r["severity"] == "critical" and r["status"] == "FAIL"]
    assert failures == []

