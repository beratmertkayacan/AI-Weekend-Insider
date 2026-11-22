---
name: pipeline
description: Run a task through the verifier, fixer and reviewer subagents, then
  write a run report and wait for the user's decision.
disable-model-invocation: true
argument-hint: [task description]
---

# Pipeline

Task: $ARGUMENTS

You are the orchestrator. Subagents cannot talk to each other, so you pass each
report to the next agent yourself. Run the agents one at a time, never in parallel.
Do not write or fix the code yourself; that is the fixer's job.

If the task is empty or too vague to judge when it is done, ask the user before
starting.

## Steps

1. **Baseline** — run `verifier`. Keep its report.
2. **Build** — run `fixer` with the task and the baseline report, pasted verbatim.
   This is round 1.
3. **Verify** — run `verifier` again.
   - FAIL or BLOCKED: go to "Another round" with this verifier report.
   - PASS: continue.
4. **Review** — run `reviewer` with the task.
   - `hold`: go to "Another round" with this reviewer report.
   - `ship` or `ship with nits`: continue to "Finish".

### Another round

There are at most **2 rounds** (2 fixer runs) per pipeline run.

- If round 2 has not been used: run `fixer` again with the task and the failing
  report pasted verbatim, then return to step 3.
- If round 2 is already used: stop. The outcome is `hold`. Go to "Finish".

## Finish

1. Write the report to `reports/pipeline/<YYYY-MM-DD-HHMM>-<short-task-slug>.md`
   using the template below. Write it in Turkish. List every agent run in the
   order it happened, including runs that failed.
2. Tell the user, in Turkish: the joint outcome, what changed and why, any nits,
   and what you need them to decide. Link the report file.
3. **Stop and wait.** Do not commit until the user approves. Never push or merge.
   When you do commit, follow the commit rules in the user's CLAUDE.md.

## Report template

```markdown
# Pipeline raporu: <görev>

- **Tarih:** <YYYY-MM-DD HH:MM>
- **Ortak karar:** ship | ship with nits | hold
- **Kullanılan tur:** <1 ya da 2> / 2

## Koşan ajanlar

| # | Ajan | Model | Ne yaptı | Sonuç | Sonraki adım |
|---|------|-------|----------|-------|--------------|
| 1 | verifier | haiku | ... | PASS/FAIL | ... |

## Ajan raporları

<Her ajanın döndürdüğü bloğu, sırasıyla ve değiştirmeden buraya koy.>

## Değişen dosyalar

- `<yol>` — <ne değişti, neden>

## Ortak kararın gerekçesi

<Verifier ve reviewer sonuçlarını birleştiren 2-4 cümle.>

## Kullanıcıdan beklenen kararlar

- <örn. commit atılsın mı, nit'ler düzeltilsin mi>
```
