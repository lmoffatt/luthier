# luthier test, bite 3: a binding names a generator, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). The evidence report
(`record/IA/evidence-2026-10-14/report.md`, "Laws that need a generator" and "The tester", not
fixed 5): a binding names only a census, never a generator, so the laws over symmetric and
orthogonal matrices, unit lists, calibrated uniform samples and clear diagonals run on listed
cases only (grade `cases`) where 7.R1 lets a test name its generators.

## The prompt

Read `CLAUDE.md` first, then that report's two sections, `docs/spec/07-tests.md` 7.R1, 7.S1,
7.S5, 7.S9 (a generator as a functor with its parameters or a name with its fingerprint, in
the entry's identity), `src/luthier/lib/generators.lth` (`Gen`, `Binding`, `resolve`, `Random`,
`Support`, `Filter`, the sized generators, what a binding can hold), `generators_model.lut`,
`test.lth` §1 (`test`'s `where` and `profile`), `src/luthier/tester.py` (`prepare`, the bindings,
`draw_base`, `new_entry`'s binding expanded) and `src/luthier/arrays.py` (`gen_symmetric` and
other generators kept from v0.1). Another Opus writes `plot.lth`, `plot_model.lut`: touch
neither. Change `src/luthier/tester.py`, `tests/test_tester.py`, programs under `tests/tester/`,
`src/luthier/lib/generators_model.lut` only to add a generator as a model value with its route
(one commit by its path, [proposed], message ending "Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>"), and `tests/tester/arrays_laws.lut`, `probability_laws.lut` to use them.

1. A `where`/`profile` binding may name a generator: a value of `Gen T` defined in Luthier
   (generators.lth's forms) or a host generator declared as an extern `(size : Nat) -> Seed ->
   T * Seed` (v0.1's `gen_symmetric(rng, size)` style, through the bridge: say how the seed
   crosses and comes back, 7.S1). The tester draws the parameter from it at the spec's size and
   seed; the entry's binding records the generator as 7.S9 says (a name with its fingerprint:
   the hash of its cone); coverage `Drawn`.
2. Generators for: symmetric matrices of a given size (`gen_symmetric`), orthogonal ones (QR
   of a Gaussian, or Householder; 7.S5's family), unit lists (`List (Vec Float64)` of unit
   vectors), a calibrated uniform sample, a diagonal with an atom at 0; as model values in
   `generators_model.lut` with routes to `src/luthier/arrays.py` or a new `generators.py`
   (host code, P7) if arrays.py is not the place; each with the law its model must meet
   (symmetric: `s == transpose s`; orthogonal: `transpose q * q == identity` within a tolerance
   parameter; unit: norm 1 within tolerance; uniform: by `UniformAtLevel` at a Level).
3. `arrays_laws.lut` and `probability_laws.lut`: the listed-case lines of the pinv, rank and
   Kolmogorov laws gain a sampled twin bound to the generator (keep the listed ones); run them
   (`luthier test FILE --no-cert`, minutes, background) and paste the lines: the grade should
   be `sampled` now; a refuted law is a finding for its author.

Check: `PYTHONPATH=src python3 -m pytest tests/test_tester.py tests/test_run.py -q`, then the
suite. Do not commit the Python or the test programs' stores (the coordinator does); commit
the `.lut` files you change, each alone. Report in your final message.
