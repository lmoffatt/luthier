1. **Laws that are wrong or unsatisfiable together.** I do **not** see a pair of laws that is plainly unsatisfiable together. The main failures are laws that are too weak or state the wrong equivalence.

   The clearest wrong law is in `library.lth`:

   > `TheoryFileNoExtern ... := l.admits TheoryFile p == not (hasExtern p)`

   This says *absence of `extern` is sufficient* for admissibility as a theory file. But 12.S23 requires rejection of “an `extern`, an action or a model value”. So a theory file containing an action or a foreign model but no `extern` is **required by this law to be admitted**. library.lth 12-files-and-tools(3)

   A second problem is the relation templates:

   > `isSymmetric ... := not (r x y) or r y x`  
   > `isTransitive ... := not (r x y and r y z) or r x z`

   The file itself immediately acknowledges that these implication premises “rarely hold” under sampling and says the caller should instead quantify over related pairs. That means the *templates themselves do not enforce the discipline stated in the prompt*; a later theory can innocently quantify them over arbitrary `x,y,z` and obtain nearly vacuous tests. laws.lth

2. **Evidence.** `Settling` captures pieces of D-2026-10-13-l, but **not enough to say the decision**. The decision requires: `forall` evidence may be exhaustive, listed cases, or sampled; exact refutation by counterexample; `exists` by a witness with its cost; conjunction by pair, disjunction by one side; citation/assumption of the whole law; material `then`. decisions-cited(2)

   What is correctly present: citation is genuinely whole-law because

   > `CitedWhole ... (p : Law) ... := m.settles p (Cited r) == TakenOn r`

   quantifies over arbitrary `p`; assumption does likewise. `ThenIsMaterial` agrees with material implication for Boolean cases, and `BothByPair` gives a general pair rule. laws.lth

   What is missing or too weak is substantial. First, “refuted **exactly** by a counterexample” is not stated. The only positive rule is

   > `Forall A (fn x { Case false }) ... == Refuted`

   so it covers the constant-false family, not arbitrary `p` with a counterexample at `a`; there is also no converse forbidding `Refuted` without a counterexample. Likewise the existential law only treats the constant-true family. laws.lth

   Second, `Listed` has **no settling law at all**, and there is no distinguishable exhaustive evidence. Thus the implementation cannot tell “these are all cases” from “these are some hand-picked cases”. `Drawn` only obeys

   > `not (... == Confirmed)`

   rather than being required to yield statistical support when successful or refutation when it contains a counterexample. laws.lth laws.lth

   Third, the decision's cost-bearing existential evidence cannot actually be represented here. `Law` has only

   > `Case : Bool -> Law`

   and `Evidence` only

   > `Evaluated : Bool -> Evidence`

   despite D-2026-10-13-l explicitly requiring an existential witness “with its cost”, possibly non-zero over the reals. §1 knows about cost-valued verdicts, but §3's `Law`/`Evidence` loses them. laws.lth decisions-cited(2)

   Fourth, disjunction is barely specified:

   > `Either (Case true) q` with `Side true ...`

   says nothing about the right side, what the `Bool` in `Side` means generally, or composite laws. Similarly `ThenIsMaterial` only covers `Case a` and `Case b`, not general laws. laws.lth

3. **Checks.** The computational projections mostly state the intended part of 5.S9 correctly. `HoldsIsEmpty`, `FirstIsPrefix`, and `ReasonOfFirst` are exact; `RefineIsHolds` correctly makes the raw value appear iff the check holds. `both` exactly concatenates failures, and `either` returns no failures when either check succeeds and both lists otherwise. checks.lth checks.lth

   But they do **not fully state 5.S9 at the type level**. The specification's reason form contains the refined subtype and `refine` returns `Maybe {x:T | p x}`; here they are deliberately weakened to

   > `ok : T -> Reason T E`  
   > `refine : T -> Maybe T`

   with refinement recovered only by a law. So the behavior is captured, but a consumer does not receive the refinement in its type as 5.S9 states it. checks.lth 05-laws

   And `both`/`either` state those two clauses of 5.S11, **not all of 5.S11**. The dependency-chain rule—bind the reason form, stop at the first failure, and block only the dependent cone—is only mentioned in a comment and explicitly omitted from the theory. checks.lth

4. **The library.** It states fragments of 12.S21–S23 and L6.12, but it is far too example-specific to characterize a loader.

   For 12.S21, these are sound examples:

   > `NothingWithoutDemand ... == nil`  
   > demand for `"LA"` or `"x"` must include `"la_numpy.lut"`  
   > demand for `"LinearAlgebra"` must not include that model file.

   But almost all of `reads` is unconstrained. On any demand other than those examples, or any `FileSystem` other than `sample`, the loader can do anything. Even for `["LA"]`, it may read every other file too: only membership of the required file is demanded. This does not establish “an import no demand reaches is never read”. library.lth 12-files-and-tools

   For 12.S22/L6.12, the intended privacy test is good as a negative example:

   > `not (member "helper" ...) and not (member "Numpy" ...)`

   but visibility is otherwise only lower-bounded with `allIn`. A loader may expose arbitrary extra private names and still pass, provided they are not literally `"helper"` or `"Numpy"` in this sample. Thus it does **not** establish “sees only what the theory names”. library.lth The actual principle is exact: the importer sees a module “only through the theory it gives the module as type”. principles(20261013-112317)

   More importantly, 12.S22 also requires delayed verification that the demanded file really defines `Numpy` **as a model of `LinearAlgebra`**. `Loader` has no operation or law expressing that check at all. 12-files-and-tools(3)

   For 12.S23, as noted above, `TheoryFileNoExtern` is actively too permissive: actions and foreign models pass. `KindByExtension` also tests only `"a.lth"` and `"dir/b.lut"`, so a loader could classify every other `.lth`/`.lut` backwards and certify. library.lth

   In short, a loader could pass while **misclassifying almost every filename, leaking almost every private name, eagerly reading unrelated files after the first demand, failing to check model-ascription, and accepting actions/models in theory files**.

5. **Roles (L2.7).** The governing principle says a `data` needs laws that state the role of its distinct constructors; merely distinguishing constructors is not enough. principles

   **`Law`: partial.** Every constructor occurs somewhere in a law, but `Forall`, `Exists`, `Either`, and `Then` only get special-case roles rather than their general meaning. So syntactically covered, semantically under-specified.

   **`Evidence`: fails L2.7.** `Listed` has no law whatsoever. `Side` only has a law for `Side true`; nothing states what `false` means. `Drawn` merely says what it cannot do. `At` is only characterized through constant-false/constant-true examples. laws.lth laws.lth

   **`Verdict`: fails L2.7.** `Confirmed`, `Refuted`, and `TakenOn` receive operational roles, but no law ever requires `Supported`, and none requires `Unsettled`. They are presently free tags. laws.lth laws.lth

   **`Reason`: good.** `ReasonOfFirst` distinguishes both `ok` and `failed` and states exactly when each is produced. checks.lth checks.lth

   **`FileKind`: nominally present, substantively weak.** Both constructors occur in `KindByExtension` and the admission laws, but their general extension role is not stated—only two literal filenames—and `TheoryFile`'s admissibility role contradicts 12.S23 by reducing it to “no extern”. library.lth library.lth

6. **What I would change first.** Fix **`Settling` in `laws.lth`** first: replace the example-specific rules by constructor-complete, form-directed laws that can distinguish exhaustive/listed/sampled `forall` evidence and carry the actual cost of an existential witness.

   Reason: this is not merely missing coverage in one loader example. `Settling` is supposed to define what certification *means*, and presently an implementation can satisfy it while refuting a `forall` without a counterexample, never giving `Supported`, ignoring `Listed`, and being unable even to represent D-2026-10-13-l's non-zero-cost witness. Everything that later calls something “evidence” inherits that ambiguity.