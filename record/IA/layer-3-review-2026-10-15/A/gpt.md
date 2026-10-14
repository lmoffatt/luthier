There are **four blocking issues** in this round: the `Host` “laws” perform actions and lose the world token; `observe` is not anchored to what it claims to observe; certification’s identity omits budgets even though budgets can change an outcome; and `Certifying.grade` is underdetermined. I would fix those before extending either layer.

## 1. `world.lth`

1. **Laws that are wrong.**  
   The strongest defect is in `"HostAgreesPrint ... : Bool :="`, `"HostAgreesReadFile ... : Bool :="`, and `HostObserveChangesNothing`. These are declared as Boolean laws, but evaluating them executes `observe` and a host action. Worse, `HostAgreesPrint` extracts `(w1, holds)` from `agreement` and returns only `holds`, discarding `w1`. A-prompt  
   That contradicts the settled rule that each `W` value is used once A-prompt and the spec's own distinction that evaluation has no effect while an action is identified by taking and returning `W`. A-prompt  
   `agreement` itself is fine as an **action/certifier** returning `W * Bool`; the three `Host...` predicates are not fine as laws.

2. **Laws that do not determine what they claim.**  
   `agreement` trusts `o.observe`. There is no law connecting the `S` returned by `observe` to the places of the actual world that it supposedly represents. `HostObserveChangesNothing` only asks two consecutive observations to agree. A-prompt  
   A wrong host can therefore pass: let `print` write somewhere other than stdout and let `observe` report that place as `State.stdout`. `agreement` sees exactly the fictional state transition predicted by `printDescribed`, although the actual designated stdout was never changed.  
   There is a second incompleteness in `Externs`: the prose says an extern “whose type has no law ... is not applied,” but neither `Route` nor `Externs` contains its declared type or even a `hasLaw` fact. A-prompt L11.2 explicitly requires this condition. A-prompt

3. **Roles (L2.7).**  
   No locally declared `data` occurs here, so I find no L2.7 constructor-role defect in this file.

4. **The model against the theory.**  
   Nothing in the pure part of `world_model.lut` visibly violates `World`, `Described`, or `Console`. The host externs cannot be checked from the supplied material; see the final “not sure” section.

5. **Against the specification.**  
   The principal contradiction is internal to the architecture: §5 turns the *certifier that performs an action* into the *Boolean law being certified*. 10.S1 says definitions have no effect; 10.S3 says an effectful function is recognized by the `W -> ... -> W * A` shape. A-prompt  
   Also, the file claims the lawless-extern condition but cannot express it structurally, as above.

6. **Implication over a type.**  
   `"not d.own or ..."` in `OwnIsIdempotent` tests the interesting case only when a randomly generated `Described` happens to have `own = true`. A-prompt This should quantify over an `OwnDescribed` subtype.  
   Likewise `"not r.provisional or ..."` in `ProvisionalIsAssumed` should quantify over provisional routes. A-prompt

7. **What I would change first.**  
   Separate **law** from **certifier**. Define a pure predicate over an observed action case, roughly `(before, args, after, result) -> Bool`; let `agreement` be the world action that gathers such a case and evaluates the predicate. Never make a law consume `W`.

8. **Cutoffs.**  
   I find no policy cutoff hard-coded as a constant.

9. **Certifying the host.**  
   The missing law/trust boundary is **observation fidelity**. Something must establish that, for each requested `p`, the representation returned by `observe` really denotes the world's observation at `p`. At present `agreement` only proves consistency between the action and the observer; it cannot prove that the observer is telling the truth. This must either be a separately certified observation primitive or an explicitly cited/assumed root of trust.

---

## 2. `world_model.lut`

1. **Laws that are wrong.**  
   None: this file defines models, not new laws.

2. **What is not determined.**  
   The model exposes the hole in `world.lth`: `observe := extern "python:luthier.host.observe"` is simply supplied alongside the actions it is supposed to police. A-prompt Nothing independent anchors that observer.

3. **Roles.**  
   No local `data`; no issue found.

4. **Model against theory.**  
   The pure `console` model appears consistent: `printLine` changes only `stdout`, `readFile` leaves `State` unchanged, and the declared places match those descriptions. A-prompt  
   I cannot verify the three Python externs from these files.

5. **Against specification.**  
   No additional deviation beyond inheriting the defective `Host` certification protocol.

6. **Implication over a type.**  
   None; no laws are declared here.

7. **What I would change first.**  
   Do not change `console` first. Fix `world.lth`, then make this model supply whatever separate evidence/assumption the new observation-fidelity requirement needs.

8. **Cutoffs.**  
   None.

9. **Certifying the host.**  
   The model currently supplies a route to `observe`, but no independent reason to believe that route observes the claimed places. That is exactly the missing certificate.

---

## 3. `certification.lth`

1. **Laws that are wrong.**  
   `Identity` omits `budgets`:

   `Identity = { law, cone, binding, seed, cases }`

   while `Entry` separately contains `budgets`, and `Outcome.NotRunFor` explicitly includes cases such as fuel being exhausted. A-prompt Yet `Store` requires two entries with the same identity to have the same outcome. A-prompt

   Counterexample: run the same law/cone/binding/seed/cases with a tiny fuel budget → `NotRunFor "fuel"`; repeat with enough fuel → `Passed`. Same `Identity`, different `Outcome`; the intended store violates `determined`.

2. **Laws that do not determine what they claim.**  
   `grade` is underdetermined. There is a law for an empty certificate, failures, irrelevant entries, two passing entries under equal/different bindings—but **no law says what the grade of one current `Passed` entry is**. A-prompt  
   A wrong `Certifying` can therefore return `nothing` for `{entries := [one current Passed entry]}`, behave correctly on the special cases appearing in the laws, and pass every stated `grade` law.

   `Store` is also claimed to have “the latest in front,” but its refinement only requires `determined` and `gradedAsOutcome`; there is no ordering law. A-prompt A reversed historical list is therefore a valid `Store`, after which `latestOf` can return the wrong entry.

3. **Roles (L2.7).**  
   This is substantially good. `Reach` gets semantics from `ReachesAsSets`; `Outcome` gets distinct roles through pass/failure/not-run laws; and `State` is interpreted by `RefusalSaysWhy` plus `ProvisionalIsRefused`. A-prompt I do not see a constructor that is merely enumerated with no role.

4. **The model against the theory.**  
   Addressed under `certification_model.lut` below.

5. **Against the specification.**  
   `record` conflicts with the frozen-certificate chain. It says an already known identity leaves the store unchanged, even under `--deep`. A-prompt L10.4 says a later check issues a new certificate, keeps both, and puts the latest in front. A-prompt

   Also, §5 is marked “done”, but the current file does not implement the `CostAlgebra C`, cost-valued bound/evidence, or `compose` required by 6.S16; `entryBound` and `entryEvidence` are just holes and are not laws of `Certifying`. A-prompt The later Boolean-first decision explains why that implementation is deferred, but the file should not simultaneously present the section as complete.

6. **Implication over a type.**  
   The worst offenders are `WeakestAcrossBindings` and `StrongestUnderOneBinding`: each has a long conjunction including `c.entries == nil`, matching law/hash, two passes, two grades and equal/unequal bindings. A random tuple almost never exercises the consequent. A-prompt  
   `AFailureRefutes`, `ACoveringPassServes`, and `ServesIsMonotoneInTheCutoff` have the same testing problem to lesser degrees. A-prompt A-prompt  
   These should quantify over constructed subtypes such as “two current passing entries under different bindings.”

7. **What I would change first.**  
   Fix the identity/cache semantics around `budgets` and `NotRun`. Either budgets participate in identity, or `NotRun` must not be memoized as a deterministic known outcome. As written a low-resource attempt can poison the identity of a later viable check.

8. **Cutoffs.**  
   No hard-coded numerical cutoff found. `Demand.accepts` is supplied as data, which is consistent with P11. The current Boolean-first decision explicitly requires criteria to remain parameters. A-prompt

9. **Certifying the host.**  
   No additional host-specific law belongs here. This layer should record the evidence generated by the corrected world certifier; it should not itself make `observe` trustworthy.

---

## 4. `certification_model.lut`

1. **Laws that are wrong.**  
   No new laws are declared.

2. **What is not determined.**  
   No new underdetermination beyond that of `Certifying`; this model happens to choose the sensible missing behavior for one-pass certificates, but another model need not.

3. **Roles.**  
   No new `data`.

4. **Model against theory.**  
   For the code visible here, `identity`, `stale`, `contains`, `grade`, `serves`, `refuse`, and `transport` appear to satisfy the stated laws. In particular, `grade` actually does compute a grade for a single passing entry, even though the theory never requires it. A-prompt  
   I found no concrete counterexample against the written `Certifying` laws.

   `hashing` cannot be verified because its implementation is external. A-prompt

5. **Against the specification.**  
   The model confirms a design mismatch: `serves` is `Demand -> Entry -> Bool`, while 6.S15 speaks about a **certificate** serving a demand. A-prompt This becomes important once several entries jointly produce quantitative evidence; the current Boolean slice can mostly hide the mismatch.

6. **Implication over a type.**  
   N/A; implementation, not laws.

7. **What I would change first.**  
   After fixing the theory's identity, make `known`/store behavior correspond to that choice. In particular, don't let a budget-dependent `NotRun` become a permanent cache hit for a later better-funded test.

8. **Cutoffs.**  
   None hard-coded.

9. **Certifying the host.**  
   `cone_hash` remains an extern and therefore itself needs whatever ordinary extern certification applies. No host-observation issue is solved here.

---

## 5. `10-world.md`

1. **Laws that are wrong.**  
   N/A as executable laws.

2. **What it fails to determine.**  
   The chapter never states the missing observation-fidelity obligation. 10.S13 says a library supplies representations, observations and laws, but does not say what establishes that a host observation corresponds to the real designated place. A-prompt

3. **Roles.**  
   N/A.

4. **Models against theories.**  
   N/A.

5. **Against decisions/specification.**  
   There is one direct wording error in 10.S5:

   > `act ... gives a new token each time, so two applications to one token are two nodes`

   A-prompt

   Under the settled uniqueness decision, **two applications to one token must be illegal**, not merely distinct DAG nodes. Each `W` value is used once. A-prompt

   More importantly, 10.S10/10.S12 are not reconciled with strict certification. 10.S12 says an extern “with no law yet may run in a named world,” while 6.S14 says a demand has no opt-out and a provisional or uncertified cone is refused. A-prompt A-prompt L10.6 says such an exception waits for an actual O3 case. A-prompt  
   Unless 10.S12 is explicitly that O3 mechanism, the two clauses cannot both govern `run`.

6. **Implication over a type.**  
   N/A; this chapter states specification clauses, not tested predicates.

7. **What I would change first.**  
   Amend §5/§6 so that it distinguishes three things cleanly: the pure law describing an action, the effectful certifier that observes an action, and the trust/certificate of the observation itself. Then resolve whether 10.S12 is O3 or remove its claim that an uncertified extern may run.

8. **Cutoffs.**  
   No hard-coded cutoff found; the named-world choice is explicitly a demand parameter.

9. **Certifying the host.**  
   Add the observation trust/fidelity requirement to this chapter. Otherwise `agreement` can certify only **agreement with an observer**, not agreement with the world.

---

## 6. `06-certification.md`

1. **Laws that are wrong.**  
   N/A as executable laws.

2. **What it fails to determine.**  
   The chapter itself is reasonably determinate at the cost-algebra level; the incompleteness is mainly that the current `.lth` has not implemented what this chapter says.

3. **Roles.**  
   N/A.

4. **Models against theories.**  
   N/A.

5. **Against current decisions/specification.**  
   This chapter is now **stale with respect to D-2026-10-14-c**. It still presents cost-valued laws, bound/evidence costs, `C`, `⊕`, and cost cutoffs as the current certification theory. A-prompt The later decision says: first every law is Boolean, cutoffs stay exposed as demand-supplied parameters, and `Distance`/`Evidence` come later after failures teach what is required. A-prompt

   6.S16 is also mechanically stale: it says `lib/certification.lut` “is not written,” whereas this snapshot now contains `certification.lth` plus `certification_model.lut`; and it requires `CostAlgebra`, `compose`, cost-valued `serves`, etc., which the current theory does not yet provide. A-prompt

6. **Implication over a type.**  
   N/A in this prose chapter.

7. **What I would change first.**  
   Update this chapter to state the **current Boolean slice explicitly**, and move the `C` architecture into a “next refinement” subsection. At present `certification.lth` looks non-conforming partly because the controlling spec predates the later decision.

8. **Cutoffs.**  
   No constant cutoff: the chapter consistently places cutoffs in the demand. The problem is not P11; it is that the chapter still expresses them through the pre-D-2026-10-14-c cost formulation.

9. **Certifying the host.**  
   N/A; certification should record host-certifier evidence, not supply the missing observation semantics.

## What I would fix, in order

1. **World:** stop treating `HostAgrees*` as effectful Bool laws. Make `agreement` a certifier action over a pure agreement predicate, preserving the returned `W`.
2. **World:** establish a root of trust/law for `observe`; otherwise the Host theorem is circular.
3. **Certification:** fix `Identity` versus `budgets`/`NotRun`, including cache semantics.
4. **Certification:** add the missing single-pass law for `grade`, and a real “latest-first” invariant for `Store`.
5. **Specs:** update `06-certification.md` for the Boolean-first decision and resolve 10.S12 versus strict 6.S14.
6. Only then fill the cost/evidence layer.

## Not sure

I cannot verify the behavior of `python:luthier.host.observe`, `print_line`, `read_file`, or `python:luthier.certify.cone_hash`, because their host implementations are not included here. I therefore cannot assert that either model's externs actually satisfy their theories.

I also cannot determine from these six files whether Luthier permits the forward references/cycles such as `Store (k : Certifying)` before `Certifying` is declared; that is a type-check/static-semantics question, and the prompt explicitly says these files have not type-checked yet.

Finally, I cannot verify whether `Supported` and `Cites` are correctly classified as `settled` without the imported `laws.lth`; I therefore did not flag that choice.