## 1. Laws that are wrong or unsatisfiable together

I found no set of laws that is jointly unsatisfiable. Several laws, however, reject a correct model or certify a wrong one.

**`TheoryFileNoExtern (l : Loader) (p : SurfaceProgram) : Bool := l.admits TheoryFile p == not (hasExtern p)`**
- Because this is stated as `==`, it forces a loader to admit every theory file without an extern, including one with a top-level action or a model value. 12.S23 rejects both, and the file's own header says "no extern and no top-level action".
- `hasExtern` only looks at the body of a top-level `define` that is directly an `extern` application. A loader that also catches an extern under a `fn`, a `let` or a `match` therefore *fails* the law.
- The law should be one direction, `hasExtern p` implies not admitted, plus the other rejections as separate laws.

**`ModelFileAdmits (l : Loader) (p : SurfaceProgram) : Bool := l.admits ModelFile p`**
- This forbids rejecting anything in a model file. D-2026-10-13-i and -j (cited in 12.S23) say different models of one theory live in different files.
- A correct loader that rejects two models of one theory in one `.lut` fails this law.

**`DemandReadsItsFile`, `member "la_numpy.lut" (l.reads sample "main.lut" ["x"])`**
- `reads` does not distinguish the checker's demand from `run`'s. 12.S22 says the importer is checked against the theory alone, without reading the model's file.
- Read as a checker demand, this law contradicts 12.S22. Read as a run demand, it is right. `reads` needs the kind of demand as an argument.

**`both (u v : Verdict)` in laws.lth §3**
- This function is not commutative: `both Supported Unsettled = Supported` but `both Unsettled Supported = Unsettled`.
- The first result is unsound, because a conjunction with an unsettled part is reported as supported.
- It also drops information: `both (TakenOn r) Supported = TakenOn r` loses the statistical part, and `both (TakenOn r) (TakenOn s)` loses `s`.
- Through `BothByPair`, this makes `settles (Both p q)` depend on the order of `p` and `q`.

**`Law : U := data { Forall : (A : U) -> (A -> Law) -> Law ; ... }`** (and `Evidence`'s `At : (A : U) -> A -> ...`)
- A type in `U` with a constructor over `U` is inconsistent under a predicative checker. `Law` and `Evidence` belong one universe up.
- This is not a law, but it will be the first thing the type checker rejects.

**Laws quantified over `(E : U)`, `(A : U)` or `(p : A -> Law)`** (`VerdictOfCheck`, `SampleNeverConfirms`, `BothByPair`)
- These have no generator, so as written they cannot be tested. They need to be stated at chosen types, or as case laws.

**`ExactLift`**
- This law is a consequence of `VerdictOfBool` together with `CostScale`'s two laws. It is redundant, not wrong.

## 2. Evidence: `Settling` against D-2026-10-13-l

It says only part of it. Every form-to-evidence law is stated on a constant predicate, so it cannot tell whether the model evaluates `p a` at all.

**A `forall` refuted exactly by a counterexample.**
- `ForallRefutedByCounterexample` uses `fn x { Case false }`, where every point is a counterexample. A model that refutes any `Forall` given any `At` passes.
- Missing are the compositional law, `settles (Forall A p) (At A a e)` is `Refuted` when `settles (p a) e` is, and the converse that makes it "exactly": no evidence other than a counterexample refutes a `forall`, so `Listed` or `Drawn` with all parts confirmed is never `Refuted`.
- A `Drawn` sample that contains a counterexample is never said to refute.

**Confirmed over an infinite domain only statistically.**
- `SampleNeverConfirms` is only negative. A model that returns `Unsettled` for every sample passes, because nothing says a clean `Drawn` gives `Supported`.
- `Drawn : Nat -> List Evidence -> Evidence` carries a seed but no statistic or level (7.S17).
- Exhaustive confirmation of a finite domain (`Listed`) has no law, and the theory has no notion of a finite `A`.

**An `exists` confirmed by a witness.**
- Again this is stated only on `fn x { Case true }`.
- Missing: a witness whose evidence does not confirm does not confirm; a single false instance never refutes an `exists` (the dual of the `forall` case); and above all, "a witness with its cost", which is determinate but not zero over the reals.
- Neither `At` nor `Verdict` has a cost, so the graded confirmation the decision describes cannot be expressed.

**`then` material.**
- `ThenIsMaterial` settles `Then` by `Evaluated (material a b)`, which is evidence already computed as the material value, so the law is close to a tautology.
- It never ties `Then p q` to the evidence of its parts. A model that treats `Then` like `Both` on a `Pair` passes.
- `Law` has no `Not`, so the definition `not (p and not q)` cannot be written as a form. `Then` is primitive where the decision makes it derived.

**A citation models a law whole.**
- `CitedWhole` and `AssumedWhole` state this.
- With `r = "assumption"`, however, a citation and an assumption give the same verdict.
- The reference is a `String`, while 12.R1 makes a citation take a `Reference` value from a `.bib`.

**Also missing.**
- `Evaluated b` carries its own Boolean, so evidence can lie. `settles (Case true) (Evaluated false)` is unconstrained, and a model may confirm it.
- `Either` has no refutation law (both sides refuted), and `Side false` (the right side) has no law.

## 3. Checks

**Projections and 5.S9.** The four laws do state that the projections are determined by `failures` as 5.S9 says. Three gaps remain:
- Both `ok : T -> Reason T E` and `refine : T -> Maybe T` lose the subtype. The comment owns only the second.
- Nothing relates `Bool` to `Failures Unit` cut at one failure, which 5.S9 states as the meaning of `Bool`.
- `ReasonOfFirst` and `RefineIsHolds` use `==` on `Reason T E` and `Maybe T`. That needs structural equality on `T` and `E`, which 5.S4 does not grant for every carrier.

**`both` and `either` and 5.S11.**
- `BothConcatenates` and `EitherKeepsBoth` state 5.S11 correctly.
- Missing: the bind of the reason form, which stops at the first failure. The file defers it to spec 8, but 5.S10 puts "their composition" in this library.
- Also missing: anything saying `both` is the applicative structure 5.S11 names. `concatFailures` re-defines list append instead of using the free monoid of kernel_laws.lth that the comment cites, so associativity and unit are neither inherited nor stated.

## 4. The library

**What the laws state.**
- The extension decides the kind (12.S23).
- A demand-free read is empty (12.S21).
- A theory demand reads no model (12.S21, 12.S22).
- The model's own name and its sibling `helper` are invisible to the importer.

**What a loader could do wrong and still pass.**

*File kinds:*
- `KindByExtension` checks two literal paths. A loader that hard-codes them, or calls every non-`.lth` path a model file (`.bib`, no extension, `x.lth.lut`), passes.

*What is visible:*
- `SeesOwnImportedAndCore` is a lower bound only. A loader that makes every name of every file visible except `helper` and `Numpy` passes, including names of files never imported.
- The privacy law does not test ascription. `LinearAlgebra` is declared as `U` with no fields and `helper` is a separate top-level definition, so `SeesModelThroughTheory` tests "no flat import", not "the importer sees only what the theory names" (L6.12).
- A test of ascription needs a model with fields `f` and `g` against a theory that names only `f`, with `LA.g` invisible.

*What is read:*
- `reads` has no upper bound beyond the theory case. A loader that reads every file in the system on any non-empty demand passes, and so does one that reads imports no demand reaches.

*Not stated at all:*
- The check on first demand that the model file defines that name as a model of that theory, with an error otherwise (12.S22).
- Rejection of a theory file that imports a model file.
- Unknown extensions.

## 5. Roles (L2.7)

| Type | Constructors with a role | Constructors without a role |
|---|---|---|
| `Law` | all six appear in a law (`Then` only through the near-tautology above) | none |
| `Evidence` | `Evaluated`, `At`, `Pair`, `Side`, `Cited`, `Assumed` | `Listed` (no law); `Drawn` (only a negative law, nothing it produces); `Side false` (no law) |
| `Verdict` | `Confirmed`, `Refuted`, `TakenOn` | `Supported`, `Unsettled` (no law produces them; they appear only inside `both`) |
| `Reason` | `ok`, `failed`, both in `ReasonOfFirst` | none |
| `FileKind` | `TheoryFile`, `ModelFile`, through `KindByExtension` and `admits` | none, though `ModelFile`'s role is the over-strong `ModelFileAdmits` |

## 6. What I would change first

I would change `both` in `Settling`, together with `BothByPair` that fixes it in the theory.

This is the certifier's specification. As written, a conforming certifier reports a conjunction with an unrun part as `Supported` and makes the verdict depend on the order of the conjuncts. A certificate built on it would overstate what was tested.

5.S8 also makes the combination of grades the demand's choice (the vector of grades, or the weakest), so the theory should not fix one. The least it should state is that `Unsettled` absorbs `Supported` and that the combination is commutative. Better still, the combination should be a parameter of the demand.

## Against the specification (separate item)

**5.S3 and `LawValue`.**
- 5.S3 asks for `verdict : V -> C` per value type, so that "a law into a type with no verdict is not a law".
- `LawValue` is instead one record with three fixed fields, each fully determined by its law. It is a second implementation in law form (4.R10), and it cannot express the exclusion.
- The same holds for `Projections` and `Composition` in checks.lth: each law restates its field, and checks_model.lut writes them again.
- I would make these plain definitions, and state as laws only what characterizes them, for example `holds (both c d) x == (holds c x and holds d x)`. They should not be theories with exactly one model.

**5.S1 and 5.S2 against `Law`.**
- 5.S2 decides laws valued in `C`, and 5.S1 makes `Law` the type a test runs.
- `Case : Bool -> Law` admits only Boolean cases. Either `Law` needs a cost-valued case, or the spec should say that `Law` is Boolean-only until `C` exists.