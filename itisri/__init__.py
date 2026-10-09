"""
Itisri — Runtime detection and response for agentic AI security.

Public API:
    AgentAction          Structured event emitted on every intercepted action
    ItisriConfig         Configuration object
    monitored_tool       Decorator to instrument a tool function
"""

__version__ = "0.1.0"

from itisri.core.events import AgentAction, ActionType, RiskLevel
from itisri.core.config import ItisriConfig
from itisri.instrumentation.decorators import monitored_tool

__all__ = [
    "AgentAction",
    "ActionType",
    "RiskLevel",
    "ItisriConfig",
    "monitored_tool",
    "__version__",
]
