# Brief: chapter 11, Numbers

Read `record/spec-briefs/common.md` and `record/spec-brief-template.md` first.

## Goal

Write `docs/spec/11-numbers.md`, chapter 11 of the specification: the ideal and its realizations,
the primitive number types, the axioms, the variance of function types, the bridge with the host
for numbers and arrays, the rounding law. The old file `docs/spec/06-numbers.md` is your main
source and stays in place; the integrator deletes it.

## Sources

- `docs/spec/06-numbers.md` at d12b554, whole. §0 is cited from `spec 1`, not restated.
- `docs/principles.md`: L13 (the ideal world is realized with a guarantee), in particular L13.3
  and L13.4 (rounding is non-expansive up to an additive defect of about ε|x|; the functor reading
  stands with "non-expansive plus an additive term"), L12 (laws combine; `Cost`), L3 (equality).
- `tests/spec/n1_numbers.accept.lut` to `n5_arrays.accept.lut` and the reject programs among them
  for the rules' files; `src/luthier/lib/rational.lut` for the rounding law as stated in Luthier;
  `src/luthier/rational.py`, `arrays.py` (read only) for what is implemented.

## What changes against the source

- Each item a rule or a statement with status. The types (§2), the axioms (§3), the variance (§5),
  the bridge (§6), the arrays (§7) are `[implemented]` where the interpreter does them (the source
  says what was implemented on 2026-10-05); the generic definitions through a number model (§4 and
  the end of §7) are `[proposed]`, as the source says "not yet".
- L13.3 and L13.4 enter as statements `[proposed]` (D-2026-10-12-y: the rounding correction stays
  reversible, nothing about epsilon fixed), with the rounding law of §8 as their worked instance
  and with the additive defect and the condition number named as parameters, never constants.
- "Two refinements are open" (§4) and §9 become citations: intervals or balls and the two levels
  of number theory cite O1 (the algebra of costs) and O5 (decorated outputs: the error by
  intervals); randomness cites `spec 7`.
- Where the source speaks of tolerances as constants (`roundingSlack`, `...Agrees` with a
  tolerance), say that the cutoff is the demand's (D-2026-10-12-h) and the law returns the measured
  cost, citing `spec 5` and `spec 6`; mark `[proposed]` what this changes in the libraries.
- L14: `lib/rational.lut` already states the rounding law in Luthier; name it, and name
  `lib/number_model.lut` for the generic definitions through a number model, `[proposed]`.
- `## Open`: O1, O5.

## Length

The source is about 2000 words; the chapter should be about that.
