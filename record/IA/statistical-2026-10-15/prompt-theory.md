# The statistical law's form (D-2026-10-15-b, L9.15), the theory side, brief for a Fable agent

Read `CLAUDE.md`, then L9.14 and L9.15 in `docs/principles.md`, D-2026-10-15-a and -b at the end
of `record/decisions.md`, 7.S17 to 7.S19 in `docs/spec/07-tests.md` as rewritten today, item 3
of `record/IA/layer-3-review-2026-10-15/summary-BCD.md` (the C section behind it), then
`src/luthier/lib/laws.lth` (§1 verdicts, §3 evidence), `generators.lth` (`Random`, `Level`,
`UniformAtLevel`), `probability.lth` (`UniformAtLevel`, `uniformPValue`) and their models.

Write the form: a statistical verdict `Holds | Fails | Unresolved` carrying its error rates
(alpha, beta, the samples spent); a statistical law as a theory of its statistic and its
alternative at distance delta, its value under a sequential test with alpha, beta, delta, the
initial size and the budget as parameters the demand supplies (D-2026-10-14-c); the sequential
probability ratio test as a definition over a stream of samples (two thresholds, sample more in
between, unresolved when the budget runs out); `UniformAtLevel` and `Random`'s statistical laws
rewritten in this form, no law universal over seeds; each with a control (L9.14: a biased
source the test refutes, stated as a model broken on purpose). Change laws.lth, generators.lth,
generators_model.lut, probability.lth, probability_model.lut only (another agent edits test.lth,
tester.py, certify.py now: do not touch them), one commit per file by path ("Co-Authored-By:
Claude Fable 5.1 <noreply@anthropic.com>"), each `[proposed]` where the spec leaves a reading.
Report with a shell heredoc to `record/IA/statistical-2026-10-15/report-theory.md`, committed
alone, ending with what the tester must do (one line per definition) for the next bite.
Accepted when: every changed file parses and `luthier check` is clean; `luthier check` on the
importers (tests/tester/*_laws.lut, examples/sonolocalizacion/*.lut) still clean or the report
names what breaks; no Python changed.
