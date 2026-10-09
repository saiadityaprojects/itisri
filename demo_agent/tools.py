"""Mock tools for the demo brand-visibility agent."""

from __future__ import annotations

from typing import Any

from itisri.core.events import RiskLevel
from itisri.instrumentation.decorators import monitored_tool


_DB: dict[str, list[dict[str, Any]]] = {
    "tenant_a": [
        {"brand": "Acme", "score": 0.72, "source": "chatgpt"},
        {"brand": "Acme", "score": 0.68, "source": "gemini"},
    ],
    "tenant_b": [
        {"brand": "Beta Corp", "score": 0.81, "source": "claude"},
        {"brand": "Beta Corp", "score": 0.77, "source": "perplexity"},
    ],
}


@monitored_tool(
    risk_level=RiskLevel.LOW,
    agent_id="brand_visibility_agent",
    tenant_param="tenant_id",
)
def query_brand_scores(tenant_id: str, brand: str) -> list[dict[str, Any]]:
    """Read brand scores for a tenant. Low-risk read operation."""
    rows = _DB.get(tenant_id, [])
    return [r for r in rows if r["brand"].lower() == brand.lower()]


@monitored_tool(
    risk_level=RiskLevel.LOW,
    agent_id="brand_visibility_agent",
)
def fetch_url(url: str) -> str:
    """Fetch the contents of a URL. The target URL is the risk surface."""
    return f"<html><body>Content from {url}</body></html>"


@monitored_tool(
    risk_level=RiskLevel.MEDIUM,
    agent_id="brand_visibility_agent",
    tenant_param="tenant_id",
)
def generate_report(tenant_id: str, brand: str) -> dict[str, Any]:
    """Generate a brand visibility report. Medium-risk write operation."""
    rows = query_brand_scores(
        tenant_id=tenant_id, brand=brand, session_id="report_internal"
    )
    avg = sum(r["score"] for r in rows) / len(rows) if rows else 0.0
    return {
        "tenant_id": tenant_id,
        "brand": brand,
        "average_score": round(avg, 3),
        "sources": [r["source"] for r in rows],
    }


@monitored_tool(
    risk_level=RiskLevel.CRITICAL,
    agent_id="brand_visibility_agent",
    tenant_param="tenant_id",
)
def export_client_data(tenant_id: str, destination: str) -> dict[str, Any]:
    """Export all client data to an external destination."""
    return {
        "tenant_id": tenant_id,
        "destination": destination,
        "records_exported": len(_DB.get(tenant_id, [])),
        "status": "exported",
    }
