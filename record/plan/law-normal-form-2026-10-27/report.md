# Report: a law recognized as a core property by its normal form

Brief: `prompt.md` beside this file (3192a05), on Luciano's idea in `record/notes/idea-law-normal-form-2026-10-27.md`. Claude Opus 5.5, 2026-10-27. Commits 15bdb8e, be275bb, b0f5b26, 9fbc594, 48921d7, 4b685ae, 13e49e9, 5322585, 15fc12f, 39c2a9c, 7bf177b. Committed by the coordinator from the agent's hand-back (its Write was refused). Files: src/luthier/normal.py, tests/test_normal.py, scripts/law_instances.py (version 1), check.py (`report`, the notice), docs/spec/04-static-semantics.md (4.S26 [proposed]).

## What was built

1. `unfold`: δ and β over the program check.py's typing elaborates (the file, its imports, the core's dictionary files), reducing record projections and `Let`. What unfolds is a parameter, `UNFOLD`: laws (capitalized definitions at `Bool`) and models (a body that is a record value), so `structural Float64`'s `eq` becomes `==`; value functions stay folded (they are what a law is about); bound names compare up to α.
2. `prepare` and `sort`: `==` and `/=` sorted; `and` and `or` flattened and sorted; `+` and `*` sorted where the core claims them commutative exactly and flattened where it claims them associative exactly, by the carrier's base type (`EXACT`); Float `+` and `*` sorted, never flattened. The order (`key`) is total and has no meaning.
3. `canonical_labels`: variables named by first occurrence in the ordered body, the body reordered, to a fixed point (`LABEL_ROUNDS` bounds the rounds; a cycle cut at its least form).
4. The operation abstracted: each parameter of a core property is a pattern variable; in a head's position it stands for a head (`t.reading`, `+`, `dist p`), in an argument's for an atom; a projection of a parameter (`o.eq`, `p.x`) for the same projection of one term of the law.
5. `dictionary()`: 135 properties from core/properties/*.lth and core/structures/*.lth, 200 entries with variants (a property with `o : Object B` entered as written and at `o = structural B`).
6. `recognize(law)`: each property the law is an instance of, with its instantiation; a match counts when the property, instantiated, normalizes to exactly the law's form.

`check -v` prints `instance L: L is P at ...` per recognized law (15fc12f); a notice only, no cone, store or result changes. On docs/concepts/tape.lth: `docs/concepts/tape.lth:22: instance ReadingSymmetric: ReadingSymmetric is Commutative at A = Mark, B = Float64, o = structural Float64, op = t.reading, x = a, y = b`.

## Tests

tests/test_normal.py, 13 tests passing; test_check.py and test_spec.py 192 passed, 7 xfailed; the check, report and modes tests of test_modes.py, test_audit_correspondence.py and test_certify.py 36 passed. They show: the tape's `ReadingSymmetric` gives exactly the line above; with sides swapped or variables renamed, the same normal form; `(a + b) + c == a + (b + c)` over `Float64` is not `Associative` and not trivial (not flattened); over a model's field (`d : Doubles Float64`), `d.plus (d.plus x y) z == d.plus x (d.plus y z)` is not `Associative` either, since `Doubles` claims `PlusAssociativeWithin d`, while `d.plus y x == d.plus x y` is `Commutative`; `ReadingSteps` and `ReadingAdds` recognized as nothing; 134 of the 135 core properties recognized as themselves (`OnlyThePoint`'s as-written form is degenerate; only its `structural` variant is entered); an integer associativity and `a + b == b + a` at `Int` become `X == X` under the quotient and are no instance; `a - b == b - a` at `Int` is recognized as `Commutative` at `op = -` (the notice says what a law states, not that it holds).

## The scan

`scripts/law_instances.py` over src/luthier/lib, examples and tests/tester at 13e49e9 (488 s): 77 laws recognized. 54 are wrappers whose body names the property (core.lut's 50 `IntCommutative`-style claims, `DotCommutative`, `ReverseIsAnInvolution`, `SqrtMonotone`, `KolmogorovAgrees`). The ad hoc ones, homonyms core_metrics missed:
- lib/certification.lth: `NothingIsTheUnit` is `LeftNeutral` at A = Maybe ?, o = structural, op = q.combine, e = nothing, x = g
- lib/core/lists.lut: `AppendAddsLengths` is `Preserving` at A = List A, B = Nat, opA = op, opB = +, f = lengthList A
- lib/ebnf.lth: `AcceptsWhatDerives` is `Pointwise` at B = Bool, f = derives d e, g = r.accepts, x = ts
- lib/laws.lth: `ZeroIsExact` is `Reflexive` at A = C, r = s.leq, x = s.zero
- lib/laws.lth: `CombineNeverConfirmsMore` is `Preserving` at A = Verdict, B = Bool, opA = m.combine, opB = and, f = isConfirmed
- lib/laws.lth: `WorseRatioCommutes` is `Commutative` at A = B = Maybe Float64, o = structural, op = m.worseRatio
- lib/laws.lth: `WorseRatioAssociates` is `Associative` at A = Maybe Float64, o = structural, op = m.worseRatio
- lib/numbers.lth: `DivideOne` is `RightNeutral` at A = Float64, op = d.divide, e = 1.0
- lib/plan.lth: `LookupComparesTheFullKey` is `Pointwise2` at C = Bool, f = ==, g = h.serves true, x = stored, y = asked
- lib/program.lth: `RefinesItself` is `Reflexive` at A = Term, r = t.refines, x = ty
- lib/world.lth: `IdentityCarriesHash` is `Injective` at A = B = String, f = e.identity r, x = h, y = k
- tests/tester/laws.test.lut and weakest.test.lut: `NotInvolutive` is `Involutive` at A = Bool, f = not
- tests/tester/laws.test.lut: `AndIsOr` is `Pointwise2` at A = B = Bool, f = and, g = or
- tests/tester/vacuity.test.lut: `ZeroIsNeutral` is `LeftNeutral` and `RightNeutral` at A = Int, op = +, e = 0
`IntPlusCommutes` is trivial since 5322585 and no longer listed. Some of core.lut's wrappers also read as a second property (the same statement under two names): `IntCancellative` is `Injective` at f = op x; `IntPointwise2` is `Pointwise` at f = f x; `IntSurjective` is `Inverse` and `IntInverse` is `Surjective`; `IntCongruent` is `Monotone` at s = == and also `Substitutive`. No file failed to read; nothing is claimed of the laws not listed.

## Limits met

- The theory bounds the method (Richardson's theorem; Knuth-Bendix may not terminate); narrower in practice: only commutativity and associativity reorder, and a flattened node matches only at its arity.
- The first scans gave 518 false instances out of 578: core properties whose body is a parameter applied to parameters (`Least`'s `leq bottom x`, `LandsIn`'s `p (f x)`, `Symmetric`'s `r p.y p.x`) match any application. Three rules removed them: a typed match (each parameter's term of the parameter's instantiated type, so `Symmetric` needs a pair typed `Related A r`); a projection of a parameter stands for the same projection; the property's last parameter is the law's last. `Least`, `Greatest` and `LandsIn` stay out of the dictionary.
- Unresolved types show as `?`. Labels are the theory's (`t.equal` against `o.eq` is not matched).
- Cost: `check -v` about 5 s more per process; the full scan 8 to 17 minutes.
- `and` and `or` are sorted: exact for the Boolean they denote, not for evaluation; acceptable for a notice, never done to a run.

## Decisions taken on my own

`UNFOLD = "laws and models"` (P11); a law is a capitalized definition at `Bool` with no `&`; global operators matched as written; within-bound withholding read from the `WITHIN` table for global operators and from the theory's own conjuncts for a model's field; the three restrictions above, degenerate properties left out; a law trivial under the quotient is no instance; names `instance` and 4.S26; the scan kept as a script (P2). Each one commit to undo.

## Question

Should a later task rewrite the eleven ad hoc laws as one-line claims of the core property, as `DotCommutative` is, so they reuse the core's controls, or stay as written with the notice enough?

Coordinator's answer (2026-10-27): they stay as written. Luciano's idea is that Luthier accepts both ways and deduces the instance; the next step is that a recognized instance reuses the core property's controls and certificates through the recognition, without rewriting the law.
