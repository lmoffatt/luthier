I am not counting the two stated limits—Nat induction and uniqueness of the free-monoid fold—as findings.

### 1. **Laws that are wrong**

I found **no Bool law that is simply false of the intended core model, nor a pair that is plainly inconsistent**. The serious defects are mostly weaker: laws that admit models they were meant to exclude.

There is, however, a domain problem with structural equality: `Substitutive ... (B : U) ... := f p.x == f p.y` quantifies over arbitrary codomains `B`, although chapter 3 explicitly says equality of functions is not structural. The same problem appears in several generic categorical laws using `==` on arbitrary `A : U`, `B : U`, etc. They need objects/equalities, not merely structures. kernel_laws.lth 03-kernel(3)

### 2. **Laws that do not determine what they claim**

This is the main problem.

- **`Structural` admits `eq = false` everywhere.** The line is `StructuralIsObject ... (x : A) (p : EqualPair ...) (c : EqualChain ...)`. If `eq` is constantly false, `EqualPair` and `EqualChain` are empty, so that whole law has no cases—including its embedded `Reflexive` check. `Substitutive` also has no cases. Thus the always-false equality passes `Structural`. Reflexivity must remain a separate law quantified only over `x`, as it is in `Object`. kernel_laws.lth

- **`Reduction` admits the reducer `reduce p n t = nothing` for every input.** `agree` says `"nothing -> true"`, and `Final` also says `"nothing -> true"`. Therefore the completely non-operational interpreter satisfies *every* reduction law. term.lth term.lth

- **`Alpha` does not determine alpha-equivalence for all binders.** `RenameBound` specifies renaming only for `Lam` and `Pi`. A perfectly good equivalence relation that performs alpha-renaming for `Lam`/`Pi` but requires literal binder equality for `Sigma`, `Subtype`, `Data`, and pattern-bound variables satisfies the remaining congruence laws. It wrongly rejects, for example, `Sigma "x" U (Var "x")` versus `Sigma "y" U (Var "y")`. term.lth

- **`Substitution` is radically underdetermined.** A model can implement correct substitution for `Var`, `App`, `Pair`, `Inj`, and `Lam`, but simply return the original term for `Pi`, `Sigma`, `Subtype`, `Match`, `Sum`, `Data`, records and `Proj`. It passes every listed law, including `SubstRespectsAlpha`. term.lth

- **`CanonicalForm` need not remove module prefixes.** Take a correct alpha-normalizer, but set `unqualify x = x`. Then `UnqualifyIdempotent` holds, `CanonOfName` holds, `CanonOfAlpha` holds, and `CanonKeepsTerm` holds because every name is now considered “already unqualified”. This directly defeats the stated purpose. term.lth

- **Named products/coproducts do not bind their names to their arrows.** For `recordXY`, keep the correct `.x` and `.y` projections but put `firstName := "foo", secondName := "bar"`. Every `NamedProduct` law still passes because names are constrained only by `"not (firstName == secondName)"`. The same defect exists for injections. kernel_laws.lth

- **`Evaluation` can be a four-case lookup table.** A fake evaluator that handles exactly the Int/String literal cases and `1 + 2`, and returns `nothing` otherwise, satisfies the whole theory. `QuoteGivesTheTerm` does not even mention `e`. term.lth

These are not sampling weaknesses; they are models of the written laws.

### 3. **Roles (L2.7)**

The kernel core roles are basically present: `unit` through terminality, `true`/`false` through Boolean algebra, and `nil`/`cons` through the monoid/fold laws. That follows the explicit L2.7 requirement that constructors require a semantic role, not merely enumeration. principles(10) kernel_laws.lth

The missing roles are in `term.lth` and `term_model.lut`:

- `"Roles: Prim (§5)"` is claimed for `Constant`, but `Prim` mentions only `IntConst`; `FloatConst` and `StringConst` receive no such primitive role. term.lth term.lth
- `"Roles: Iota (§5)"` is claimed for all `Pattern`, but no reduction law states the role of `PLit`. term.lth term.lth
- `Primitive` has no role law in `Reduction`; `Datum` has no law stating what a datum does in a program. term.lth
- The roles of `Universe`, `World`, `Pi`, `Sigma`, `Sum`, `Data`, `Subtype`, and `Record` are explicitly postponed to `WellFormed`; therefore they remain unstated in this bundle rather than being supplied by `ValuesStay`. “Does not reduce” is not the conceptual role of a type former. term.lth
- If L2.7 applies equally to implementation helpers, `HeadStep { Done, Next }`, `PatternStep { Hit, Miss, Demand }`, `PatternListStep`, and `ArmStep` are new `data` definitions with no laws at all. term_model.lut term_model.lut

### 4. **The models against their theories**

For the ordinary concrete kernel models—`Unit`, `Empty`, `Bool`, `List`, `Nat`, pair, Bool/Maybe coproduct—I find no counterexample to the laws actually written. kernel_models.lut

One model declaration is over-general:

> `structuralEquality (A : U) : Structural A := { eq := fn x y { x == y } }`

This cannot hold for arbitrary `A : U`: take `A = Nat -> Nat`; chapter 3 explicitly says function equality is not structural. The model must range over structures possessing structural equality, not all `U`. kernel_models.lut 03-kernel(3)

For `term_model.lut`, I found no counterexample to the **weak written `Reduction` laws**. I do find semantic counterexamples the theory fails to test. Most clearly, a user definition of `"+"` loses to primitive recognition: `stepApplication` detects `App (Var "+") i` before delta and `stepPrimitive` computes the integer operation without consulting `lookupBody`. Likewise constructor applications are deliberately inspected `"before delta"`. Thus redefined names do not get ordinary Delta semantics in those positions. term_model.lut term_model.lut

### 5. **Reduction**

| Law | Verdict |
|---|---|
| `Beta` | **Shape is faithful**, but `agree` makes every fuel failure count as success. |
| `Delta` | **Incomplete.** `"A defined name reduces to its body"` becomes only `App (Var f) arg`; bare `Var f` is never specified. |
| `Iota` | **Incomplete.** Injection, unary constructor, wildcard, pair and one skip case are present; literal patterns, arbitrary constructor arity/nesting and general arm sequences are not determined. |
| `ProjOfRecord` | **Faithful for the stated two-distinct-field case**, but not a general n-field projection law. |
| `Prim` | **Not faithful to 3.S17.** It states only integer `+`, `*`, `==`; chapter 3 says arithmetic and comparisons on `Int`, `Float64`, `String`, plus structural `==`. |
| `HolesStay` | **Too weak for 3.S19.** It covers bare declared names, `Hole`, and `Axiom`, not “a term containing a hole where reduction needs a value”. |
| `ValuesStay` | Reasonable extra WHNF laws, but incomplete as a characterization: e.g. `Pair`, `Inj`, `Primitive` are absent. |
| `Final` | **Not sound as a fuel invariant**, because either the first run or the `n+1` run may return `nothing` and `agree` then declares success. |
| 3.S18 Extern | **Missing.** `ExternIsValue` says only that a bare extern is a value; it deliberately does not state the required host call when sufficiently applied. |

Chapter 3 states the five rules directly, including the broader Prim and Extern rules. 03-kernel(3) The theory weakens them as above. term.lth

So **`agree` is not sound**. Fuel exhaustion is “no evidence”, but the Bool returned by a law means “law holds”. The comment that the certifier counts exhaustion separately does not repair the theory: as a model predicate, `nothing` has already been converted to `true`. That is exactly why the always-`nothing` reducer inhabits `Reduction`.

### 6. **Against the specification**

There are three direct mismatches, plus one specification-level tension.

First, chapter 3's decided `Act` fields include `"declaration, definition, alias, and the directives of §1"`, whereas `term.lth` defines only `Declare`, `Define`, `Datum`, explaining that aliases/imports disappear. D-2026-10-13-o adds the datum, but does not say that the previously decided alias/directive fields are removed. 03-kernel(3) term.lth

Second, 3.S33 literally says `reduce : Term -> Term`; `term.lth` gives `reduce : Program -> Nat -> Term -> Maybe Term`. Fuel and environment are sensible, but this is nevertheless a different decided interface and needs the specification changed rather than silently interpreted as shorthand. 03-kernel(3) term.lth

Third, 3.S18 says sufficiently applied externs call the host; neither the theory nor `term_model` implements that reduction. An `Extern` falls through `stepHead` as `Done`, so an application remains stuck. 03-kernel(3) term_model.lut

The specification itself also has a tension that the model resolves without a cited decision: 3.S1 says `"A program is a set of top-level acts with no order"` and explicitly allows a later definition to fill a declaration, while 3.S29 says `Program` is a list. `term_model` makes that list operationally ordered: `lookupBody` stops at the first matching `Declare`, so `[Declare f ..., Define f ...]` leaves `f` unresolved. 03-kernel(3) term_model.lut

### 7. **What I would change first**

**Separate one-step reduction from fuelled evaluation.**

The five definitional rules should constrain an exact `step`/head-reduction operation with no `Maybe` fuel outcome. Then define `reduceFuel` separately as iteration of that operation and state its monotonic/stability laws separately. Remove `"nothing -> true"` from semantic equality entirely.

Reason: at present

> `agree ... { nothing -> true ; ... }`

allows **`reduce = always nothing` to be a certified interpreter**. Until that is fixed, strengthening `Beta`, `Delta`, `Iota`, `Prim`, or `Final` individually cannot make `Reduction` mean reduction. term.lth