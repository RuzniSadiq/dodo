# AGENTS.md — dodo

## Autonomous development contract

This repo is developed by both humans and coding agents. Any agent or harness
working here reads this section first and obeys it. It states repo facts, not
process doctrine. The process lives in `bin/gibson` → `.claude/skills/ship/`.

Machine-readable companion: `.agents/gate.json` (same commands, parseable).

### Shared agent memory

- **Read** root `MEMORY.md` at session start before mutating work.
- **Dual-write:** durable lessons go in `MEMORY.md`, not only in a local
  runtime store.
- **No CI loop for pure memory commits:** if a commit touches **only**
  `MEMORY.md`, do **not** run the gate and do **not** wait on review. Mixed
  memory + product code uses the normal green gate.
- **Append-only**; rebase immediately before writing; on conflict keep both
  sides. No secrets in memory files.

### Gate commands (the definition of "green" here)
```bash
uv run mypy --strict src              # typecheck
uv run ruff check .                   # lint
uv run pytest -q                      # test (prints GIBSON_TEST_METRICS for test-integrity)
uv run python -m compileall -q src    # build
```
All of these must pass before any **product** commit, with **zero new failures
versus the branch point**. Run them via `bin/gate` (`bin/gate --baseline` at
branch point; it also fails if the test total drops or skips rise).

### Ground rules for machine contributors
1. **Never mutate the shared checkout.** One task = one branch = one git
   worktree of your own.
2. **Claim before you touch.** Add the `agent-claimed` label to the issue.
   Already claimed ⇒ stop and coordinate.
3. **Never review or approve your own work.** An independent reviewer —
   ideally a different model — inspects the exact committed head, read-only.
4. **Acceptance criteria are the contract**, verified by a test, never by
   assertion.
5. **Report failures verbatim.** Never mark done what you did not verify.
6. **Clean up:** remove the worktree, delete the branch, release the claim.

### Hot files (single claimant, own PR)
| File | Rule |
|---|---|
| pyproject.toml | no casual deps; own commit |
| .agents/gate.json | gate changes need human review |
| tests/conftest.py | owns test-integrity metrics; never weaken |
| MEMORY.md | append-only lessons; pure updates skip CI |

### Risk tiers (merge policy)
| Tier | Scope | Merge |
|---|---|---|
| A | output formatting, tests, docs, isolated helpers | auto when gate green + review approves |
| B | new commands/flags, behaviour changes, new *optional* task-file fields | auto only if ≤150 lines, no hot files, review has zero findings; else human |
| C | breaking/migrating task file, hot files, `bin/`, `.claude/` | always human |

Kill switch: `touch .gibson-halt` stops the loop before its next step.

### Framework warnings
- Python ≥ 3.10, standard library only. Do not add runtime dependencies.
- `bin/gate` reads `GIBSON_TEST_METRICS` emitted by `tests/conftest.py`. Keep it.

### Deployment truth (verified 2026-10-31)
- No hosted deployment. Distribution is `pip install .` from `main`.
- Production branch: `main`.

### Stop and ask a human for
- Changes to `.agents/gate.json`, `tests/conftest.py`, `bin/`, or `.claude/`
- Deleting or migrating a user's task file format
- Publishing to PyPI, secrets, legal commitments

### Commit and PR conventions
- `git commit -s` (DCO sign-off) on every commit.
- Branch name: `<issue>-<slug>`. PR body carries `Closes #<issue>`.
