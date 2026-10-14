# arrays.lth after the evidence: PinvRestricts' domain, the tolerance scaled by the conditioning

Written 2026-10-14 by the coordinating session (luthier-3e). On the evidence report
(`record/IA/evidence-2026-10-14/report.md`, "Findings"): two laws of arrays.lth refuted; the
author (a Fable agent of the day) is not around; by Luciano's word the agents state the fix,
marked [proposed], one commit each to undo.

## The prompt

Read `CLAUDE.md` first, then that report's "Findings" and the `Pinv*` rows of its table, then
`src/luthier/lib/arrays.lth` at `pinvSym`, `PinvRestricts`, `PinvProjects`, `PinvSymmetric`,
`PinvScales`, `Symmetric`, `RankFloor`, `approxMatSlack`, and `docs/spec/11-*.md` 11.S14, 11.S18
(a sum compared relative to the magnitudes it adds; tolerances as measured costs),
D-2026-10-14-c (`record/decisions.md`, end). Another agent edits `src/luthier/*.py` and `tests/`:
change only `src/luthier/lib/arrays.lth` and `tests/tester/arrays_laws.lut`.

1. `PinvRestricts` is false on an indefinite matrix: `pinvSym` keeps the eigenvalues above
   `floor × max|w|`, so the negative ones are dropped and `s p s` differs from `s` by the
   negative part. State it over the positive semidefinite matrices (a subtype `PositiveSemidefinite`
   of `Symmetric`, by the predicate the file can state: every quadratic form `v^T s v >= 0` on a
   listed basis is not enough; use what the leaf gives, `retainedRank` of `s` equal to that of
   `s` with its negative part removed, or state the slack as the dropped part's norm), citing
   11.S18; say which reading you took and why, [proposed].
2. `PinvProjects`, `PinvSymmetric`, `PinvScales` fail on Hilbert 5 by rounding of order
   `cond × eps` against a flat `tol`: scale the comparison as `DotAgrees` does (relative to the
   magnitudes compared: `|p| × |s| × eps`-like, or the condition number read from the retained
   spectrum), with the tolerance still a parameter of the law (D-2026-10-14-c), citing 11.S14.
3. `tests/tester/arrays_laws.lut`: the listed matrices stay; add the PSD subtype's cases where
   the law moved; the refuted lines should now pass. Run `PYTHONPATH=src python3 -m luthier.cli
   test tests/tester/arrays_laws.lut --fuel 100000000` (minutes; background) and paste the lines
   of the four laws before and after.
`arrays.lth` must parse and `luthier check` clean. Commit each file alone (`git add` its path;
never `-A` or `.`), messages naming the laws and 11.S14/11.S18, ending with "Co-Authored-By:
Claude Sonnet 5.5 <noreply@anthropic.com>". Report in your final message.
