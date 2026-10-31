# AGENTS.md — dodo

## Autonomous development contract

This repo is developed by both humans and coding agents. Any agent or harness
working here reads this section first and obeys it. It states repo facts, not
process doctrine — your harness (The Gibson) supplies the process.

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
mypy --strict src              # typecheck
ruff check .                   # lint
pytest -q                      # test (prints GIBSON_TEST_METRICS for test-integrity)
python -m compileall -q src    # build
```
All of these must pass before any **product** commit, with **zero new failures
versus the branch point**. Run them via Gibson's `scripts/gate.sh`.

### Ground rules for machine contributors
1. **Never mutate the shared checkout.** One task = one branch = one git
   worktree of your own.
2. **Claim before you touch.** One `- Active-work claim: <slug>` line in an
   open draft PR body (created by Gibson `scripts/claim.sh`), plus the
   `agent-claimed` label. Overlapping claim ⇒ stop and coordinate.
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

### Framework warnings
- Python ≥ 3.10, standard library only. Do not add runtime dependencies.
- Gibson's test-integrity sensor does not parse pytest output natively;
  `tests/conftest.py` emits `GIBSON_TEST_METRICS`. Keep it.

### Deployment truth (verified 2026-10-31)
- No hosted deployment. Distribution is `pip install .` from `main`.
- Production branch: `main`.

### Stop and ask a human for
- Changes to `.agents/gate.json`, `tests/conftest.py`, or CI workflows
- Deleting or migrating a user's task file format
- Publishing to PyPI, secrets, legal commitments

### Commit and PR conventions
- `git commit -s` (DCO sign-off) on every commit.
- Branch name: `<issue>-<slug>`. PR body carries `Closes #<issue>`.
