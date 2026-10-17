# Bite 2, the properties: report

2026-10-17, by Claude Fable 5.1, an agent of the coordinating session, on `prompt-bite-2.md` of
this folder (execution.md sections 1, 2, 3.1 to 3.3, 6 and 8; D-2026-10-17-b, -c, -d, -f as
dc781f2 corrects it). Bite 1 had not started, so the properties import `Object` from
kernel_laws.lth; bite 1 repoints that line when it moves `Object`.

Commits, staged by path:

- c05df18 `src/luthier/lib/core/properties/relations.lth`, `operations.lth`, `functions.lth`.
- 0fbde1a `tests/tester/core_instances.lut`, `core_laws.test.lut`, `core_controls.test.lut`;
  `Complemented`'s binder renamed in operations.lth.
- 9a62e94 execution.md: the Status line and bite 2 as built.
- this commit: the report.

## What the checks printed

- `luthier check` on the three files: nothing, exit 0. With `-v`: 32 `unclaimed` (every Bool law
  of the three files, claimed by no body in its own file; the claimants are the wrappers of
  core_instances.lut now and the structures of bite 3 later) and `loose` on every definition, as
  on every library file. Note that `check` is weak on these files: a probe with `r x` typed as
  `Bool`, a projection of a field that does not exist and `x + "a"` also passed with exit 0, so
  the test programs are what verifies the signatures.
- `luthier certify tests/tester/core_laws.test.lut tests/tester/core_controls.test.lut`:
  `core_laws.test.lut: 58 laws, 73 lines ran, 0 known`, every law `sampled` or `cases` and
  `controlled (refuted on its control at ...)`; `core_controls.test.lut: 0 laws, 59 controls, 59
  lines ran, 0 known`, every control `refuted ...: the control passed`. No `uncontrolled`, no
  `not run`, no `control failed`. 30 s. The store is `tests/tester/core_instances.cert.json`,
  untracked.
- `python -m pytest -q`, in the background: `7 failed, 805 passed, 6 skipped, 9 xfailed in
  1377.75s`. The seven (test_lm's maximizer, test_run's numpy norm, product, checked runs and the
  bound maximize) all fail on one message: `numpy: PinvSymmetric: failed at m = numpy, tol =
  tolerance, fl = floor, s = { m := 10, n := 10, f := extern "host:616595" }`, a `Failed` entry
  dated 2026-10-17T13:36 in the uncommitted working-tree `arrays_model.cert.json`, which the
  other agent's work on tester.py and the stores is rewriting (its commit 2070458 landed during
  the run). Nothing imports the files of this bite, so the failures are not bite 2's; 805 passed
  against 799 before.
- `python3 scripts/check_spec.py`: its known finding only, `docs/spec/03-kernel.md:190` (the run
  of 10 words shared with docs/principles.md); exit 1 as before.

## Signatures of section 3 that changed, and how

1. The composites. `Equivalence`, `Preorder`, `PartialOrder`, `TotalOrder`, `StrictOrder`
   (3.1), `Isomorphism`, `Bijective` (3.3) were written as `&` of partially applied laws whose
   quantified variables differ (`Reflexive A r : A -> Bool` beside `Symmetric A r : Related A r
   -> Bool`). `luthier check` accepts that, but the kernel has no reduction for `&` on functions:
   `luthier eval` of `Equivalence Int (fn a b { a == b })` returns the stuck term `& fn (x : Int)
   {...} (& ...)`, no Bool, so no test could grade it and a structure's wrapper of bite 3
   (`ObjectEquivalence A o := Equivalence A o.eq`) would raise "the law gave ..., not a Bool".
   Each composite now takes the quantified variables of its parts, drawn independently, and
   conjoins the parts with `and`:
   `Equivalence (A : U) (r : A -> A -> Bool) (x : A) (p : Related A r) (c : Chain A r) : Bool`,
   `Preorder ... (x : A) (c : Chain A r)`, `PartialOrder (A) (o) (r) (x y : A) (c : Chain A r)`,
   `TotalOrder` the same, `StrictOrder (A) (r) (x : A) (p : Related A r) (c : Chain A r)`,
   `Isomorphism (A B) (oA) (oB) (to) (from) (x : A) (y : B)`, `Bijective (A B) (oA) (oB) (f) (s)
   (x y : A) (z : B)`. The names are D-2026-10-17-c's; only the quantifiers were added. Section
   2's reason for keeping a record in a structure (the tester quantifies a conjunction's
   variables as one law's) is the same fact, and bite 3's one-line wrappers pass these variables
   through (`ObjectEquivalence (A : U) (o : Object A) (x : A) (p : Related A o.eq) (c : Chain A
   o.eq) : Bool := Equivalence A o.eq x p c`).
2. `Complemented`'s constant is `(z : A)`, not `(unit : A)`: `unit` is core's constructor of
   `Unit`, and the constant is the operation's absorbing element (`false` for `and`, `true` for
   `or`), so it shares `Absorbing`'s name for it, which also lets one profile bind both laws.
3. functions.lth imports `Related` from relations.lth (for `Monotone`, `Congruent`); the plan
   did not list the import.

Everything else is as section 3 writes it, including `functions (A B : U) (o : Object B) : Object
(A -> B)` declared and not defined, `Both` (a type, exercised by `IntBothWaysEqual`), and the five
within-bound operations and three within-bound functions.

## The instances and the controls

The wrappers live in `tests/tester/core_instances.lut` and not in the test programs: a control
is matched to its law by the hash of the law's cone (certify.py `control_status`), so the laws
program and the controls program must name one definition with the instance as a parameter
bound by each program's profile, and a test program is never imported (D-2026-10-16-e); the
pattern is fit_cutoffs.lut's and plot_cases.lut's. One wrapper per property per type
(`IntReflexive (r : Int -> Int -> Bool) (x : Int) := Reflexive Int r x`, `BoolCommutative`,
`StringNeutral`, `FloatAssociativeWithin`, ...; 58 wrappers), the equalities values of `Object`
built with `==`.

Confirmed instances: `Int` with `<=`, `<`, `==`, parity (the equivalence), `+`, `*`, `min`,
`max`, the projections, `0`, `1`, `succ`, `pred`, `negate`, `double`, `square`, `clamp`, and
functions built with `id`, `compose`, `flip`, `const` against ones written by hand; `Bool` with
`and`, `or`, `not`, `true`, `false`; `String` with `+` and `""`; `Float64` with `+` within
`3 gamma2 (|x| + |y| + |z|)` (D-2026-10-17-f, dc781f2), `*` over `+` within `3 gamma2 |x| (|y| +
|z|)`, `x * 0.1` against `x / 10` within `gamma2 |x|`, and the exact ones (`+` commutative,
`0.0` neutral, negation an inverse and an involution, clamp idempotent) within a bound of zero.

Controls, each refuted: the brief's (`-` for Associative and Commutative, `<` for Reflexive,
`x + 1` for Idempotent and Involutive, `fn x y { x }` for Cancellative, a bound of zero for
AssociativeWithin on `+`), and for the rest an instance whose refutation is not a rare draw:
`always` (comparability, every pair related) against Antisymmetric and PartialOrder, `near`
(within 3) against Transitive, `==` against Total and Asymmetric, `<=` within a parity class (a
partial order that is not total) against TotalOrder, implication against the laws of a Boolean
operation, a projection against the neutral law of the other side, `double` with `half` against
Surjective and Bijective, `square` against Preserving, `negate` against Monotone, `id` against
Congruent, bounds of zero against the within-bound laws on `-`, `1.0`, `x + 1.0`.
`StringCommutative` has a control and no confirmed instance (`+` on strings is not commutative).

Two draws had to be chosen with 7.S6 in mind: `Chain Int equal` (one value three times) is found
too rarely at size 10 in 2000 tries, so `Equivalence`'s instance is parity and `TotalOrder`'s
control is `<=` within a parity class rather than `==`. 4.R3 refuses a predicate that does not
read its arguments, so `always` is `a <= b or b <= a` and `constTrue` is `b or not b`.

## Decisions taken on my own (one commit undoes each)

- The composites quantify their parts' variables and conjoin with `and` (above, item 1).
- `Complemented`'s binder is `z` (item 2).
- The wrappers and the real instances live in `core_instances.lut`, imported by both programs;
  the broken instances in `core_controls.test.lut`.
- Wrapper names are the type joined to the property (`IntReflexive`), the instance bound by the
  parameter's name from a profile named after the instance (`onLeq`, `onPlus`); the bounds are
  named by arity (`bound1`, `bound2`, `bound3`) so that one profile serves every within-bound law.
- The gamma2 bounds of the confirmed `Float64` instances, derived in core_instances.lut's comment.

## For bite 3

A structure's one-line wrapper of a composite must pass the quantified variables (item 1). And
the plan's circular import (relations.lth imports `Object` from equality.lth, whose
`ObjectEquivalence` imports `Equivalence` from relations.lth) is a cycle of files; core.lut's
note says the loader allows one when no name reaches itself, which holds here, but it is untested.

## Question

The composite predicates cannot be the `&` of partially applied laws the design wrote (section
3.1, 3.3; the kernel does not reduce it). Is the fix taken here, one Bool law over the parts'
variables drawn independently, the form you want, or should the tester learn to split a `&` of
laws into its conjuncts (which section 2 also waits for, to drop the structures' records)?
