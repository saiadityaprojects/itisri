# Itisri Architecture

Full design documentation. See `README.md` for the high-level overview
and the research paper for the complete specification.

## Components

1. Instrumentation — intercepts agent actions
2. Baseline — learns behavioral profiles
3. Detection — rules + anomaly scoring
4. Mapper — enumerates capabilities
5. Response — enforces policy

## Data Flow

Action → Instrumentation → Rule Engine + Anomaly Engine → Score Fusion → Response Executor → Enforcement
