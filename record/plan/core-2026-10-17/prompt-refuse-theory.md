# Brief: certification.lth states the conjunction route and the witness of `refuse`

Before the tag (Luciano, 2026-10-22). report-bite-13b.md leaves one place where the code says more
than its theory: bite 13c's items 3 and 4 (report-bite-13c.md and its follow-up) gave certify.py a
conjunction route (a demand resolved to its subject and obligations, the vetoes read once on every
subject, the direct veto scoped by reach with the refuted-consequence exception, D-2026-10-22-a and
-d) and a witness (one entry per obligation, used by admission, the run's record and the result
key). `certification.lth` and `certification_model.lut` don't state them.

Read `CLAUDE.md`, then `report-bite-13c.md` (with both follow-ups), `report-bite-13b.md` (its
section on 13c's addition), spec 6.S15 and 7.S22, `record/decisions.md` at D-2026-10-22-a and -d,
and `certification.lth`, `certification_model.lut`, `tests/tester/certification_*.test.lut`, and
`certify.py`'s `veto`, `witness`, `_about`, `_passes_theory`.

State in certification.lth the route and the witness as laws over the theory's `refuse` (or a new
theory beside it, if that reads better), give certification_model.lut the reference model that
follows certify.py, and add law lines and controls (a wrong model for each: a route that skips a
veto, a witness that drops an obligation, a veto not scoped by reach, a consequence refuted on a
model that passes the defining laws but not treated as refuting all). Each law graded and each
control refuted. Compare the model against certify.py on the cases of tests/test_certify.py that
exercise these paths, and say where they agree.

Run with `/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`;
scratch under ~/.cache/luthier-refuse/. Touch only certification.lth, certification_model.lut,
tests/tester/certification_*.test.lut and their stores. Re-certify the certification programs
twice (second pass 0 lines ran). Small commits staged by path: subject, blank line, one body line,
ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>".

Accepted when: `luthier check` clean on the three files; the second certify pass at 0 lines ran;
`python -m pytest -q tests/test_certify.py tests/test_tester.py` passes; core_metrics' counts not
up. Report: append a section "Before the tag: refuse's route and witness" to report-bite-13b.md,
committed: the laws, the controls, the agreement with certify.py, decisions taken on your own.
