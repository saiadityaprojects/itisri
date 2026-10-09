"""ItisriConfig — central configuration object."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ItisriConfig:
    """Configuration for an Itisri deployment."""

    agent_id: str = "default"
    deployment_name: str = "local"

    data_dir: Path = field(
        default_factory=lambda: Path(os.getenv("ITISRI_DATA_DIR", "./data"))
    )

    anomaly_threshold: float = 0.65
    rule_severity_floor: str = "low"

    alpha_isolation_forest: float = 0.4
    beta_markov: float = 0.3
    gamma_embedding: float = 0.3

    baseline_alpha: float = 0.97
    baseline_min_samples: int = 50
    baseline_contamination: float = 0.05

    default_response_mode: str = "enforce"
    require_human_approval_for_critical: bool = True

    log_level: str = field(
        default_factory=lambda: os.getenv("ITISRI_LOG_LEVEL", "INFO")
    )

    def __post_init__(self) -> None:
        total = (
            self.alpha_isolation_forest
            + self.beta_markov
            + self.gamma_embedding
        )
        if abs(total - 1.0) > 1e-6:
            raise ValueError(
                f"Score fusion weights must sum to 1.0, got {total:.4f}"
            )

        self.data_dir = Path(self.data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
