# Report: the spec says what the code does (step 2)

Brief `prompt-spec-status.md`; input `report-debt.md` (step 1). Made 2026-10-16 by a Sonnet 5.5 agent.
`python3 scripts/check_spec.py` exits 1 as before with the single finding 03-kernel.md:190 (a run of ten words
shared with docs/principles.md) and prints: `check-spec (information): 181 implemented, 81 decided (of which 33
suspended), 8 proposed` (before: 139 implemented, 122 decided, 9 proposed).

## Checker and index (6c08c32)
`[decided D-x; suspended by D-y]` and `[decided Ln.k; suspended by D-y]` accepted, D-y looked up in
record/decisions.md; one information line with the counts; docstring and docs/spec/00-index.md updated.
A `[proposed]` clause cannot carry a suspension (the grammar says decided), so those got the postponement in text.

## Changed to [implemented] (42; evidence re-checked by opening the code, line numbers in the debt report had drifted, so I confirmed by symbol)
- 2.S2, 2.S21: parse.py:3-4 (literals derived from luthierSyntax), test_parse.py `test_literals_are_not_names`, `test_other_words_are_names`. 2.S19: same tests (`test`, `gen` ordinary names), test.lth TestSpec.
- 3.S2: core.lut `primitive` bodies, library.lth hasPrimitive/hasAxiom. 3.S3: parse.py acts import and operator. 3.S35: no define action in world.lth, Program is data.
- 4.S6: cli.py `_standings`, check.py `declared`. 4.S9: kernel_laws.lth Object/Concrete. 4.S10: by absence, nothing asks it (tests/eval/plan_agree.lut is the agreement law; status was proposed). 4.S14, 4.S17: check.py violatesS14, looseFunction, reported not rejected as the clause says.
- 5.S3, 5.S5, 5.S7: laws.lth CostScale, lift, exact, verdictOfBool, verdictOfCheck, VerdictsAreExact; numbers.lth Tolerance. 5.S4: kernel_laws.lth. 5.S9, 5.S10, 5.S11: checks.lth Failures, Reason, isEmpty, take, holds, refine, both/either/chain.
- 6.S2: laws.lth Evidence (Cited, Assumed, Tested); certification.lth Certificate. 6.S14: certification.lth ProvisionalIsRefused, run.py refusal, cli.py --accept help (12.S17).
- 7.S16: run.py `x.run.json` record, world.lth Crossing. 7.S17, 7.S18: tester.py sequential test (alpha, beta, delta in the entry); the clause already carries D-2026-10-15-b's amendment. 7.S20: test.lth TestSpec, defaultBudgets.
- 8.S5, 8.S6: world.lth actions by type; translation.lth `<-` binds a fresh name. 8.S9: certify.serves via run.py, certification.lth ServesAtTheCutoff; results by key from step 3a. 8.S14: plan.lth Confluent, tests/eval/plan_agree.lut, tests/test_session.py. 8.S15: demand.lth `recorded`, run.py record.
- 9.S1, 9.S3, 9.S4: certification.lth specimens with *_model.lut; run.py FirstActions and Host laws; plan_agree.lut.
- 10.S1, 10.S3, 10.S4, 10.S5, 10.S13: world.lth sections 1 to 5. 10.S7: run.py HostChangesOnlyDeclared. 10.S14: by absence.
- 11.S11: generators.lth section 1. 12.S9: arrays.lth with arrays_model.lut and arrays.py. 12.S17: refusal in run.py and certification.lth (its last sentence, "Today ... refuses only under --require-certified", is stale; I did not touch the wording).

## Suspended (33), status edited
D-2026-10-14-c (17): 1.S12, 5.S2, 6.S4, 6.S5, 6.S6, 6.S7, 6.S10, 6.S11, 6.S12, 6.S13, 6.S15, 7.S10, 7.S11, 8.S1, 8.S2, 11.S10, 11.S18.
D-2026-10-13-m (1): 6.S16. Its comment at certification.lth:26 names D-2026-10-13-m; D-2026-10-14-c would make 6.S4 and 6.S16 begin with an eight-word run the checker rejects as a repeat.
D-2026-10-13-ae (2): 3.S39, 4.R2. D-2026-10-13-ad (13): 9.S5 to 9.S17 (9.S8 and 9.S11 are `[decided L6.4]` and `[decided L6.8]`, now with the suspension).

## Postponement written in the clause's text (11, no decision named by the comment)
4.S11, 4.S12, 4.S13 (lib/program.lth:259); 7.S3 (generators.lth:41); 8.S3, 8.S4, 8.S11 (plan.lth:37); 10.S12 (world.lth:63); 11.S16 and 11.S19 (numbers.lth:24, core.lut:99); 11.S17 (under D-2026-10-14-c, being a proposed clause).

## Left as they are, with the reason
- 1.S11: a symbols table, nothing in the code to confirm.
- 3.R3, 4.R10, 7.R1, 7.R2, 7.R4: rules; `[implemented]` needs an accept and a reject program in Files, they have none or only an accept (3.R3).
- 4.S22: the tests have a smaller Codec (Int), not the Table example of the clause; partial.
- 12.S1: its text says the loader's "file denotes a record" is not yet a law.
- All pending clauses of the debt report (step 1 lists them), the "comment only" five (7.S2, 7.R3, 7.S4, 7.S8, 7.S19) among them.
- Not touched, as the brief says: 8.S8, 8.S10, 12.S18, 10.S6, 12.S11, and src/.

Commits: 6c08c32 (checker, index), d9c4773 .. 9bf852f (one per chapter, 01 to 12).
