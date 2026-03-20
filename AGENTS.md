# AGENTS.md

## Cursor Cloud specific instructions

**dowel** is a Python logging library for ML research. It is a single-package library (not a web app or monorepo) with no external service dependencies.

### Key commands

- **Install**: `pip install -e ".[all,dev]"` (editable install with all extras + dev tools)
- **Lint**: `flake8` (configured in `setup.cfg`)
- **Test**: `pytest --cov=dowel` (runs 53 tests across 4 workers with coverage)
- **Docs**: `cd docs && make html`
- **Example**: `python examples/log_progress.py`

### Gotchas

- **flake8 version**: The `setup.cfg` uses inline comments in config values (e.g. `extend-ignore = D107  # ...`) which are not supported by flake8 >= 6.0. The update script pins `flake8<6.0.0` to maintain compatibility. If you see a `ValueError` about error codes not matching, ensure flake8 < 6 is installed.
- **PATH**: pip installs scripts to `~/.local/bin` which may not be on `PATH` by default. The update script adds it. If `flake8` or `pytest` are not found, run `export PATH="$HOME/.local/bin:$PATH"`.
- **TensorFlow warnings**: TF logs about CUDA/oneDNN during tests are expected and harmless (no GPU in the VM).
