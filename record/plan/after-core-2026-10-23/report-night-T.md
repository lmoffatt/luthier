# Report of night agent T: typed comparisons, a name capture in `solve`, `==` on injections

2026-10-26, Claude Opus 5.5, on the coordinator's brief for agent T. Base commit 842b7e4. Sources: report-wave-a-3.md (A9, untyped comparisons), report-wave-a-3b.md ("For others", the capture), report-B2.md (the stuck `==` on `Extended`). Committed by the coordinator from the agent's hand-back (its Write was refused). Commits: b0a03ea, bea8798, 61fce45, 444973f, 35a0921, e262418, 20cac89. Files: elaborate.py, kernel.py, tests/test_elaborate.py, tests/test_check.py, tests/test_kernel.py, docs/spec/03-kernel.md, 04-static-semantics.md, tests/tester/arrays_controls.test.lut, generators_model.lut. Scratch under ~/.cache/luthier-night/T/. Nothing certified.

## 1. Comparisons are typed (444973f)

`==`, `/=`, `<`, `<=`, `>`, `>=` go through `comparison` in elaborate.py: the right operand is walked at the left operand's type, and the two types must fit one way or the other (`fits` and `plain`, as `operator_use` does for `+`). A mismatch is refused with 4.R9 ("x == "a": == compares two values of one type, but x has type Int and "a" has type String"). Skipped when a type is unknown or the operands are types; `implies` unchanged. An integer literal (or a negated one) compared with a `Float64` elaborates as the `Float64` it denotes, on either side (`x < 0` is `x < 0.0`): needed beyond checking, since the kernel's `_primitive` compares constants of one type only, so `x < 0` at `Float64` was stuck at run time before. A float literal against an `Int` is refused. Tests: test_check.py `test_a_comparison_of_two_types_is_refused`, test_elaborate.py `test_a_comparison_types_its_operands_and_an_integer_literal_takes_float64`, both failing on 842b7e4. Spec: a sentence in 4.R9, marked proposed (e262418). `+` does not take an integer literal at Float64 (`x + 0` is refused): the question.

## 2. The name capture in `solve` (bea8798, 35a0921)

Two captures. `solve` returned early on `pattern == actual`, so a claim's `List A` against a caller's `List A` matched without solving `A`, and `model_of` said the model depends on `A`; the `if actual != pattern` guard dropped the same case one level down. Now an equal pattern naming a binder is walked, and a binder is recorded even when its solution is the name it shares. Second: `instantiate`, `model_of`, `claim_matches` and `sibling_subtype` substituted one name after another, so `h (A B : Concrete) (p : B * A) : B := first p` got `pairs A A` and was refused; `substitute_all` replaces the names at once, renaming through fresh `k%n` names only when a value names another key. Tests in test_check.py and test_elaborate.py fail on 842b7e4 and pass after. `pickFrom` has its parameter `A` again (its canonical body hashes the same).

## 3. `==` on injections (b0a03ea, 20cac89)

A label whose part is `Unit` had arity 0, so `infiniteDistance unit` (how core.lut writes it) was no value and `==` didn't step; now such a label is a value bare or applied to one part, and `_equal` zips the parts: `finiteDistance 0.0 == infiniteDistance unit` steps to false, `infiniteDistance unit == infiniteDistance` to true (test_kernel.py `test_equality_on_a_unit_label_applied_to_unit`). With `same (a b : Extended) : Bool := a == b`, `luthier eval` printed the stuck term on 842b7e4 and prints `false` now. The bare expression at `luthier eval` stays stuck: the probe's program has no sum to read labels from (`Extended` is an alias; `runtime_slice` follows no label to it); the fix is run.py's (the probe keeping a definition of each sum whose labels the term names). Next to it: a `match` read the two writings of a Unit label as different shapes (`match r { stopA u -> 1 ; _ -> 2 }` on a bare `stopA` gave 2); the kernel's `PCon` reads it bare or applied on either side (20cac89, with its test). Spec: a sentence in 3.S17, proposed.

## Files newly refused and fixed

`luthier check` over the 122 `.lth`/`.lut` files, on 842b7e4 and the final commit: item 1 newly refused tests/tester/arrays_controls.test.lut at `valueOneVecFunctor` and `valueOneMatFunctor` (their maps compared an entry of the type parameter `A` with `1`). Replaced with maps that reverse the entries, `reversedVecFunctor` and `reversedMatFunctor` (61fce45), which break `map id` too, so each line is refuted at `MapId` first; on a copy holding only those two lines both conjuncts are refuted (`MapCompose` gives (-10, 2) against (2, -10) on the sentinel (5, -1)). Item 2 refused nothing new. At the current HEAD all files check clean.

## Cones expected to move

Compared the canonical elaborated body of every definition before and after, in check's typing (122 files) and the tester's runtime program (54 test programs): only arrays_controls' two MapCompose controls moved. Item 1 moved no term (the tree writes `0.0`); item 2 moved nothing (only `pickFrom`'s annotation, erased by the hash). The kernel changes move no cone, but can change outcomes where `==` met a Unit label applied to `unit` (structural equality of `Extended`, `StopReason`, the reasons in resources.lth): the re-certification will show any.

## Checks

test_elaborate.py, test_check.py, test_kernel.py: 251 passed before the match fix; test_kernel.py 76 passed after. test_spec.py, test_lists.py, test_core_structures.py: 103 passed, 7 xfailed. `check_spec.py`: its known finding.

## Decisions taken on my own

1. The integer literal takes `Float64` only in comparisons, as a literal or a negated literal; arithmetic unchanged.
2. The comparison's fit is symmetric, skipped when a type is unknown or the operands are types; `implies` not checked.
3. The capture fixed in `solve` and by substituting all names at once.
4. MapCompose's two controls became reversals, renamed.
5. `pickFrom`'s parameter is `A` again.
6. The match fix for Unit labels beside the `==` fix.
7. run.py's slice left alone.
8. Both spec sentences proposed.

## Question

Comparisons read `x < 0` at `Float64` as `x < 0.0`, while `x + 0` at `Float64` is still refused (4.R9). Should arithmetic also read an integer literal at the other operand's numeric type, or should comparisons refuse it as `+` does?

Coordinator's answer (2026-10-26): the first, uniformly. An integer literal takes the other operand's numeric type in arithmetic as in comparisons, as Haskell reads a literal through `fromInteger` (L7.6: Haskell's manner where it fits); it moves no cone today. Logged as D-2026-10-26-a; Luciano told; one commit undoes it.
