---
name: house-review
description: Use when the user asks to review a diff, a pull request, or a staged change.
---

# Code review — house rules

1. Start with the **risk surface** — auth, money, data deletion, network calls.
2. Group comments by file. For each, cite `path/to/file.py:42`.
3. Prefer suggesting a patch over describing the issue.
4. Flag any new dependency. We don't add libraries lightly.
5. End with a one-line verdict: **ship**, **ship with nits**, or **hold**.
