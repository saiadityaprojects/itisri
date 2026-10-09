"""Deterministic mock LLM for the demo agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class LLMResponse:
    """A single LLM response: either a tool call or a final answer."""

    tool_call: Optional[dict[str, Any]] = None
    final_answer: Optional[str] = None


class MockLLM:
    """Deterministic mock LLM for reproducible demos and benchmarks."""

    def __init__(self, poison: Optional[dict[str, Any]] = None) -> None:
        self.poison = poison
        self._step = 0

    def reset(self) -> None:
        self._step = 0

    def next_action(self) -> LLMResponse:
        if self.poison is not None:
            if self._step == 0:
                self._step += 1
                return LLMResponse(tool_call=self.poison)
            return LLMResponse(final_answer="Task complete.")

        plan = [
            {
                "tool": "query_brand_scores",
                "args": {"tenant_id": "tenant_a", "brand": "Acme"},
            },
            {
                "tool": "generate_report",
                "args": {"tenant_id": "tenant_a", "brand": "Acme"},
            },
        ]

        if self._step < len(plan):
            call = plan[self._step]
            self._step += 1
            return LLMResponse(tool_call=call)

        return LLMResponse(final_answer="Brand visibility report generated.")
