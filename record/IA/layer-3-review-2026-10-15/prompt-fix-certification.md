# certification.lth after round 1: the grade by the fold, subtypes instead of coinciding strings, a current failure refuses

Written 2026-10-15 by the coordinating session (luthier-3e). Items 2 and 4 of `summary.md`'s top
screen in this folder, and C1, C3, C5, C7, C10 of its certification.lth section: read them there
(and the replies they cite under `A/` only where the summary quotes a counterexample).

## The prompt

Read `CLAUDE.md`, then `summary.md` (the top screen and the certification.lth section),
`src/luthier/lib/certification.lth` whole and `certification_model.lut`, D-2026-10-14-c. Change
those two files only, one commit each by path ("Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>"); every law stays Boolean with its cutoffs as parameters; the report
through the shell (the Write tool refuses report files) to `report-fix-certification.md` in this
folder, committed alone.

1. C1 (item 2): the grade determined for every certificate: a law per step of the fold (adding
   one current pass to any certificate gives the weakest or strongest as §2's reading says), or
   `grade` defined in the theory; the model follows.
2. C3 (item 2): the laws that guard their consequent with `e.law == c.law`, `not (k.serves d e)`
   and the like quantified over the subtypes (`ServedEntry k d`, `CurrentFailure c`,
   `CurrentPass c`, an entry of the certificate's law) instead of premises two random strings
   rarely meet (7.S12, L9.6).
3. C5 (item 4): a law with a current failure is refused whatever serves (`RefusalSaysWhy`,
   `Certified`), and the model.
4. C7 (an entry's grade tied to its evidence and its reach to its cases), C10 ("the latest in
   front" as a law), and the "Roles:" pointer on `Value` (C8).
5. Leave as questions for Luciano, untouched: C2 (`record` on a known identity) and C4 (budgets
   in the identity).
Accepted when: both files parse and `luthier check` clean; `PYTHONPATH=src python3 -m pytest
tests/test_certify.py tests/test_run.py -q` passes (certify.py may need to follow C5: if a test
of run's refusal must change, say exactly which and why, and leave the Python to the
coordinator); the report lists per item the law changed and quotes it.
