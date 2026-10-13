# Review of layers 0 and 1: what the replies say

2026-10-13, by Claude Opus 5.5 (the session that wrote the reviewed files), for the coordinating
session and Luciano. Read whole: A from GPT, DeepSeek, Gemini and Claude Fable (section A amended
with Fable's reply); B from Claude Opus, DeepSeek, Gemini; C from GPT, Claude Opus, Gemini. Each
finding was checked against the file at the frozen commit (7a7d66e) before it was counted; the
count is how many models raised it. Nothing has been fixed yet.

Overall: no reviewer found laws that contradict each other. The common verdict is that many laws
are true but too weak: a wrong model passes them. Four defects are serious, each found by two or
more models:
- the fuel rule that lets a reducer answering `nothing` pass every law of reduction (A);
- `ReportsExactly`, vacuous on random programs and too strong where a rule is only partly stated (B);
- `Settling` stated on constant predicates only (C);
- the loader laws, which give lower bounds and no upper ones (C).

## A. The kernel (kernel_laws, kernel_models, term, term_model)

### Agreed and verified

- **Alpha-equivalence is not pinned down (Fable; GPT and DeepSeek in part).** The model
  `alphaEq s t := head s == head t and sameNames (freeVars s) (freeVars t)` passes every law of
  `Alpha`, yet it equates `Lit 1` with `Lit 2` and `App f g` with `App g f`. Verified: every law of
  §2 says when two terms are alpha-equal, and none says when they are not, except for two `Var`s.
  Since every later theory compares up to `alpha`, a coarse model weakens them all, and no test of
  the right model can show it. Fable's first fix: the converse of `AlphaCongruent`, that
  alpha-equal wholes have alpha-equal parts, head by head, with `RenameBound` for every binder.
- **`agree` makes fuel exhaustion a success (GPT, DeepSeek, Fable; Gemini calls it sound).** So the
  reducer `reduce p n t = nothing` satisfies every law of `Reduction`, `Final` included. Verified:
  `agree` returns `true` on `nothing`. This is the most serious finding. GPT's fix: state the five
  rules on an exact one-step `step` (no fuel), and define the fuelled `reduce` as its iteration,
  with its own laws.
- **Constructors without a law of their role (all three).**
  - `Primitive`, `PLit`, `FloatConst`, `StringConst` and `Datum` have no role law. Verified: `Prim`
    mentions only `IntConst`, and no law uses `PLit` or `Datum`.
  - The type formers' roles are deferred to `Typing`, whose laws do not mention them (also B).
- **`Prim` is narrower than 3.S17 (GPT, DeepSeek).** It covers integers only, not `Float64`,
  `String` or structural `==`. Verified.
- **`Delta` is narrower than 3.S15 (all three).** It covers only `App (Var f) arg`, never a bare
  `Var f`. It also unfolds unconditionally, where 3.S15 says "only when that makes progress"; the
  model's `stepHead` does the same. Verified.
- **The structural equality over every `U` (all three).**
  - `structuralEquality (A : U)` and `Substitutive (B : U)` use `==` on any type. 4.R8 denies `==`
    on function types, so both must range over types with structural equality. Verified.
  - `Structural` with `eq` always false passes (GPT). `StructuralIsObject` puts reflexivity in the
    same law as the quantifications over `EqualPair` and `EqualChain`, which are then empty.
    Verified.
- **The substitution laws are too weak (GPT, Gemini, DeepSeek).**
  - A model that substitutes correctly only into `Var`, `App`, `Pair`, `Inj` and `Lam` passes
    every law; the laws never mention `Pi`, `Sigma`, `Match`, `Data` or records. Verified.
  - The capture case (a binder free in the term substituted) has no law (DeepSeek).
- **Other underdetermined theories (GPT, DeepSeek).** Each verified:
  - `RenameBound` covers only `Lam` and `Pi`.
  - `unqualify = id` passes `CanonicalForm`.
  - The names of `NamedProduct` and `NamedCoproduct` are not tied to their arrows: only
    "distinct" is stated.
  - `Evaluation` is passed by a four-case lookup table, and `QuoteGivesTheTerm` does not mention
    its model.
- **`FoldNil`/`FoldCons` test the helper `foldList` and not a model (Gemini).** They hold by
  definition. Verified.
- **The model reads a program as ordered (GPT).** `lookupBody` stops at a `Declare` that comes
  before the `Define` of the same name. 3.S1 says a program has no order. Verified.
- **3.S18: an applied extern calls the host (GPT).** No law and no model step does this.
- **No reduction strategy is stated (Fable).** No law says that the head of an application, the
  scrutinee of a match or the record of a projection is reduced first, so a model that fires rules
  only at the root passes. And no law asks for a value at any fuel: the one-step laws should say
  `reduce p 1 t == just t`. Verified.
- **The Boolean algebra is self-dual (Fable).** `{ top := false, bottom := true, meet := or, join
  := and }` passes all nine laws, so "the role of `true` is its top" is stated by no law. What tells
  `true` from `false` is `if`; the missing law joins `booleans` to `ifThenElse`
  (`m.top == c.left unit`). Verified. The same holds of `Coproduct Unit Unit Bool`. Also: no law
  says `cons a xs == combine (inject a) xs`.
- **The model reduces a match on a hole (Fable).** `reduce [Declare "z" ty] 3 (Match (Var "z")
  [(PLit (IntConst 0), a), (PWild, b)])` gives `b`, since a stuck scrutinee is read as a miss and
  the wildcard takes it. 3.S19 says it does not reduce. `constructorTerms` also takes a declared
  hole for a nullary constructor, and non-linear patterns become equality tests, which 3.S10 does
  not have. Verified in term_model.lut.
- **`Prim` computes on an undefined `Var "+"` (Fable).** 3.S9 makes a name without a body a hole;
  the primitive rule belongs to the body `Primitive` (3.S2). Verified.
- **`canonical` cannot run (Fable).** Its string functions are holes, so the form that defines the
  hash is an uncertified model. Known, and stated in its report.

### Not taken

- **"`Beta` in kernel_laws is eta" (DeepSeek).** It is beta at the lambda `fn y { f y }`. It is
  weak, since only one kind of body is tested, but it is not eta.
- **"`IotaPair` substitutes sequentially and captures" (DeepSeek).** The guard makes the
  sequential substitution equal to the simultaneous one: the second variable is not free in the
  first value.
- **"`head` is an accessor, against L2.7" (Gemini).** `AlphaKeepsHead` is a law of alpha that
  uses `head`; it does not claim to give constructors their roles.
- **"Prefixed constructor names in patterns are not unqualified" (Gemini).** True, but a minor gap
  of `canonical`. It is mine to fix, not a finding against a law.
- **"`structuralEquality` fails reflexivity on NaN, and substitutivity on `0.0` against `-0.0`"
  (Fable).** By 11.S7 NaN is an error and so is division by zero, so neither case arises. If
  spec 11 makes `-0.0 == 0.0` hold, the case is left for that chapter.

### Mine to fix (no question)

- **Reduction:** split it into an exact `step` and a fuelled `reduce`, and drop "nothing agrees".
  Spec 3.S33 then says `step` and `reduce` with their types; today it says `reduce : Term -> Term`
  (GPT).
- **Roles:** add role laws for `Primitive`, `PLit`, `FloatConst`, `StringConst` and `Datum`.
- **`Prim`:** cover `Float64`, `String` and structural `==`.
- **`Delta`:** cover the bare name, and unfold only when that makes progress, with a stated
  meaning of progress.
- **Equality:**
  - `Structural` and `structuralEquality` range over types with structural equality;
  - `Substitutive` ranges over codomains with structural equality;
  - reflexivity becomes a law of its own.
- **Substitution:** state it for every constructor, and add the capture case.
- **`RenameBound`:** cover every binder, including pattern variables.
- **`CanonicalForm`:** add a law that `unqualify` drops a prefix (`unqualify "m.f" == "f"`).
- **Named products and coproducts:** tie the names to the arrows (`project r.firstName == r.first`).
- **`Evaluation`:** quantify over constants, not just cases.
- **`ListAlgebra`:** remove it, since `FreeMonoid`'s `fold` already gives `nil` and `cons` their
  roles.
- **`lookupBody`:** prefer a `Define` over a `Declare` in any order.
- **3.S18:** an extern step through a host field of the model.
- **`Alpha`:** the converse of congruence for every head, and `Lit c ~ Lit d` only if `c == d`.
  This one goes first.
- **The strategy:** state weak head reduction (head, scrutinee and record reduced first), and add
  the one-step laws at fuel 1.
- **`Bool`:** join `booleans` to `ifThenElse`; add `cons a xs == combine (inject a) xs`.
- **The model:** a match on a hole stays stuck; a hole is not a constructor; patterns are linear.
- **`Prim`:** a rule of `Primitive` bodies, not of a bare name; parenthesize its guard.
- **`IotaPair`:** add the mirror instance (Fable).
- **The comment "a record of more is nested":** wrong against the flat `RecordValue` and
  D-2026-10-13-o.
- **Chapter 3 lags the files (Fable):** 3.R1, 3.S36's `KernelLaws`, 3.S29's `Act`, and `Axiom`'s
  string. To update together with question 2.

## B. The checker (translation, program)

### Agreed and verified

- **`ReportsExactly` is vacuous on random programs (all three).**
  - It holds in both directions (Claude Opus): rules R1, R2 and R3-on-data are violated almost
    always (random names are unknown), and R5 to R12 almost never.
  - "Exactly" is too strong while a predicate is partial (R2, R12, R6): a checker that implements
    the whole rule fails the law (Claude Opus).
  - The fix all three converge on:
    1. split each rule into two laws, over violating and non-violating programs;
    2. draw programs that are well formed, from a small pool of names;
    3. mutate them by one edit aimed at the rule;
    4. take the accept and reject programs of `tests/spec/` as a census;
    5. state only "violates implies reported" until a predicate is complete.
- **Name resolution is wrong (Claude Opus, DeepSeek).** Each case verified:
  - dotted names (`c.parse`) are never resolved to their prefix;
  - a program's constructors are not `known`;
  - an earlier binder is not in scope in a later one;
  - `rebind` does not bind what follows;
  - `sigmaNamed` removes its second name from its own type.

  So R1, R2, R3 and S14 reject the files that state them.
- **`containsArrow` errs in both directions (Claude Opus).**
  - It scans a `data`'s constructor types, which are arrows, and so rejects `==` on almost any
    `data`.
  - It does not see a theory's declared base.
  - It skips pattern-bound variables.

  Verified.
- **4.R4 and 4.R5 miss a declaration followed by a definition (Claude Opus).** 4.R4 is also
  written as a blacklist where the rule is a whitelist. Verified.
- **4.R3 has gaps (all three).** It passes `{ _ : T | true }`, never checks a theory defined
  separately from its declaration, and does not look into lambda predicates. Reading a law as a
  definition at `Bool` counts helpers as laws and misses laws at `Failures E`, at `Law` or with
  parameters. Verified.
- **`fits` (4.R6) rejects parameterized theories and laws of several arguments (Claude Opus).** It
  does not compare under the binders. Verified.
- **`Typing` passes trivial models (Claude Opus, DeepSeek).** With `same` and `refines` always
  true, every law holds. It has no laws for most formers, global names, untypable terms, or the
  pattern half of 4.R11, and `TypeOfLam`/`TypeOfApp` are implications with rare premises.
  Verified.
- **The translation has gaps (all three).** Each verified:
  - missing rows: clauses over two or more parameters; `m.f`; an action in a block; `-x` on
    `Float64`; an alias with binders; the demand that forgets `e`;
  - the §2 laws elaborate undeclared names, where `term` should give `nothing`;
  - `TypeForms` writes a constructor type that is not an arrow (`s : List C`);
  - the `Conditions` reason form needs alpha on pattern binders, which `RenameBound` lacks;
  - the 2.S12 table still says pair, one-branch `match` and `Sigma` where D-2026-10-13-x replaced
    them. That is the table lagging a decision; the coordinating session owns chapter 2.
- **A real slip (Claude Opus).** In `program.lth`, `bodyApplications (e : Elaboration a)` has `a`
  unbound; my mechanical rename did it. Verified.

### Not taken

- **"4.R2 rejects declared names in term position" (Gemini).** `known` includes declared names.
- **"`removeAll` erases valid free variables under shadowing" (Gemini).** The inner scope removes
  its own binder first.
- **"`A + B` to left/right labels is not fixed" (Claude Opus).** 3.S4 fixes them.

### Mine to fix (no question)

- **`ReportsExactly`:**
  - split into "violates implies reported" and "does not violate implies not reported", over two
    subtypes;
  - use generators of well-formed programs, mutated per rule, with `tests/spec/` as a census;
  - state only the sound direction while a predicate is partial.
- **Names:** fix resolution (prefixes, constructors, binder scope, `rebind`, `sigmaNamed`).
- **`containsArrow`:** read constructor arguments, declared bases, and pattern variables.
- **4.R4 and 4.R5:** read declarations, and make 4.R4 a whitelist.
- **4.R3:** read separate theory definitions and lambda predicates. Treat as a law a definition
  reachable from a theory's `&` (Claude Opus), not any definition at `Bool`.
- **`fits`:** compare under binders.
- **`Typing`:** a non-trivial `same` and `refines`, rules for every former and for global names,
  untypable terms, quantification over typed terms, and the pattern half of 4.R11.
- **Translation:** the missing rows and declared contexts. The table of 2.S12 should be updated
  after D-2026-10-13-x; that is the coordinating session's, and I will message it.
- **`bodyApplications`:** bind `a`.
- **4.S14:** report an unclaimed law, or leave it to 4.R2. 4.S14 says such a law "defines nothing",
  not that it is an error.
- **4.R9:** compare bases. Passing a base where its subtype is expected is an obligation (4.R5,
  4.R11), not an error.

## C. Laws, checks, the library (laws, checks, checks_model, library)

### Agreed and verified

- **`Settling` is stated only on constant predicates (all three).** Each verified:
  - the compositional laws are missing ("refuted exactly by a counterexample" with its converse;
    an `exists` not confirmed by a failing witness);
  - `Listed` has no law;
  - `Supported` and `Unsettled` are produced by no law;
  - `Side false` has no law;
  - `Evaluated b` carries its own Boolean, so evidence can lie;
  - the witness of an `exists` has no cost (D-2026-10-13-l);
  - `Then` is primitive and its law nearly a tautology (`Law` has no `Not`).
- **`both` over verdicts is not commutative and is unsound (Claude Opus).** `both Supported
  Unsettled = Supported`, but the other order gives `Unsettled`. 5.S8 makes the combination of
  grades the demand's. Verified.
- **The loader has lower bounds, no upper bounds (all three).** Verified. A loader that reads every
  file, or shows every name except `helper` and `Numpy`, passes. Also:
  - `SeesModelThroughTheory` does not test ascription: the theory has no fields;
  - the check that a file defines the imported name as a model of its theory is absent;
  - `KindByExtension` tests two literal paths.
- **`TheoryFileNoExtern` and `ModelFileAdmits` are stated as `==` (GPT, Claude Opus).**
  - The first forces a theory file to be admitted when it holds an action or a model but no
    extern.
  - The second forbids a model file from being rejected at all.

  Verified.
- **`DemandReadsItsFile` on `"x"` contradicts 12.S22 for the checker's demand (Claude Opus).** The
  checker is checked against the theory without reading the model. `reads` must take the kind of
  demand. Verified.
- **Checks (GPT, Claude Opus).** Each verified:
  - the reason form's `ok` loses the subtype, besides `refine`;
  - nothing ties `Bool` to `Failures Unit` cut at one failure;
  - the bind of the reason form is missing (5.S10 puts composition in this library);
  - `concatFailures` redefines `append` instead of using the free monoid.

### Not taken

- **"`Law`, `Evidence` and the rest are collections, since their roles are in downstream
  theories" (Gemini).** By D-2026-10-13-p a constructor's role may be stated in the theory that
  uses it, as `Rhs` gets its roles from `Derives`. The roles that are missing are listed above.

### Mine to fix (no question)

- **`Settling`:**
  - compositional laws on any predicate, with their converses;
  - `Listed` (exhaustive over a finite type) confirms;
  - a clean `Drawn` supports, and one with a counterexample refutes;
  - `Either` with either side, and both sides refuted;
  - evidence that cannot lie: `Evaluated` checked against the case;
  - a commutative combination, with `Unsettled` absorbing, or a parameter of the demand.
- **The loader:** upper bounds (only the files the demand reaches, only what the theory names), a
  real ascription test (a model with fields beyond its theory's), the model check on first demand,
  the kinds from the extension in general, and `admits` one-directional, with actions and models
  rejected from a theory file.
- **Checks:** `Bool` as `Failures Unit`, the bind of the reason form, `append` from the free
  monoid, and the subtype in `ok` where a field can name it.

## Questions for Luciano

Each with my recommendation; each reversible.

1. **A block in a dependent kernel (B, Claude Opus).** D-2026-10-13-y keeps a block as a lambda
   applied. Under `(fn n { b }) 3`, the body does not know `n ≡ 3`, so `{ n := 3 ; v : Vec n := ... }`
   types as a local definition (`let`) and not as a lambda applied. Recommended: the kernel gains
   a local definition, `Let : String -> Term -> Term -> Term -> Term` (name, type, value, body),
   with `n ≡ 3` inside the body, and a block elaborates to nested `Let`s. Cost: one constructor and
   its laws. The surface (`fn`, blocks) does not change.
2. **The fields of `Act` (A, GPT).** 3.S29, decided in D-2026-10-12-ah, lists `Act` as
   declaration, definition, alias and the directives. term.lth has `Declare`, `Define` and `Datum`,
   since aliases are expanded before checking and the directives became functions (3.S39, 2.S21).
   Recommended: `Act` as in term.lth, with 3.S29 updated to say so.
3. **4.R3 on a `data` (B, Claude Opus).** Chapter 4 says both "each constructor needs a law of its
   role" and "a `data` with no constructor so bound … is reported". Recommended, by L2.7: reject
   when any constructor has no role law (as `Color` stays a reject, 70b1c26), and report the table
   of observers against constructors besides.
4. **The universe (C, Claude Opus).** `Law` and `Evidence` are in `U` with constructors over
   `(A : U)`, and `Typing` states `U : U`. That is consistent only without a hierarchy of
   universes, which is a known inconsistency (Girard) but harmless for testing. Recommended:
   version 0 keeps `U : U`, said in chapter 3 as a known limit; a hierarchy waits for the proof
   layer (3.S11).
5. **Theories with one model (C, Claude Opus, by 4.R10).** `LawValue`, `Projections` and
   `Composition` are theories whose laws restate their single model, which is a second
   implementation in law form. Recommended: make them definitions, and keep as laws only what
   characterizes them, such as `holds (both c d) x == (holds c x and holds d x)`.
6. **Laws valued in `C` (C, Claude Opus).** `Law` admits only Boolean cases, while 5.S2 decides
   laws valued in the cost `C`. Recommended: keep `Law` Boolean until the cost library (step 5),
   and say so in 5.S1; `Law C` then gains a cost case.

7. **Stuck terms and 3.S15 (A, Fable).** 3.S15 says a recursive function applied to an argument
   that does not reduce "stays folded": a name is unfolded only when that makes progress. That is
   a presentation of stuck terms, not a definitional equality. It makes the normal form depend on
   the specimen, so `Delta` is false of a host that follows it and true of term_model.lut.
   Recommended: retire "stays folded" from 3.S15. Reduction unfolds a defined name in head
   position; a stuck term is whatever reduction leaves, the same for every specimen; and folding
   back for display is the printer's.
