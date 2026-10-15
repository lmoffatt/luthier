# Every law of the slice refutes a wrong model (L9.14, D-2026-10-15-a): the control lines

Read `CLAUDE.md`, L9.14 in `docs/principles.md`, `report-tester.md` in this folder (how a control
line is written and reported), `tests/tester/tables_controls.lut` as the pattern, and the five
counterexamples the B/C/D fixes already refuted (`record/IA/layer-3-review-2026-10-15/
report-fix-BCD.md`: the give-up maximizer, `phi := pt - 1`, even-iteration acceptance, `score :=
0`, `info := -I`). Another agent rewrites the statistical laws (laws.lth, generators.lth,
probability.lth's `UniformAtLevel`): skip those, and touch no theory file.

1. For each law certified by `tests/tester/{arrays,numbers,probability,belief,optimization,fit,
   tables,world,plot,generators}_laws.lut` (non-statistical), write a control line in a sibling
   `*_controls.lut`: the law on one model broken on purpose (a wrong leaf, an off-by-one, a
   zero, a swapped sign; the five above where they fit), expected refuted. Sonnet-level work per
   file; you may split it across files as you go. A law for which no wrong model can be built
   without a new definition gets a line in the report saying why.
2. Small follow-ups: bind `budget` in belief_laws.lut and fit_laws.lut's cutoffs (50, as the
   fix agent's probe); delete the leftover `Failed: t = holeT` entry from
   `tests/tester/tables_laws.cert.json` (an ignored, derived store) and refresh both tables
   stores with `luthier certify`; the stale docstrings in run.py naming `PassedDownNotRecomputed`,
   `RecordsEveryCutoff`, `Runs`.
3. Run `luthier certify` on every `*_laws.lut` and `*_controls.lut` (background, --jobs 2,
   --fuel 100000000; about 40 minutes) and paste the per-law status lines grouped as controlled,
   uncontrolled (with why), CONTROL FAILED (a law too weak: name the law and the model; do not
   fix the theory, it is a finding).
Commit the .lut files (each alone, by path) and run.py; your report with a shell heredoc to
`report-mutants.md` here, committed alone. Accepted when: the suite passes; the status listing
pasted; no `CONTROL FAILED` left unexplained.
