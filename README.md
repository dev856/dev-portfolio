# Dev Portfolio

Streamlit portfolio app managed with `uv`.

## Setup

```powershell
uv sync
```

This project is pinned to Python 3.13 through `.python-version` because the
current pinned `pyarrow` wheel is not available for Python 3.14.

For better disk reuse on Windows when the default `uv` cache is on a different
drive than this repo, this repository includes `uv.toml` so `uv` keeps its cache
in `.uv-cache/` and hardlinks packages into `.venv/`.

```powershell
uv sync
```

## Run

```powershell
uv run streamlit run Home.py
```

The virtual environment is created in `.venv/` and is ignored by git.
