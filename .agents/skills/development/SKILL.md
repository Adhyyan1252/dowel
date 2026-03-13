# Dowel Development

Python logger for ML research. Source in `src/dowel/`, tests in `tests/dowel/`.

## Commands

```sh
# Setup
pip install -e .[all,dev]

# Pre-commit hooks
pre-commit install -t pre-commit
pre-commit install -t pre-push
pre-commit install -t commit-msg

# Test
pytest --cov=dowel

# Lint
flake8

# Format
yapf -ipr src/ tests/

# Docs
cd docs && make html
```

## Style

- Single-quoted strings, Google-style docstrings, Google import order
- `__init__` documented in class docstring (D107 ignored)
- Tests exempt from docstring checks
