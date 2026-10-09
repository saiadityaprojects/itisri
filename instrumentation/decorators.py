"""
@monitored_tool — decorator that instruments a tool function.

When the decorated tool is invoked, Itisri emits an AgentAction event
capturing the tool name, parameters, risk level, tenant scope, and
execution duration.
"""

from __future__ import annotations

import functools
import inspect
import time
from typing import Any, Callable, Optional

from itisri.core.events import ActionType, AgentAction, RiskLevel


_EMITTED: list[AgentAction] = []


def emitted_actions() -> list[AgentAction]:
    """Return all emitted actions (debug helper)."""
    return _EMITTED


def clear_emitted() -> None:
    """Clear the emitted actions list (debug helper)."""
    _EMITTED.clear()


def emit(action: AgentAction) -> None:
    """Emit an AgentAction to the global sink."""
    _EMITTED.append(action)


def monitored_tool(
    risk_level: RiskLevel = RiskLevel.LOW,
    agent_id: str = "default",
    session_id: str = "default",
    tenant_param: Optional[str] = None,
) -> Callable:
    """Decorator factory for instrumenting a tool function."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sid = kwargs.pop("session_id", session_id)

            tenant_id = None
            if tenant_param:
                tenant_id = kwargs.get(tenant_param)
                if tenant_id is None and args:
                    try:
                        sig = inspect.signature(func)
                        params = list(sig.parameters.keys())
                        if tenant_param in params:
                            idx = params.index(tenant_param)
                            if idx < len(args):
                                tenant_id = args[idx]
                    except (TypeError, ValueError):
                        pass

            action = AgentAction.create(
                agent_id=agent_id,
                session_id=sid,
                action_type=ActionType.TOOL_CALL,
                tool_name=func.__name__,
                parameters=_safe_params(func, args, kwargs),
                risk_level=risk_level,
                tenant_id=tenant_id,
            )

            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                action.result = _safe_repr(result)
                return result
            except Exception as exc:
                action.metadata["error"] = str(exc)
                raise
            finally:
                action.duration_ms = (time.perf_counter() - start) * 1000.0
                emit(action)

        return wrapper

    return decorator


def _safe_params(func: Callable, args: tuple, kwargs: dict) -> dict[str, Any]:
    try:
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        bound: dict[str, Any] = {}
        for i, value in enumerate(args):
            if i < len(params):
                bound[params[i]] = _safe_repr(value)
        for k, v in kwargs.items():
            bound[k] = _safe_repr(v)
        return bound
    except (TypeError, ValueError):
        return {
            "_raw_args": _safe_repr(args),
            "_raw_kwargs": _safe_repr(kwargs),
        }


def _safe_repr(value: Any, max_len: int = 500) -> Any:
    try:
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value if not isinstance(value, str) else value[:max_len]
        if isinstance(value, (list, tuple)):
            return [_safe_repr(v, max_len) for v in value[:20]]
        if isinstance(value, dict):
            return {
                str(k): _safe_repr(v, max_len)
                for k, v in list(value.items())[:20]
            }
        return repr(value)[:max_len]
    except Exception:
        return "<unrepresentable>"
