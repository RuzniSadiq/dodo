# MEMORY.md — shared agent memory

**Read this early** in any coding, review, or merge session.
**Update it** when the same failure class appears twice (prefer a test/sensor
over a long essay).

### Dual-write rule (mandatory)

Whenever an agent writes durable operational memory in a local runtime store,
**also write here**.

### No CI loop for memory-only updates

Commits that touch **only** this file skip the green gate. Mixed memory +
product code still uses the normal gate.

_Last updated: 2026-10-31_

---

## Operating notes

| Topic | Rule |
|-------|------|
| Claims | Draft PR body `- Active-work claim: <slug>` via Gibson `claim.sh` |
| Green gate | See `AGENTS.md` / `.agents/gate.json` |
| Deploy | None; `main` is the release branch |

---

## Lessons (append-only)

## 2026-10-31 — adoption-seed

- Repo adopted Gibson agent-memory conventions (AGENTS memory block + this file).
- Pure memory commits skip the product green gate; dual-write is mandatory.

## 2026-10-31 — pytest-test-integrity

- **What happened:** Gibson's test-integrity sensor only parses
  Vitest/Jest/node:test output, so pytest counts were invisible to it.
- **Fix / rule:** `tests/conftest.py` prints
  `GIBSON_TEST_METRICS total=N skipped=M todo=0`. Never remove it.
