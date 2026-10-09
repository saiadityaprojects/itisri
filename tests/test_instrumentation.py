"""Tests for the @monitored_tool decorator."""

from itisri.core.events import ActionType, RiskLevel
from itisri.instrumentation.decorators import (
    clear_emitted,
    emitted_actions,
    monitored_tool,
)


def test_decorator_emits_action_on_call() -> None:
    clear_emitted()

    @monitored_tool(risk_level=RiskLevel.HIGH, agent_id="test_agent")
    def my_tool(x: int) -> int:
        return x * 2

    result = my_tool(21)

    assert result == 42
    actions = emitted_actions()
    assert len(actions) == 1
    assert actions[0].tool_name == "my_tool"
    assert actions[0].action_type == ActionType.TOOL_CALL
    assert actions[0].risk_level == RiskLevel.HIGH
    assert actions[0].agent_id == "test_agent"
    assert actions[0].parameters.get("x") == 21


def test_decorator_emits_on_exception() -> None:
    clear_emitted()

    @monitored_tool(risk_level=RiskLevel.LOW, agent_id="test_agent")
    def failing_tool() -> None:
        raise ValueError("boom")

    try:
        failing_tool()
    except ValueError:
        pass

    actions = emitted_actions()
    assert len(actions) == 1
    assert "error" in actions[0].metadata
    assert actions[0].metadata["error"] == "boom"


def test_decorator_captures_tenant_id() -> None:
    clear_emitted()

    @monitored_tool(
        risk_level=RiskLevel.LOW,
        agent_id="test_agent",
        tenant_param="tenant_id",
    )
    def scoped_tool(tenant_id: str, query: str) -> str:
        return "ok"

    scoped_tool(tenant_id="tenant_a", query="test")

    actions = emitted_actions()
    assert actions[0].tenant_id == "tenant_a"


def test_decorator_respects_session_override() -> None:
    clear_emitted()

    @monitored_tool(risk_level=RiskLevel.LOW, agent_id="test_agent")
    def simple_tool() -> str:
        return "ok"

    simple_tool(session_id="override_session")

    actions = emitted_actions()
    assert actions[0].session_id == "override_session"
