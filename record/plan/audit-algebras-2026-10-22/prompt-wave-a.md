# Brief: wave A of the audit's execution, in three agents

`execution.md` beside this file plans wave A (no question of Luciano's). A1 and A8 are done
(03723fa, b395a05, ac2c7b8). The rest goes to three agents at once, split by files so they don't
collide:

- Agent 1 (Opus): A4, A5, A6, in that order. Files: certify.py, certification.lth,
  certification_model.lut, their test programs, tests/test_certify.py.
- Agent 2 (Sonnet): A2, A7. Files: run.py, demand.lth, plan.lth, their models and test programs,
  tests/test_run.py.
- Agent 3 (Opus): A3, then A9. Files: tester.py, laws.lth, laws_model.lut, elaborate.py, check.py,
  their test programs, tests/test_tester.py, tests/test_elaborate.py, tests/test_check.py.

Each agent: read `CLAUDE.md`, `execution.md` (your bites, their sources and acceptance criteria),
`decisions.md` for context (its five questions are Luciano's and unanswered: don't act on them),
and the audit sections each bite cites. Each bite with a test that fails before and passes after,
committed as it passes. Touch only your files; if a bite needs another agent's file, say so in your
report and leave it. Don't re-certify the stores: the coordinator runs one wave after the three
finish. Run your test files with `/home/lmoffatt/miniconda3/bin/python -m pytest -q`; a failure
left must be a stale store (name it) or not yours (show it fails the same at the commit before your
first). `python scripts/check_spec.py` prints only its known finding. Scratch under
~/.cache/luthier-wave-a/<agent>/, not /tmp; long runs waited for in the foreground with bounded
waits. Small commits staged by path: subject, blank line, one body line, ending with
"Co-Authored-By: Claude <Opus 5.5 or Sonnet 5.5> <noreply@anthropic.com>".

Report: `report-wave-a-<agent number>.md` beside this file, committed (not execution.md, which
the three would edit at once; the coordinator marks the bites done there): per bite what you did,
the commits, the checks, decisions taken on your own, at most one question. If your Write is
refused for it, give its full text in your final message.
