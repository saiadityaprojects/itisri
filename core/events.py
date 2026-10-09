"""
AgentAction — the structured event emitted on every intercepted action.

Every tool call, memory operation, and model output produces one of these.
This is the atomic unit of observability in Itisri.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional


class ActionType(str, Enum):
    """The four categories of agent actions Itisri monitors."""

    TOOL_CALL = "tool_call"
    MEMORY_READ = "memory_read"
    MEMORY_WRITE = "memory_write"
    MODEL_OUTPUT = "model_output"


class RiskLevel(str, Enum):
    """Risk classification for a tool or action."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentAction:
    """A single intercepted agent action."""

    timestamp: float
    agent_id: str
    session_id: str
    action_id: str
    action_type: ActionType
    tool_name: Optional[str] = None
    parameters: dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    risk_level: RiskLevel = RiskLevel.LOW
    context: list[str] = field(default_factory=list)
    provenance: Optional[str] = None
    tenant_id: Optional[str] = None
    duration_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        agent_id: str,
        session_id: str,
        action_type: ActionType,
        tool_name: Optional[str] = None,
        parameters: Optional[dict[str, Any]] = None,
        risk_level: RiskLevel = RiskLevel.LOW,
        context: Optional[list[str]] = None,
        provenance: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> "AgentAction":
        """Convenience constructor that fills in timestamp and action_id."""
        return cls(
            timestamp=time.time(),
            agent_id=agent_id,
            session_id=session_id,
            action_id=str(uuid.uuid4()),
            action_type=action_type,
            tool_name=tool_name,
            parameters=parameters or {},
            risk_level=risk_level,
            context=context or [],
            provenance=provenance,
            tenant_id=tenant_id,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serializable representation (for JSON, storage, or transport)."""
        d = asdict(self)
        d["action_type"] = self.action_type.value
        d["risk_level"] = self.risk_level.value
        return d

    def signature(self) -> str:
        """
        Short signature used for Markov sequence modeling.

        For tool calls, this is the tool name. For other action types,
        it's the action type value. This is the alphabet of the Markov chain.
        """
        if self.action_type == ActionType.TOOL_CALL and self.tool_name:
            return self.tool_name
        return self.action_type.value
