# luthier test, bite 3: a binding names a generator, report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-3.md; saved by the coordinator.
Commits by the agent: 23968d5 generators_model.lut (the families `symmetric`, `symmetricOf k`,
`gram` (PSD), `orthogonal k` (Haar, QR of a Gaussian), `unitList`, `uniformSample`,
`clearDiagonal`, each with the law its values meet, the atom probabilities and bounds as
arguments, P11), 67aabca probability_laws.lut, ed7e5f4 arrays_laws.lut (sampled twins of the
listed lines). Committed by the coordinator with this report: `src/luthier/tester.py`,
`src/luthier/generators.py` (new host code, P7), `tests/test_tester.py` (3 tests),
`tests/tester/generators_laws.lut` (the generators' own seven laws, sampled 100, none refuted).

tester.py: a binding's name is a generator when its definition's type unfolds to `Nat -> Seed ->
T * Seed` (Luthier or a host extern), else a census; a family `(k : Dim) -> Gen T` is applied to
the law's earlier parameters by binder name (7.S7); the seed threads through each draw (7.S1;
the host seeds `random.Random` and draws the next seed last); every drawn value is checked
against the parameter's type (a value outside makes the line NotRun naming the generator);
coverage `Drawn`; the entry records `"<name> [reads] (generator, size N)"` with the generator's
cone hash and host routes (7.S9).

Runs (fuel 1e8, seed 20261014): arrays_laws.lut 18.5 min, the pinv and rank twins all
`sampled` 100 but `PinvRestricts`, refuted 2/100 on full-rank PSD matrices from `gram`
(condition 4.6e4 and 3.4e3: `approxMatSlack` compares with a flat `tol (1 + |a| + |b|)`, an
entry near 0 carries rounding of cond × eps × |s|: needs the magnitude-scaled `approxMatOf` its
siblings use, for arrays.lth's author); the listed lines all pass; probability_laws.lut §5
lines: the Kolmogorov laws and UniformAtLevel sampled 100 (0 refuting cases where about 1 is
expected at alpha 0.01: the tester does not estimate a level yet, 7.S17).

Findings: check.py's 4.R5 refuses a standalone `x : T := extern "..."` when `T` is imported
(the externs put in one record `hostGenerators`; every family's cone then includes every
route); run.py's Runner gets stuck on a constant whose body is a partial application of an
extern applied to the remaining arguments (worked around with lambdas); the brief's "unit: norm
1" was wrong (`UnitList` is entries in [0, 1]).

Decisions of the agent: a generator under ExhaustiveMode is NotRun; a generator's file is not a
store home; the `gram` family and the ClearDiagonal twins added; twins at size 10.
