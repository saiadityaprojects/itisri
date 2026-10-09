# Itisri

**Runtime detection and response for agentic AI security.**

Itisri watches AI agents the way a SOC watches endpoints. It intercepts every tool call, memory operation, and model output; learns what normal behavior looks like; and detects or blocks poisoning, hijacking, and privilege abuse before damage is done.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](#roadmap)

---

## Why Itisri Exists

Modern LLM agents retrieve web content, query databases, call APIs, and assemble outputs. This creates an attack surface that traditional security tools do not monitor. The defining vulnerability is **indirect prompt injection (IPI)**: an adversary embeds malicious instructions in content the agent retrieves during normal operation, and the agent executes them as if they came from its operator.

Existing defenses operate at the **content layer** — they try to classify whether text is malicious. This is a probabilistic, evadable task. Published benchmarks show system-prompt guardrails fail against **62%** of structured IPI payloads, and LLM-as-judge classifiers reduce attack success rate to **14%** at a latency cost of **182 ms** per inference.

Itisri shifts detection to the **action layer**. It monitors what the agent *does*, not what it *reads*. Behavior is observable. Baselines are learnable. Deviations are measurable. Enforcement is deterministic.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     USER / TASK INPUT                       │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  AGENT ORCHESTRATOR                         │
│              (LangGraph / LangChain / Custom)               │
└─────────────────────────────────────────────────────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
   Tool Calls         Memory Ops         Model Output
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                         ITISRI                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Instrument.  │─▶│  Baseline    │─▶│  Detection   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                                    │              │
│         ▼                                    ▼              │
│  ┌──────────────┐                    ┌──────────────┐       │
│  │  Surface     │                    │  Response    │       │
│  │  Mapper      │                    │  Executor    │       │
│  └──────────────┘                    └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
       Block / Alert / Log / Downgrade / Require Approval
```

1. **Instrumentation** wraps agent tools and intercepts every action.
2. **Baseline** learns statistical profiles of normal behavior per agent.
3. **Detection** runs rule-based policies and anomaly scoring in parallel.
4. **Surface Mapper** enumerates the agent's capabilities and flags risk.
5. **Response Executor** enforces policy-driven actions by severity.

---

## Detection Rules

Itisri ships with twelve detection rules mapped to **OWASP LLM Top 10 2025** and **MITRE ATLAS**.

| Rule ID | Detection | OWASP | ATLAS |
|---|---|---|---|
| ITI-RAG-001 | RAG document contains injection markers | LLM01 | AML.T0051 |
| ITI-RAG-002 | Retrieved doc deviates from topic baseline | LLM08 | AML.T0051 |
| ITI-INJ-003 | Input contains injection heuristics | LLM01 | AML.T0051 |
| ITI-INJ-004 | Injection concealed via Unicode/tag chars | LLM01 | AML.T0051 |
| ITI-TOOL-005 | Tool call outside baseline allowed set | LLM06 | AML.T0057 |
| ITI-TOOL-006 | Tool params contain non-allowlisted URLs | LLM05 | AML.T0057 |
| ITI-TOOL-007 | Tool call data size exceeds baseline 3σ | LLM06 | AML.T0057 |
| ITI-LEAK-008 | Cross-tenant data access detected | LLM02 | AML.T0057 |
| ITI-OUT-009 | Model output attempts to invoke a tool | LLM05 | AML.T0051 |
| ITI-OUT-010 | Output similarity to baseline below threshold | LLM09 | — |
| ITI-AGENCY-011 | Agent accesses unseen capability | LLM06 | AML.T0057 |
| ITI-DOS-012 | Action rate exceeds baseline threshold | LLM10 | AML.T0029 |

Rules are defined in YAML under `itisri/rules/` and are extensible without code changes.

---

## Quick Start

### Prerequisites

- Python 3.11 or newer
- Docker and Docker Compose (optional, for containerized demo)
- No API keys required — the demo agent uses a deterministic mock LLM

### Install Locally

```bash
git clone https://github.com/saiadityaprojects/itisri.git
cd itisri
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Run the Demo Agent

```bash
python -m demo_agent.run
```

You'll see a stream of `AgentAction` events printed to stdout as the demo agent processes a brand-visibility task.

### Run a Benchmark Scenario

```bash
python -m benchmark.runner --scenario 03
python -m benchmark.runner --all
```

### Run with Docker

```bash
docker-compose up --build
```

### Run Tests

```bash
pytest
```

---

## CLI

Itisri exposes a command-line interface for monitoring, scanning, and reporting.

```bash
# Watch an agent in real time
itisri watch --agent brand_agent

# Scan an agent's attack surface
itisri scan --agent brand_agent

# Run the full attack benchmark
itisri benchmark --all

# Generate an HTML report
itisri report --format html --output reports/latest.html

# Tail live alerts
itisri alerts --tail
```

---

## Repository Layout

```
itisri/
├── itisri/               # Core library
│   ├── core/             # Event schema, config
│   ├── instrumentation/  # Agent action interception
│   ├── baseline/         # Behavioral profiling
│   ├── detection/        # Rules + anomaly scoring
│   ├── response/         # Policy enforcement
│   ├── mapper/           # Attack surface enumeration
│   ├── cli/              # Command-line interface
│   └── rules/            # YAML detection rules
├── demo_agent/           # Vulnerable sample agent
├── benchmark/            # Six attack scenarios
├── tests/                # Unit and integration tests
└── docs/                 # Architecture and deployment docs
```

---

## Architecture

Itisri operates as a sidecar enforcement layer between the agent orchestrator and external resources. See `ARCHITECTURE.md` for the full design and `THREAT_MODEL.md` for the threat analysis mapped to MITRE ATLAS.

Core components:

- **`AgentAction`** — the structured event emitted on every intercepted action
- **`@monitored_tool`** — decorator that instruments a tool function
- **`BaselineEngine`** — learns and stores behavioral profiles
- **`DetectionEngine`** — evaluates rules and anomaly scores
- **`ResponseExecutor`** — enforces severity-based actions
- **`SurfaceMapper`** — enumerates agent capabilities

---

## Evaluation Targets

| Metric | Target |
|---|---|
| True Positive Rate | ≥ 85% |
| False Positive Rate | ≤ 5% |
| Per-action overhead | ≤ 50 ms |
| Throughput | ≥ 500 actions/sec |
| Baseline stability | Variance < 5% |

Results from the six benchmark scenarios are published in `benchmark/results/`.

---

## Standards Alignment

- **OWASP LLM Top 10 (2025)** — LLM01, LLM02, LLM05, LLM06, LLM08, LLM10
- **MITRE ATLAS** — AML.T0051, AML.T0057, AML.T0029
- **NIST AI Agent Standards Initiative (2026)** — agent identity, authorization, prompt injection as identity boundary attack

---

## Threat Model

Itisri assumes:

1. The LLM is untrusted. Its outputs may be manipulated.
2. External content is untrusted. It may contain adversarial instructions.
3. The agent's tools are trusted but over-permissioned.
4. Behavioral baselines are learnable.
5. The attacker can observe the agent's output but not the internal baseline model.

Full analysis in `THREAT_MODEL.md`.

---

## Roadmap

- [x] Project skeleton and core event schema
- [x] Instrumentation layer with `@monitored_tool`
- [x] Demo agent and benchmark scaffolding
- [ ] Baseline engine (Isolation Forest + Markov)
- [ ] Detection engine (rules + anomaly scoring)
- [ ] Response executor
- [ ] Attack surface mapper
- [ ] Six benchmark scenarios with full attack payloads
- [ ] CLI and HTML reporting
- [ ] LangGraph middleware adapter
- [ ] ChromaDB memory hooks
- [ ] Qdrant adapter (production vector store)
- [ ] Multi-agent coordination detection

---

## Contributing

See `docs/contributing.md`. Issues and pull requests are welcome.

---

## License

MIT — see `LICENSE`.

---

## Citation

If you use Itisri in academic work, cite:

```bibtex
@misc{aditya2026itisri,
  title  = {Itisri: A Runtime Detection and Response Engine for Agentic AI Security},
  author = {Sai Aditya},
  year   = {2026},
  note   = {CSE Graduate, ANITS}
}
```

---

## Author

**Sai Aditya**
CSE Graduate, ANITS
GitHub: [@saiadityaprojects](https://github.com/saiadityaprojects)
