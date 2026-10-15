# certification.lth knows the statistical evidence, brief for a Sonnet agent

Read `CLAUDE.md`, `report-tester.md` in this folder ("Findings" and "Decisions": `admits` does
not know `Tested`, so `heldAsRun` would refuse a statistical pass graded sampled; an unresolved
test is stored as `NotRunFor "unresolved at ..."` because certification.lth has no unresolved
outcome), laws.lth §4 (`StatisticalVerdict`, `Tested`, `StatisticalByTest`), and
`src/luthier/lib/certification.lth` §1-§2 with `certification_model.lut`.
State, `[proposed]`: `admits` accepts `Tested` evidence for the grade `StatisticalByTest` gives;
`Outcome` gains `Unresolved` carrying the rates and the spent (a not-run that is not a failure
and not a pass, no grade); the error rates of a passed statistical entry kept in the entry (the
price of its grade, D-2026-10-15-b). Change those two files only, one commit each by path
("Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"); report with a shell heredoc to
`report-certification.md` here, committed alone, ending with what certify.py must change (one
line each). Accepted when: both files parse and `luthier check` is clean, and the importers
(demand.lth, plan.lth, tests/tester/*.lut) still check clean.
