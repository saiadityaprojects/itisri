"""Brand-visibility agent."""

from __future__ import annotations

import uuid
from typing import Callable

from demo_agent.llm import MockLLM
from demo_agent import tools as tool_module


class BrandVisibilityAgent:
    """A minimal agent that runs a plan against instrumented tools."""

    def __init__(
        self, llm: MockLLM, agent_id: str = "brand_visibility_agent"
    ) -> None:
        self.llm = llm
        self.agent_id = agent_id
        self.session_id = str(uuid.uuid4())
        self.tool_registry: dict[str, Callable] = self._build_registry()

    def _build_registry(self) -> dict[str, Callable]:
        return {
            "query_brand_scores": tool_module.query_brand_scores,
            "fetch_url": tool_module.fetch_url,
            "generate_report": tool_module.generate_report,
            "export_client_data": tool_module.export_client_data,
        }

    def run(self, max_steps: int = 10) -> str:
        self.llm.reset()

        for _ in range(max_steps):
            response = self.llm.next_action()

            if response.final_answer is not None:
                return response.final_answer

            if response.tool_call is None:
                return "Agent stopped: no action returned."

            tool_name = response.tool_call["tool"]
            args = dict(response.tool_call.get("args", {}))
            args["session_id"] = self.session_id

            if tool_name not in self.tool_registry:
                return f"Agent stopped: unknown tool '{tool_name}'."

            try:
                self.tool_registry[tool_name](**args)
            except TypeError as exc:
                return f"Agent stopped: bad args for '{tool_name}': {exc}"

        return "Agent stopped: max steps reached."
