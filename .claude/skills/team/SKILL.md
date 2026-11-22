---
name: team
description: Build a task with a planner that branches into a fixer and a test-writer
  working in parallel, then verify, review, write a run report and wait for the user.
disable-model-invocation: true
argument-hint: [task description]
---

# Team build

Task: $ARGUMENTS

You are the orchestrator. Subagents cannot start other subagents or talk to each
other, so you start every agent and pass each report on yourself, verbatim.
Do not write or fix the code or the tests yourself.

```
            planner            (+ verifier baseline, at the same time)
           ┌───┴────┐
        fixer    test-writer   (at the same time; app/ and tests/)
           └───┬────┘
           verifier
               │
           reviewer
```

Tell the user, in Turkish, what each stage returned before you start the next one.

## Steps

1. **Plan** — start `planner` with the task and `verifier` (baseline) in the same
   message so they run in parallel. Both are read-only.
   - Planner STATUS is NEEDS_CLARIFICATION: ask the user its questions and stop.
   - Baseline is FAIL or BLOCKED: tell the user and ask whether to continue.
2. **Build (round 1)** — start these two in the same message so they run in parallel:
   - `fixer` with the CONTRACT and the APP_BRIEF. Tell it: change files under
     `app/` only, write no tests, and expect new tests to appear under `tests/`
     that it must not edit.
   - `test-writer` with the CONTRACT and the TEST_BRIEF.
3. **Verify** — run `verifier`.
   - FAIL or BLOCKED: go to "Repair round" with this report.
   - PASS: continue.
4. **Review** — run `reviewer` with the task and the CONTRACT.
   - `hold`: go to "Repair round" with this report.
   - `ship` or `ship with nits`: go to "Finish".

### Repair round (round 2)

There are at most **2 rounds** per run: the parallel build, then one repair.

- If the repair round has not been used: run a single `fixer` with the CONTRACT
  and the failing report, both verbatim. Tell it the contract is the source of
  truth: fix whichever side deviates from it, under `app/` or `tests/`, and never
  weaken a test just to make it pass. Then return to step 3.
- If the repair round is already used: stop. The outcome is `hold`. Go to "Finish".

## Finish

1. Write the report to `reports/team/<YYYY-MM-DD-HHMM>-<short-task-slug>.md` using
   the template below. Write it in Turkish. List every agent run in the order it
   happened, including failed runs, and mark which runs were parallel.
2. Tell the user, in Turkish: the joint outcome, what changed and why, any nits,
   and what you need them to decide. Link the report file.
3. **Stop and wait.** Do not commit until the user approves. Never push or merge.
   When you do commit, follow the commit rules in the user's CLAUDE.md.

## Report template

```markdown
# Team raporu: <görev>

- **Tarih:** <YYYY-MM-DD HH:MM>
- **Ortak karar:** ship | ship with nits | hold
- **Kullanılan tur:** <1 ya da 2> / 2

## Ağaç

<Koşan ajanları dallanmayı gösterecek şekilde çiz; her birinin yanına sonucunu yaz.>

## Koşan ajanlar

| # | Aşama | Ajan | Model | Paralel mi | Ne yaptı | Sonuç |
|---|-------|------|-------|------------|----------|-------|
| 1 | Plan | planner | sonnet | evet (verifier ile) | ... | READY |

## Sözleşme

<Planner'ın CONTRACT bölümü, değiştirmeden.>

## Ajan raporları

<Her ajanın döndürdüğü bloğu, sırasıyla ve değiştirmeden buraya koy.>

## Değişen dosyalar

- `<yol>` — <ne değişti, neden> — <hangi ajan>

## Ortak kararın gerekçesi

<Verifier ve reviewer sonuçlarını birleştiren 2-4 cümle.>

## Kullanıcıdan beklenen kararlar

- <örn. commit atılsın mı, nit'ler düzeltilsin mi>
```
