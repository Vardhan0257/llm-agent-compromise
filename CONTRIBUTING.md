Contributing to AgentCompromiseLab

Thanks for your interest in contributing — small, focused contributions are most helpful.

How to contribute

- Issues: file a clear bug or enhancement in GitHub Issues with reproduction steps and expected behavior.
- Code: open a pull request against `main`. Keep changes small and focused. Use feature branches named `feat/<short-desc>` or `fix/<short-desc>`.
- Tests: add or update unit tests in `tests/` for any behavior you change. CI runs `pytest`.
- Experiments: add datasets or experiment scripts under `scripts/` and write a short note in `REPORT.md` describing the experiment parameters.

Repository style

- Python: follow PEP8; prefer explicit typing where useful. Keep functions small and well-documented.
- Logging: use the existing `logging` configuration and prefer structured messages when adding experiment traces.

Running locally

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run tests:

```powershell
pytest -q
```

3. Reproduce experiments:

```powershell
python scripts/train_validator.py
python scripts/run_bypass_experiments.py
python scripts/plot_results.py
```

Code of conduct

Be respectful and constructive. This repository is for defensive research and educational use only. Don't use it to target real systems or people.

Maintainers

- The project maintainers are the repository owners. Open PRs and assign or request review as needed.
