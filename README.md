# bottymcbotbot

A small assistant service that uses a local Ollama model for chat and function-calling tools.

This README explains how to install dependencies, use the included `Makefile`, and set up Ollama with the model used by this project (`gpt-oss:20b`).

## Requirements

- Python 3.12+
- pip (or a Python package manager that can read `pyproject.toml`)
- Ollama (local model runtime) — see the instructions below

## Install dependencies

This project uses `pyproject.toml`. You can install dependencies with pip, pipx, or a virtual environment.

Example using a virtual environment and pip:

```bash
python -m venv .venv
source .venv/bin/activate  # on WSL / Linux
python -m pip install --upgrade pip
pip install -e .
# Install test/dev dependencies
pip install -r <(python - <<'PY'
import tomllib, sys
p = tomllib.loads(open('pyproject.toml','rb').read())
reqs = []
for g in ('dev','test'):
    if f"dependency-groups" in p and g in p['dependency-groups']:
        reqs.extend(p['dependency-groups'][g])
print('\n'.join(reqs))
PY
)
```

Alternatively, install directly from `pyproject.toml` using `pip` (PEP 621+ support may vary):

```bash
pip install -r requirements.txt  # if you generate one, or
pip install .
```

Recommended minimal dependencies from `pyproject.toml`:

- fastapi
- uvicorn
- wireup
- ollama
- openai

## Makefile

This repo includes a `Makefile` to simplify common tasks. Typical targets you may find useful:

- `make run` — start the application (usually runs uvicorn)
- `make test` — run the test suite
- `make lint` — run linters/type checkers

To see available targets, run:

```bash
make help
```

(If your environment is WSL, run `make` from the WSL shell.)

## Setting up Ollama

Ollama is used as a local LLM runtime. This project expects an Ollama daemon listening on `http://localhost:11434` and uses the `gpt-oss:20b` model by default.

1. Install Ollama — follow instructions at https://ollama.com/. On Linux/WSL you can install via the provided package or using their installation script.

2. Start the Ollama daemon:

```bash
ollama daemon
```

3. Pull/download the model used by this project (example name):

```bash
ollama pull gpt-oss:20b
```

Confirm the model is available:

```bash
ollama list
```

The project is configured to use `gpt-oss:20b`. If you prefer a different model, update the Ollama model setting in `src/libs/chat/ollama/client.py` or provide a configuration for `OllamaAISettings`.

## Configuration

- Default Ollama base URL: `http://localhost:11434/`
- Default model: `gpt-oss:20b` (configured in `src/libs/chat/ollama/client.py` via `OllamaAISettings`)

You can override these values via the dependency injection container or by editing `src/libs/chat/ollama/client.py`.

## Running the app

Assuming dependencies are installed and Ollama is running with `gpt-oss:20b`:

```bash
# from the project root
uvicorn src.main:app --reload
```

or use the Makefile target (if provided):

```bash
make run
```

## Tests

Run tests with:

```bash
pytest -q
```

## Notes

- This project relies on local Ollama models. Ensure you have disk space and network access to pull models.
- The codebase uses `wireup` for dependency injection; configuration is done via service classes in `src/libs/chat/ollama/client.py`.
- If you encounter issues contacting the Ollama daemon, ensure it's running and that the `base_url` matches the daemon address.

If you'd like, I can:
- Add a `requirements.txt` or `dev-requirements.txt` generated from `pyproject.toml`.
- Add a small script `scripts/setup_ollama.sh` to automate pulling the model and starting the daemon.
- Add Makefile targets for `pull-model` and `start-ollama`.

Which would you like next?
