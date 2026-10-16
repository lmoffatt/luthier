# Brief: provisional externs refused by default, and the modes of running as fields of the demand

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-16-c and D-2026-10-16-d (and
D-2026-10-15-c, L5.20: every behavior has a way to be said; D-2026-10-15-g: fuel only cuts),
`src/luthier/lib/world.lth` (`applied`, `provisional`), `src/luthier/lib/demand.lth` (`Demand`,
`DEMAND_DEFAULTS`' counterpart in demand_model.lut `theDemand`), `src/luthier/lib/plan.lth`
(`TheDefaultsAgree`, the strategies), `src/luthier/run.py` and `src/luthier/cli.py` (`run`'s flags,
`--accept`, `--fuel`, `--fresh` from step 3a), `docs/spec/08-demand.md` 8.S1, 8.S3, 8.S4,
`docs/spec/06-certification.md` 6.S14, `docs/spec/10-world.md` 10.S10, 10.S12.

Build:
1. Provisional (D-2026-10-16-c): world.lth's `applied` refuses a provisional extern as run does; a
   demand runs one as assumed only when it names it: `--accept assumed:NAME` (repeatable), the grade
   `assumed` propagating downstream; a bare `--accept assumed` no longer accepts provisionals.
   `provisional` carries its reason (a string the declaration gives); every run that applies one
   warns on stderr naming it and its reason; `luthier check -v` lists the provisionals with reasons.
2. Modes as fields of `Demand` (D-2026-10-16-d), each set by a flag of run with its default declared
   in demand_model.lut and recorded: `strategy` (forward on demand the default; run.py's call by need
   is the specimen that computes it, held to `TheDefaultsAgree`; say in the record which ran),
   `fuel` (none by default for run; `--fuel N` in steps; a new `--time-limit SECONDS`), `fresh`
   (from step 3a's argument to a field). certify keeps its budget unchanged.
3. Spec: update the clauses above to what is now implemented (status `[implemented]` only for what
   you did and tested); 8.S1's list of the demand's fields.
Tests: a provisional refused without naming; accepted with `assumed:NAME`, its grade assumed in the
record and a warning on stderr; a bare `--accept assumed` refusing it (the control, L9.14); run with
no fuel bound finishing a program that needs more than the old 10,000,000 steps; `--time-limit`
stopping a loop and saying so; the strategy and fresh recorded in the demand.

Accepted when: `python -m pytest -q` passes in full (the count before plus your tests);
`python3 scripts/check_spec.py` prints its one known finding (03-kernel.md:190) and the counts;
`python3 scripts/project_principles.py --check` ok; `luthier check -v` lists provisionals. Small
two-line commits ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", staged by
path; another agent commits at the same time in certify.py and tester.py (do not touch those),
retry on .git/index.lock. Report: `record/IA/code-follows-2026-10-16/report-modes.md` by shell
heredoc, committed: what you built, the checks' output, decisions taken on your own, at most one
question.
