#!/bin/bash
[ "$(jq -r '.stop_hook_active')" = "true" ] && exit 0
[ -z "$(git status --porcelain -- '*.py')" ] && exit 0
uv run pytest -q >&2 || exit 2
