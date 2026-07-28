# Pair-Programming Debug Gym v2

Practice debugging backend systems like production incidents.

## Core idea

* The default branch (`master`) contains intentionally broken code.
* Each exercise folder is a self-contained incident.
* The solution lives in an **open PR** and is **never merged**.
* Learners fix the bug locally, then compare with the PR answer key (**Files changed**).

## How to play

```bash
git clone https://github.com/AdityaMogare/Pair-Programming.git
cd Pair-Programming
cd 01-anomaly-detector   # or another ready exercise
python3 test_detector.py
```

1. Read the exercise `README.md` (scenario + expected vs broken).
2. Run the tests — they fail on purpose.
3. Use `logs/`, `fixtures/`, and `sample_requests/` like an on-call kit.
4. Fix one bug at a time in `app.py`.
5. Stuck or done → open the matching `solution/0N-…` PR → **Files changed**.

> **Do not merge solution PRs.** They are the answer key.

## Exercises

| Folder | Level | Topic | Status |
|--------|-------|-------|--------|
| [`01-anomaly-detector/`](01-anomaly-detector/) | 1 | Local logic / anomaly rules | **Ready** |
| [`02-telemetry-pipeline/`](02-telemetry-pipeline/) | 2 | Structured logging & transforms | Scaffold |
| [`03-cache-invalidation/`](03-cache-invalidation/) | 3 | Redis cache consistency | Scaffold |
| [`04-payment-transaction/`](04-payment-transaction/) | 3 | Money & idempotency | **Ready** |
| [`05-rate-limiter/`](05-rate-limiter/) | 2 | Request throttling | Scaffold |
| [`06-background-jobs/`](06-background-jobs/) | 3 | Queue workers | Scaffold |
| [`07-auth-session-expiry/`](07-auth-session-expiry/) | 2 | Sessions & tokens | Scaffold |
| [`08-search-index-sync/`](08-search-index-sync/) | 3 | Search eventual consistency | Scaffold |
| [`09-webhook-delivery/`](09-webhook-delivery/) | 3 | Outbound integrations | Scaffold |
| [`10-concurrency-race/`](10-concurrency-race/) | 4 | Race conditions | Scaffold |
| [`11-observability-gap/`](11-observability-gap/) | 4 | Incomplete signals | Scaffold |
| [`12-config-deployment/`](12-config-deployment/) | 4 | Env & release drift | Scaffold |

### Difficulty progression

| Level | Focus | Examples |
|-------|--------|----------|
| **1** | Local logic | nulls, boundaries, off-by-one |
| **2** | API + data | validation, SQL-ish mistakes, status codes |
| **3** | State + async | cache, queues, retries, duplicates |
| **4** | Production incidents | concurrency, partial failure, observability, config |

## Exercise template

Every folder follows the same pattern:

```text
0N-exercise-name/
├── README.md           # incident brief
├── app.py              # buggy service entrypoint
├── test_*.py           # failing regression tests
├── fixtures/           # payloads, seed data, expected outputs
├── logs/               # app / SQL / worker / gateway logs
├── sample_requests/    # example HTTP bodies
└── notes.md            # learner scratchpad
```

### README sections (standard)

* Scenario
* Expected behavior
* Broken behavior
* Run
* Hints
* Success criteria

## Open PR answer key format

```text
master                         ← buggy starting line
 └── solution/01-anomaly-detector   ← fixed (open PR, never merge)
 └── solution/02-telemetry-pipeline ← when authored
```

Each solution PR should include:

* the fixed code only (prefer a small, reviewable diff)
* a short root-cause summary
* a tiny “why this happened” note
* **no merge into master**

Example PR body:

```md
Root cause: cache keys were built with the wrong user ID, which caused stale reads across sessions.

Fix:
- corrected cache key generation
- added coverage for user-specific cache isolation
- kept behavior unchanged elsewhere
```

### Maintainer: add a new exercise

```bash
git checkout master
# author 0N-name/ with buggy app.py + tests + logs + fixtures
git add 0N-name && git commit -m "Add 0N-name (buggy starting line)"
git push origin master

git checkout -b solution/0N-name
# fix bugs only inside 0N-name/
git add 0N-name && git commit -m "solution: fix 0N-name"
git push -u origin solution/0N-name
gh pr create --base master --title "solution: 0N-name (answer key — do not merge)"
```

## Tech

Python 3 stdlib only for authored exercises. No packages required to start.

## Realism checklist

Each ready exercise should feel like an on-call ticket:

* user / ops report
* logs
* failing test
* one or two subtle bugs
* believable root cause
* clean answer-key PR
