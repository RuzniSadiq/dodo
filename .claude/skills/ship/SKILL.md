---
name: ship
description: Minimal Gibson loop. Turn a plain-English feature into tiered issues, then claim, build, gate, review, merge and clean up each one without stopping except at the approval points below.
argument-hint: "<feature in plain English>"
disable-model-invocation: true
---

Feature request: $ARGUMENTS

You are the orchestrator (in the main checkout `$ROOT` = repo root). Read `AGENTS.md` and `MEMORY.md` once. Be terse: no narration between steps, one status line per step.

**Halt check:** before every step, if `$ROOT/.gibson-halt` exists, stop and report where you are.

## Tiers (from AGENTS.md)
- **A**: output formatting, tests, docs, isolated helpers.
- **B**: new commands/flags, behaviour changes, new *optional* task-file fields.
- **C**: breaking/migrating the task file format, `pyproject.toml`, `.agents/gate.json`, `tests/conftest.py`, `bin/`, `.claude/`.

## 1. Plan
Split the request into the fewest independently-mergeable issues (each ≤ ~150 changed lines). For each: title, tier, acceptance criteria (each one checkable by a named test), files likely touched, dependency order.
- All A → proceed without asking.
- Any B or C → show the plan once with AskUserQuestion (approve / edit / cancel). This approval covers the plan, not C merges.

Create issues in order: `gh issue create --title ... --label gibson,tier-X --body "<criteria>"`.

## 2–7. For each issue, sequentially
2. **Claim**: `gh issue edit N --add-label agent-claimed` (if it already has the label, skip it and report). Create the worktree: `git -C $ROOT worktree add -b N-<slug> $ROOT/../dodo-N main`, then run `bin/gate --baseline` inside it.
3. **Build**: Agent tool, `model: sonnet`. Prompt: the worktree's absolute path (work only there), the issue body, "follow AGENTS.md; write the failing tests first, then code; stdlib only; run `bin/gate` until GATE GREEN; commit with `git commit -s` ending in `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`; do not push; reply with ≤5 lines: what changed + gate result."
4. **Gate**: run `bin/gate` in the worktree yourself. Never trust the builder's claim.
5. **Review**: Agent tool, `model: haiku` for A, `model: opus` for B/C, read-only (tell it: do not edit). Give it only the acceptance criteria and the output of `git -C <wt> diff main...HEAD`. Ask for: `VERDICT: approve|changes` + numbered findings (bug, missing test for a criterion, hot-file touch, scope creep).
   - `changes` → send the findings to a new builder agent, then repeat steps 4–5. After 2 failed rounds → stop and ask the owner.
6. **Merge**: `git -C <wt> push -u origin HEAD`, then `gh pr create --head N-<slug> --title ... --body "Closes #N\n\n<summary>\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)" --label tier-X`.
   - **A**: merge if gate is green and the reviewer approved.
   - **B**: auto-merge only if diff ≤ 150 lines AND no hot files AND the reviewer approved with zero findings. Otherwise AskUserQuestion with the diff stat and the findings.
   - **C**: always AskUserQuestion, showing the diff stat, review and risk.
   - Merge: `gh pr merge N-<slug> --squash --delete-branch`, then `git -C $ROOT pull -q`. Later issues branch from the updated main.
7. **Cleanup**: `git -C $ROOT worktree remove <wt>`, `git -C $ROOT branch -D N-<slug>` (ignore if gone), `gh issue edit N --remove-label agent-claimed`. If a failure class repeated, append a one-line lesson to MEMORY.md in the *next* issue's branch (or report it at the end).

## Stop only for
Plan approval (B/C), a B merge that fails the auto rule, any C merge, 2 failed review rounds, a gate red that the builder cannot fix in 2 attempts, an overlapping claim, or halt. On any stop: say exactly what failed (verbatim output) and what you need.

## Finish
One summary table: issue | tier | PR | merged? | notes. Nothing else.
