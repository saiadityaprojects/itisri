"""Tests for the AgentAction event schema."""

from itisri.core.events import ActionType, AgentAction, RiskLevel


def test_create_fills_required_fields() -> None:
    action = AgentAction.create(
        agent_id="agent_1",
        session_id="session_1",
        action_type=ActionType.TOOL_CALL,
        tool_name="query_brand_scores",
        parameters={"brand": "Acme"},
        risk_level=RiskLevel.LOW,
        tenant_id="tenant_a",
    )

    assert action.agent_id == "agent_1"
    assert action.session_id == "session_1"
    assert action.action_type == ActionType.TOOL_CALL
    assert action.tool_name == "query_brand_scores"
    assert action.risk_level == RiskLevel.LOW
    assert action.tenant_id == "tenant_a"
    assert action.timestamp > 0
    assert action.action_id


def test_to_dict_is_json_safe() -> None:
    action = AgentAction.create(
        agent_id="agent_1",
        session_id="session_1",
        action_type=ActionType.MODEL_OUTPUT,
    )
    d = action.to_dict()

    assert d["action_type"] == "model_output"
    assert d["risk_level"] == "low"
    assert isinstance(d["timestamp"], float)
    assert isinstance(d["parameters"], dict)


def test_signature_uses_tool_name_for_tool_calls() -> None:
    action = AgentAction.create(
        agent_id="a",
        session_id="s",
        action_type=ActionType.TOOL_CALL,
        tool_name="fetch_url",
    )
    assert action.signature() == "fetch_url"


def test_signature_uses_action_type_for_non_tool_actions() -> None:
    action = AgentAction.create(
        agent_id="a",
        session_id="s",
        action_type=ActionType.MEMORY_READ,
    )
    assert action.signature() == "memory_read"
