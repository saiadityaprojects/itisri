"""Tests that the benchmark scenarios run end-to-end."""

from benchmark.runner import SCENARIOS, run_scenario


def test_all_scenarios_execute() -> None:
    for sid in sorted(SCENARIOS.keys()):
        result = run_scenario(sid)
        assert result["scenario_id"] == sid
        assert result["actions"], f"Scenario {sid} produced no actions"
        assert result["expected_detections"], f"Scenario {sid} missing expected detections"


def test_scenario_03_invokes_export() -> None:
    result = run_scenario("03")
    tool_names = [a["tool_name"] for a in result["actions"]]
    assert "export_client_data" in tool_names


def test_scenario_04_uses_foreign_tenant() -> None:
    result = run_scenario("04")
    tenant_ids = [a.get("tenant_id") for a in result["actions"]]
    assert "tenant_b" in tenant_ids
