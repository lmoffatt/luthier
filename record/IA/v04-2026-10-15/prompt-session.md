# v0.4 criterion (b): `luthier session` as 2.S18 and 12.S20 read it, brief for an Opus agent

Read `CLAUDE.md`, step 6.3 of the execution plan (criterion b), 2.S18 in `docs/spec/02-grammar.md`
(a session is a block; what it allows and reports: 2.R6 unused rebinding reported, not refused),
12.S20 in `docs/spec/12-files-and-tools.md`, 12.S19 (eval, the probe), 4.R12, O8 in
`docs/principles.md`, and `src/luthier/cli.py`, `run.py` (`Probe`, `Loaded`, `evaluate`: eval's
report `record/IA/v04-2026-10-15/report.md`). Write `luthier session [files]`: a read-eval loop
over stdin where each line is an item of a block (`x := e`, `p <- e`, a term), the files and
their imports loaded as eval does, each term printed with its type and the cone's states as eval
prints them, the session's own definitions visible to later lines, an unused rebinding reported
(2.R6), nothing recorded (as eval), and an action on the world (`w <- print w "x"`) run with the
session's token and its first-action validation as `run` does (say whether 12.S20 asks for it;
if the spec is silent, the conservative reading: actions allowed only with a flag, [proposed]).
Change cli.py, run.py, tests/test_session.py (new); the Python uncommitted; fix 12.S20's
"[implemented]" wording to what is true after, one commit of the chapter alone. Report with a
shell heredoc to `report-session.md` here, committed alone. Accepted when: the suite passes;
`printf 'x := 3\nx + 1\n' | PYTHONPATH=src python3 -m luthier.cli session` prints `4 : Int` and
the states line; `check_spec.py` prints nothing.
