"""Demo entry point. Run: python -m demo_agent.run"""

from __future__ import annotations

from demo_agent.agent import BrandVisibilityAgent
from demo_agent.llm import MockLLM
from itisri.instrumentation.decorators import clear_emitted, emitted_actions


def main() -> None:
    print("=" * 72)
    print("Itisri Demo — Brand Visibility Agent")
    print("=" * 72)

    clear_emitted()

    llm = MockLLM()
    agent = BrandVisibilityAgent(llm=llm)

    print(f"\nAgent ID:   {agent.agent_id}")
    print(f"Session ID: {agent.session_id}\n")

    final = agent.run()
    print(f"\n[Agent final answer] {final}\n")

    actions = emitted_actions()
    print("=" * 72)
    print(f"Captured {len(actions)} AgentAction events")
    print("=" * 72)

    for i, action in enumerate(actions, start=1):
        print(f"\n#{i}  {action.action_type.value}")
        print(f"    tool:        {action.tool_name}")
        print(f"    risk:        {action.risk_level.value}")
        print(f"    session:     {action.session_id}")
        print(f"    tenant:      {action.tenant_id}")
        print(f"    duration_ms: {action.duration_ms:.2f}")
        print(f"    parameters:  {action.parameters}")


if __name__ == "__main__":
    main()
