# CLAUDE.md — expense-api

## Stack
Python 3.12 · FastAPI · in-memory store · pytest · uv.

## Conventions
- Type-hint everything. Run `ruff check` first.
- Tests live in `tests/`; one file per module.
- No `print` in lib code — use `logging`.

## Commands
- Run:   `uv run uvicorn app.main:app --reload`
- Test:  `uv run pytest -q`
- Lint:  `uv run ruff check .`

## Do not touch
- `.env`, `uv.lock` (use `uv add`), `.claude/hooks/`.
