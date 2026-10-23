# Wave A, agent 3: bites A3 and A9

Claude Opus 5.5, 2026-10-23, on `prompt-wave-a.md` beside this file (f78d9ad) and `execution.md` (A3, A9). Base commit f78d9ad. Committed by the coordinator from the agent's hand-back (the agent's Write was refused for report files). Files touched: `src/luthier/tester.py`, `src/luthier/lib/laws.lth`, `src/luthier/lib/laws_model.lut`, `src/luthier/elaborate.py`, `src/luthier/check.py`, `tests/test_tester.py`, `tests/test_check.py`, `tests/tester/settling_laws.test.lut`, `tests/tester/settling_controls.test.lut` and a new test program, `tests/tester/vacuity.test.lut`. The machine rebooted during A9 (about 16:19); the only uncommitted work of the agent's at that point was the A9 edits, and they survived. Scratch work is under `~/.cache/luthier-wave-a/agent3/`.

## A3. Vacuity and the empty experiment (2ba09cf, 7e06717)

Sources: audit 12, "Vacuity, empty evidence and uncovered regions" (report.md, 5b1a05e); D-2026-10-16-m; 7.S12; L12.7.

- laws.lth: `Evidence` gets `Vacuous : Nat -> Evidence` (a run that evaluated `n` cases, none with every premise held), and `Settling` gets the law `VacuousIsUnsettled`. laws_model.lut settles it `Unsettled`. settling_laws.test.lut adds `Vacuous 3` to its evidences and a census for `n`; settling_controls.test.lut adds the control `vacuousSupports`. 2ba09cf.
- tester.py: `premises_of` reads the premises a law states in its body: `p -> q` (core's `implies`) and `if p then q else true` (with `q` other than the literal `false`, since `not p` has that form and states no premise), at the top of the body, under its lets, and through a law the body applies (unfolded, at most `UNFOLD = 8` steps). `judged` runs after `run_spec` and counts the cases where every premise held (`held`, written into the entry's `Points` evidence when the law states a premise). If no case held, the outcome is `Vacuous n`: not run with the count as its reason (D-2026-10-16-m), never graded, never served. A run that evaluated no case and raised none is an empty experiment, not run with its reason; the exception is an exhaustive run over an empty type (`EmptyIsInitial`, `x : Empty`, bite 13c item 5), which keeps its pass. An empty census was already refused before the run. 7e06717.
- tester.py: `load_program` roots core's `implies`. `p -> q` between Bools elaborates to it, but no name in the source writes it, so the slice dropped it and every such law gave "`implies ...`, not a Bool"; the bite's control `x < 0 -> x > 0` could not run before.
- `judged` sits outside `_drawing_code`, so `drawing_revision()` is unchanged (`sha256:6cd60eb7…` before and after): no sampled identity moves.

Checks. New tests in test_tester.py: the vacuous law by `then`, by `if ... else true` and through an applied law; a premise that holds in 49 of 100 cases stays graded and records the count; the empty sample not run; `x : Empty` under ExhaustiveMode keeps its pass; `premises_of` reads one premise per form. All three behaviour tests fail on the tester of 2ba09cf and pass after (before: the control gave "unsettled: the law gave implies ...", the `if` form passed as sampled, `cases <- 0` passed as sampled with 0 cases). The control `x < 0 -> x > 0` over `Nat` reads "not run: vacuous: no premise held in the 100 cases evaluated (D-2026-10-16-m)". The full `Settling` line passes without a store: 19 conjuncts, 13086 cases, graded cases; the `bVacuous` control is refuted. test_tester.py 27 passed, 1 skipped; test_tester_conjunction.py 4 passed. Stores untouched.

Tree scan (every test line of the 53 test programs whose law or conjunct states a premise in its body, run without a store): no law becomes vacuous or empty. The laws with such a premise are `RoundTrip` in tables (held 7 of 8; its control 2 of 2) and `MaximizerStationary` in belief (100 of 100, 1 of 1; its control 20 of 20). The stores hold exactly one pass over no case, `EmptyIsInitial` in core.cert.json, the exception. No stored entry asks `cases <- 0`.

Not claimed: a region with no case still caps the grade at Sampled (D-2026-10-16-j, L9.16); that cap is a policy label, not a statistical bound on that region (audit 12).

Left in other agents' files: certification.lth's `Outcome` has no `Vacuous` constructor (Agent 1's file): until it gets one, the entry's outcome is `NotRunFor` with the count as its reason and its evidence `{"Vacuous": n}`, which certify.py reads as a not-run. certify.py's `store_errors` does not refuse a stored pass over no case; the tester no longer writes one, and the only one stored is the exception. run.py's runtime slice drops `implies` too: `luthier eval` on `main : Bool := 1 < 0 -> true` prints `implies false true`, unreduced (Agent 2's file; the fix is the one tester.py's `load_program` makes).

## A9. The kinds of a hole (6bc0772)

Sources: audit 12, "O9: holes"; O9; L2.1 to L2.4; record/plan/core-2026-10-17/decisions.md (the `x + "a"` finding).

- Verification: `x + "a"` no longer passes `check`; since the core's bite 4 it is refused with "4.R9 f: x + "a": + at Int (intPlus) takes Int, but "a" has type String". A test pins it. Residual finding: comparisons are not typed, so `g (x : Int) : Bool := x == "a"` still passes `check`; `==`, `<` and the other comparisons elaborate to the kernel's symbol without a fit check. Fixing it means walking the right operand at the left operand's type, which changes how numeric literals elaborate (`x < 0` with `x : Float64`) and moves cones: a typing bite of its own, not done here.
- elaborate.py: `solve` takes `strict`. Under it an inference unknown in the actual type agrees only with a variable of the pattern, never with a type the pattern names. Claim selection (`claim_matches`, `fill_structure`) and operator binding (`operator_binding`) use it. Before, `nil : List ?A` chose the one claim at `List Int`, taking the unknown as evidence that the model was the type's; now the type is asked for ("… ?A1 is not known, so no claim is chosen by it: annotate it"). A claim generic in the element still resolves. `fits` and `refines` let an unknown agree, as before: they compare bases and record no premise as discharged (a subtype's predicate is owed where the value crosses, 4.R9, 4.R11).
- elaborate.py: `HOLE_KINDS`, `hole_kind` and `hole_kinds` read each hole's kind from the elaborated act: `unknown` (`Hole('?x')`), `parameter` (a value declared with no body), `operation` (a function declared with no body: pending), `axiom` (a Bool or `Law` declared with no body that a conjunction claims, L2.2), `type` (declared at `U` or a record, 4.S8), `external` (an extern body, L2.4). Dead code is the demand's to decide, not the elaborated form's. `check -v` prints one `hole` line per hole, with its kind and what the demand does with it.

Checks. New tests in test_check.py: each kind reported (`Codec`, declared then defined, is no hole); the unknown kind; an unknown chooses no claim while an annotated argument and a generic claim still resolve; `x + "a"` refused. The first three fail on 7e06717 and pass after; the fourth passes on both. `luthier check` over all 283 `.lth`/`.lut` files with the elaborator of 7e06717 and with the new one: identical output for every file, so no elaborated term and no cone moves. test_check.py 100 passed, test_elaborate.py 69 passed; `python scripts/check_spec.py` prints only its known finding.

## Decisions taken on my own

1. `Vacuous n` is an `Evidence` constructor of laws.lth, not a `NotRun` reason: it keeps material truth and missing evidence apart by form, as the audit proposes. The entry's outcome stays `NotRunFor` with the count, since certification.lth's `Outcome` is Agent 1's.
2. The premise forms are `->` and `if p then q else true` (with `q` other than `false`), at the top, under lets and through applied laws, up to 8 unfoldings; `q or not p` is not read as a premise (the question).
3. The empty experiment is refused by the tester; the exception for an empty type is general (any exhaustive run that enumerates an empty type whole).
4. Vacuity is judged after `run_spec`, outside the hashed drawing code, so no identity moves.
5. The tester roots core's `implies`.
6. The `held` count is written into an entry only when the law states a premise.
7. A hole's kind is computed from the elaborated act, not stored in `t.Declare` (the kernel's dataclass, hashed by every cone).
8. A Bool-valued declaration is an axiom when a conjunction claims it, an operation otherwise.
9. Strict selection covers operator bindings as well as claims.
10. The untyped comparisons are left as a finding.

## Question

Should `q or not p` count as the premise `p`? The core states antisymmetry and injectivity that way (`o.eq x y or not (r x y and r y x)`, `oA.eq x y or not (oB.eq (f x) (f y))`). Read as premises, they make these lines vacuous: `StringIsOrdered` and `FloatIsOrdered` (Antisymmetric) and `IntIsAMetric` (MetricIndiscernible) in core_laws; `Doubles`' Antisymmetric at two lines of numbers_laws; `MarkIsAMetric` in docs/concepts/tape.test.lut; and the matching controls, in 31 of the 53 test programs (scan results in `~/.cache/luthier-wave-a/agent3/scan/or.jsonl`). Each passes today without one case where its antecedent held. Yes is a one-function change (`_premise_split`), and those certificates would become not-run until their generators draw equal pairs.

Coordinator's answer (2026-10-23): yes, in the same bite as generators that draw the antecedent (related pairs), so that the reading lands together with lines that can meet it and no run loses its certificate in between.
