# The laws the controls showed too weak (L9.14), brief for an Opus agent

Read `CLAUDE.md`, L9.14, then `report-mutants.md` in this folder ("Uncontrolled, with why" and
"Findings"). Strengthen, each `[proposed]`, one commit per file by path:
1. numbers.lth `LessIsStrict`: it cannot see `less := a <= b` because the sampler draws no ties:
   quantify over a pair with a tie (a subtype or a generator with an atom at equality) so the
   `<=` model is refuted; its control in numbers_controls.lut becomes that model.
2. arrays.lth `RankScales`: holds on an absolute floor of 1e-3; state it so a wrong floor is
   refuted (the floor relative to the magnitude, as the pinv laws are since 6157fbc).
3. generators.lth's non-statistical laws that name their family in the body: take the family
   as a parameter so a broken family can be passed, and let generators_controls.lut's wrapper
   laws become ordinary control lines of those laws.
4. probability.lth `GaussianPeaksAtMean`, `ProfiledIsGaussianAtItsSigma`: take the construction
   as a parameter (the model is `gaussian`), so a wrong construction is a control.
Change only those theory files, their models and the matching `_laws.lut`/`_controls.lut`
(another agent edits probability_laws.lut, probability_controls.lut, generators_laws.lut and
generators_controls.lut for the statistical laws: coordinate by editing only the non-statistical
lines and committing each file right after you change it). Report with a shell heredoc to
`report-weak-laws.md` here, committed alone. Accepted when: every changed file parses and checks
clean; `luthier certify` on the changed `_laws.lut` and `_controls.lut` (with stores, background)
lists the four groups controlled and none CONTROL FAILED; the suite passes.
