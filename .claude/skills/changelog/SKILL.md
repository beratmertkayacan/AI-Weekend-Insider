---
name: changelog
description: Draft release notes from recent commits on the current branch.
disable-model-invocation: true
argument-hint: [number-of-commits]
---

# Changelog

Run: git log -n $ARGUMENTS --pretty=format:'%h %s' --no-merges

Group commits by Added / Changed / Fixed / Removed.
Drop dependency bumps and chore commits.
End each bullet with its short SHA.
