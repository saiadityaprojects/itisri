# Contributing

Issues and pull requests are welcome at
https://github.com/saiadityaprojects/itisri.

---

## Development Setup

Clone the repository and install in editable mode with development extras:

```bash
git clone https://github.com/saiadityaprojects/itisri.git
cd itisri
python -m venv .venv
source .venv/bin/activate     # Windows: .venv/Scripts/activate
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Run the demo agent:

```bash
python -m demo_agent.run
```

Run all six benchmark scenarios:

```bash
python -m benchmark.runner --all
```

---

## Project Structure

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

## Code Style

- **Line length:** 100 characters
- **Formatter:** `black`
- **Linter:** `ruff`
- **Type checker:** `mypy`

Run all three before submitting a pull request:

```bash
black .
ruff check .
mypy itisri
```

---

## Adding a Detection Rule

1. Create a new YAML file under `itisri/rules/` named after the rule ID:
   ```
   itisri/rules/ITI-TOOL-013.yaml
   ```

2. Use this template:

   ```yaml
   id: ITI-TOOL-013
   name: Short human-readable name
   severity: high          # low | medium | high | critical
   description: >
     One or two sentences explaining what this rule detects and why
     it matters.
   conditions:
     - field: action.tool_name
       operator: not_in
       value: ${baseline.allowed_tools}
   action: [block, alert, log]
   mitre_atlas: [AML.T0051]
   owasp: [LLM06]
   ```

3. Add a test case under `tests/test_detection.py` that exercises the rule.

4. Update the rule table in `README.md`.

---

## Adding a Benchmark Scenario

1. Create a directory under `benchmark/`:
   ```
   benchmark/07_new_attack/
   ```

2. Add an `attack.py` with a `scenario_NN_name()` function that returns a dict:

   ```python
   def scenario_07_new_attack() -> dict:
       return {
           "name": "07 — New Attack",
           "expected_detections": ["ITI-XXX-013"],
           "poison": {
               "tool": "target_tool",
               "args": {"param": "malicious_value"},
           },
       }
   ```

3. Register it in `benchmark/runner.py` under the `SCENARIOS` dict.

4. Add a test in `tests/test_benchmark.py` verifying the scenario runs end-to-end.

---

## Submitting Changes

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run `pytest` and ensure all tests pass
5. Run `black .`, `ruff check .`, and `mypy itisri`
6. Commit with a clear message:
   ```bash
   git commit -m "Add ITI-TOOL-013: detect non-allowlisted tool parameters"
   ```
7. Push and open a pull request

---

## Reporting Issues

When reporting a bug, include:

- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Full traceback if applicable

---

## Security Disclosures

If you discover a vulnerability in Itisri itself, please do not open a
public issue. Contact the maintainer directly via GitHub.

---

## License

By contributing, you agree that your contributions will be licensed under
the MIT License.
