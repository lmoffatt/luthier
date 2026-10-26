# The rest of D-2026-10-16-k and -l: report

2026-10-26, Claude Opus 5.5, an agent of the coordinating session, from the queue item in record/plan/code-follows-principles-2026-10-16.md (the one after convergence and print) and D-2026-10-16-k and -l. Base commit 5d374dd. Commits: 68d515a, 395cd93, 5b8dd91, c853b61, dc187cb, ed003db, d603119, 78e4e09 (stores), d65c66b (queue line). Logs under ~/.cache/luthier-queue-kl/. Committed by the coordinator from the agent's hand-back (its Write was refused). The same queue item names 3.R1 and 3.R2 (D-2026-10-17-a): not in the brief, not done.

## Per item

- Item 9, a host action validated once per hash of the model's cone (5b8dd91). Not done before: the first action's demand gave the law the model, the run's arguments and the places, so another argument was a new case. Now run.py's `FirstActions` gives the law and the frame law only the model, at its cone's hash (which includes the host code, 6.S8); the arguments, the action held and the places go into the entry's evidence under `case`. `test_a_first_action_is_validated_once_recorded_and_then_served` requires a run at another argument to be served by the first run's entry (fails at 5d374dd). world.lth's comment and 10.S10 say so. Old entries, whose binding lists the arguments, keep serving.
- Item 17, `Bounded n` as a domain (68d515a, dc187cb). test.lth's `grade` already graded a bounded run exhaustive, and certify.py carried the box as `BoxDomain`; missing was laws.lth's `ForallOnPoints`, which now confirms a `forall` whose points are every value of the box (model in laws_model.lut, the tester the same). `grade` no longer calls a box only supported exhaustive; `GradesAsTerms` states both cases; `gradeRank` marked as the Boolean slice's stand-in for L10.2's order. An `exists` is refuted only on the whole type. Test `test_every_value_of_a_box_confirmed_is_confirmed_on_that_box` fails at 5d374dd; control `boxOnlySupports` refuted at `ForallOnPoints`. 7.S10 has a new sentence. The tester's change is a new function `on_its_box` after `run_spec`, whose source is hashed into every sampled identity (`drawing_revision` checked equal to the base's).
- Item 20, per-law cutoffs as a typed field of `Demand` (c853b61, d603119). Not done before: cutoffs travelled in `sets`, so a hole filled with `--set` reached every law with a parameter of that name. demand.lth: `LawCutoff = { law, parameter, value }` and `Demand.cutoffs`; `lawDemand` gives a law `cutoffsOf d law`; `inner`, `recorded`, `RunRecord` and `RecordKeepsThePolicies` carry it. demand_model.lut declares none by default; plan.lth's `withSet` copies it. run.py reads `run --cutoff LAW.PARAMETER=VALUE` as a literal of the parameter's type (aliases and refinements unfolded to String, Int, Float64 or Bool), to that law alone, recorded; a cutoff no law of the cone takes refuses the run. Test `test_a_per_law_cutoff_reaches_its_law_and_a_hole_reaches_none` fails at 5d374dd; control `dropCutoffs` refuted. 8.S1 has a new sentence.
- G6, the most specific binding wins (395cd93). The code already did it (tester.py's `resolve_binding` since 48d2c5d, generators.lth's `resolve` since 2c584f3; 7.R1 said so), but no law stated it: `ParameterWins` let a resolution reading `where` in full first pass. New `ParameterWinsAcrossPlaces` in `Resolution`, a line on the reference `resolve` (none certified `Resolution` before), four controls refuted (`whereFirst`, which only the new law catches; `typeFirst`; `profileFirst`; `somethingAlways`). 7.R1 has a new sentence.
- L5, a law quantified over `U` is a static error, `Settling`'s laws on concrete instances (ed003db). `Settling`'s conjunction claims its laws over the quantified type at `Int` and the stream's state at `Nat`; its two test programs bind no type. The tester refuses a line at its start, before the store is read, when the law has a parameter whose values are types (`U` or a subtype such as `Concrete`) that the model doesn't fix and either no census binds it or a generator does (before: "not run: no generator"). Test `test_a_law_quantified_over_a_type_the_line_does_not_name_is_a_static_error` fails at 5d374dd. 7.R2 has a new sentence. The Settling line ran 13194 cases as before; its 24 controls are refuted.

## Checks

`luthier check` over src/luthier/lib, examples, docs/concepts and tests/tester clean, as at 5d374dd. Certification six at a time with `--jobs 1`: pass 1 ran lines in demand_laws (4), demand_controls (4), generators_laws (1), generators_controls (4), plan_laws (11), plan_controls (11), settling_laws (1), settling_controls (10; its first run hit the one-hour timeout and ran again alone with three hours); pass 2 ran 0 lines in all 54; both return 1 on cases, belief_laws, laws and vacuity (known). Stores in 78e4e09. Suite: every file passes under miniconda's Python (test_run 160, test_certify 90, test_tester 32, test_lm 10); test_check_private collects none.

## Decisions taken on my own

1. L5's static error applies only to a type the test line does not name; a census of types still names its instances.
2. `Settling`'s instance is `Int`, `Nat` for the stream's state.
3. An `exists` is not refuted on a box.
4. A box only supported is graded as the whole type would be (cases).
5. The box's verdict after `run_spec`, so the drawing revision does not change.
6. A first action keeps its case in the evidence under `case`; old entries left in the stores.
7. `LawCutoff` holds certification.lth's `Value`; the parameter type's refinement is not checked when `--cutoff` is read.
8. A `--cutoff` no law of the cone takes refuses the run.
9. New names: `ParameterWinsAcrossPlaces`, `quantified_over_a_type`, `on_its_box`, `cutoffsOf`, `--cutoff`.

## Question

Read strictly, 7.R2 makes any test of a law quantified over a type an error; but 130 conjuncts in 20 test programs bind the type to a census of one type (the core's containers and generic properties, lists, arrays, plan, world, demand, regions, probability, plot), which 7.R2 itself describes as how "a test of a container names the instance it runs at". Do those stay, or does every such law move to its instance in its theory, as Settling's did?

Coordinator's answer (2026-10-27): they stay. A census of types is the line naming its instance, as 7.R2 says; the static error is for a type nothing names.
