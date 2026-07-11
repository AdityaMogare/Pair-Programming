# Pair-Programming Debug Gym

Practice debugging like production: broken code on the default branch, solutions in open Pull Requests.

## How it works

1. **Pick an exercise** folder below.
2. **Run its tests** — they fail on purpose.
3. **Fix the bugs** locally (change one thing at a time).
4. **Check your work** (or get unstuck) via the matching open PR → **Files changed**.

> **Do not merge solution PRs.** They stay open forever as the answer key.

## Exercises

| Folder | Status | Topic |
|--------|--------|--------|
| [`01-anomaly-detector/`](01-anomaly-detector/) | Ready | Flag suspicious cloud events (boundary, nulls, inverted logic, thresholds) |
| [`02-telemetry-pipeline/`](02-telemetry-pipeline/) | Coming soon | Structured logging / pipeline transforms |
| [`03-agent-observability/`](03-agent-observability/) | Coming soon | Stream metrics and alert thresholds |

## Workflow (Git + PR model)

```text
master (or main)     ← starting line: intentionally buggy code
  └── solution/01-anomaly-detector   ← fixed version (open PR, never merge)
  └── solution/02-telemetry-pipeline ← (when ready)
```

### For learners

```bash
git clone https://github.com/AdityaMogare/Pair-Programming.git
cd Pair-Programming
cd 01-anomaly-detector
python3 test_detector.py
```

When stuck or done: open the repo on GitHub → **Pull requests** → find `solution/01-anomaly-detector` → read **Files changed**.

### For maintainers (adding a new exercise)

```bash
git checkout master
# add 0N-your-exercise/ with buggy code + tests + README
git add 0N-your-exercise && git commit -m "Add 0N-your-exercise (buggy starting line)"
git push origin master

git checkout -b solution/0N-your-exercise
# fix bugs only inside 0N-your-exercise/
git add 0N-your-exercise && git commit -m "solution: fix 0N-your-exercise"
git push -u origin solution/0N-your-exercise
gh pr create --base master --title "solution: 0N-your-exercise" --body "Answer key — leave open, do not merge."
```

## Tech

Python 3 stdlib only. No packages to install.
