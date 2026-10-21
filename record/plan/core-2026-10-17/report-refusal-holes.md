# The holes in the core-name refusal: report

2026-10-21, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-refusal-holes.md` of this folder (findings 1, 2a to 2d of `review-bite-5.md`; D-2026-10-18-b, spec 12.S22). Started at b1bd4e5; bites 10 and 11 committed beside it. Committed by the coordinator from the agent's hand-back (the agent's Write was refused for report files).

## Commits

- a3aa45f finding 1. `redefinitions` (run.py) exempts a name only when the file itself is listed for it in CORE_COLLISIONS; the clause that exempted it when any other file was listed is gone. Tests in test_check.py and test_run.py put a core entry in CORE_COLLISIONS (monkeypatched) and show a file outside the core defining `Reflexive` is refused, naming core/properties/relations.lth. The entries themselves are untouched.
- a37136b findings 2a to 2c. 2a: elaborate.py's `bind_operator` refuses (TypingError, rule 12.S22) an `operator` act outside the core that binds a core operator to another function at the type of the core's binding, naming the core file (`_core_operator_file`); the loader does the same through `operator_rebindings` (run.py), since a run's slice keeps no `operator` act and `eval` of `5 + 2` with `operator + := intMinus` gave 7. 2b and 2c: run.py's `binds` gives a file's top-level names (`_defines`, each label of a sum it writes, each name an import binds with `as`); check.py's `core_refusals` uses it and `Loaded` refuses `f.defined | f.labels | f.aliased`. test_elaborate.py's `test_ActsKept` bound `+` at `Int -> Int -> Int`, now refused; it binds one at `Bool`, its point unchanged.
- 2fc0b50 finding 2d, the coordinator's decision: 12.S22 lists the names refused and says a record's field, a parameter and a pattern variable stay free, since D-2026-10-18-b is about top-level names; a test checks fields `map` and `compose`, a parameter and a pattern variable `compose`.

Every new test failed on a copy of the tree without the three source changes and passes with them, but the 2d test, which passed before too.

## Checks

pytest of test_check, test_elaborate, test_run: 7 failed, 292 passed, 3 skipped, 2 xfailed. Each failure fails the same way without my changes: test_infer_is_total_on_the_library (generators_model.lut's `Symmetric * Seed` names no model of `*`); six arrays/numpy run tests (stale stores of arrays_model's numpy: AddPointwise, SubPointwise, ScalePointwise; bite 11's files).

check_spec.py: only its known finding (03-kernel.md:192). `luthier check` over the 58 files of lib and examples: four refused, three by other rules before my change (distances.lut 4.R9, experiment_zero 4.R2, generators_model.lut 4.R13), one new.

## Files newly refused

src/luthier/lib/term_model.lut: the label `Selected` of `ArmStep` (line 385) is core/structures/universal.lth's alias `Selected`. Not exempted. Through it the loader refuses certification_model.lut, certification_laws.test.lut and certification_controls.test.lut. It's bite 10's file, untouched.

## Decisions taken on my own

A rebinding is another function at the core binding's whole declared type; the same function is a no-op, another type an overload (arrays_model's `* := scale` stays). Labels come from every sum a file writes; the core's own labels are not core names. An `as` equal to the name is not refused. The loader's operator check runs only with lib/core and reads a file's acts alone in the core's context; an operator bound to an imported function is left to `check`.

## Not probed

The elaborator keys operator bindings on the first operand's type alone: arrays_model's `* := scale` and `* := mscale` sit at `Float64`, beside the core's `floatTimes`.

## Question

Should bite 10 rename term_model.lut's label `Selected` (say `ArmSelected`), or should a label be a name apart from core definitions?

Coordinator's answer (2026-10-21): rename. A sum's label is also its injection (`r : S := unit 3`), a top-level name like any other, so it stays under the refusal.
