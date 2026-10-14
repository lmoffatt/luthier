# Review

I reviewed all six files at commit `055589c`. The numbered findings below apply directly to the four Luthier files; the two specification chapters are treated as normative references, with internal specification tensions called out separately as requested.

---

## 1. `world.lth`

1. **Laws that are wrong**

   None is demonstrably false of the intended console model.

   A kernel-semantics concern is recorded under “not sure” below: both `HostAgreesPrint` and `HostObserveChangesNothing` ultimately discard a token.

2. **Laws that do not determine what they claim**

   - An extern’s declared type is absent:

     > `Route = { name : String, route : String, provisional : Bool }`

     and

     > `AppliedWhenSettled (e : Externs) (r : Route) (h : String) : Bool :=  
     >   e.applied r h == (r.provisional or settled (e.verdictOf r h))`

     A model such as

     ```text
     verdictOf r h = if r.provisional then Assumes else Confirmed
     applied r h = true
     identity r h = appendStr r.route h
     ```

     passes all three `Externs` laws, including routes whose declared type has no laws. The theory therefore does not express “an extern with no type to validate against is not applied.”

   - `OwnIsIdempotent` checks only the state, not the full result:

     > `not d.own or stateAfter S A (d.describe (stateAfter S A (d.describe s))) == stateAfter S A (d.describe s)`

     An own action can leave the same store while returning a different `A` on the second application. That is not enough for the action to be memoizable as an action result.

   - `RecordCrossesByField` tests only the one-field record:

     > `b.callField [(l, f)] l xs == b.callBack f xs`

     A bridge that handles `[(l, f)]` but returns `([], 0)` for every multi-field record passes this law, although D-2026-10-14-a says a record crosses “with each function a callback.”

3. **Roles**

   There is no `data` declaration in this file, so the narrow L2.7 constructor rule finds nothing.

   If the principle is also meant to cover record fields, `Route.route` has no role law: none of the `Externs` laws constrains behavior by route.

4. **The models against their theories**

   Not applicable here; see `world_model.lut`.

5. **Against the specification**

   - 10.S8 says:

     > “An extern has a name, a declared type and a route to a host function”

     but `Route` contains no declared type or laws. Consequently 10.S10’s

     > “An extern with no type to validate against is not applied”

     is unrepresentable.

   - 10.S6 calls own actions “idempotent and memoizable.” The law implements only same-store idempotence, not same-result memoizability.

6. **Implication over a type**

   - `OwnIsIdempotent` is guarded by `not d.own`; random described actions will usually be world actions, so the own-action case is rarely reached. Quantify over an `OwnDescribed` subtype with `d.own == true`.
   - `ProvisionalIsAssumed` is guarded by `not r.provisional`; most random routes are non-provisional. Quantify over provisional routes.
   - The place laws such as `ChangesOnlyDeclared` are correctly shaped: a random place is usually undeclared, which is exactly the case whose preservation is being tested.

7. **What I would change first**

   Strengthen `Host` so its descriptions cannot be self-serving. Either parameterize `Host` by `Console S` or add laws requiring `printDescribed` and `readFileDescribed` to satisfy the `Console` laws. Otherwise agreement can be certified against a description chosen to match the host, even when both are wrong.

8. **Cutoffs**

   None found. No tolerance, resolution, convergence threshold, rank floor, or level is written as a constant.

9. **Certifying the host**

   The missing law is a **description-validity law**, approximately:

   ```text
   HostDescriptionsSatisfyConsole
   ```

   requiring each host-supplied description to satisfy the corresponding `Console` laws—or requiring the descriptions to be the console operations themselves.

   This no-op model passes every current `Host` law:

   ```text
   bad.print w s = (w, unit)

   bad.printDescribed s = {
     describe = fn st { (st, unit) },
     own = false,
     places = ["stdout"],
   }

   bad.readFile w p = (w, nothing)

   bad.readFileDescribed p = {
     describe = fn st { (st, nothing) },
     own = false,
     places = [p],
   }
   ```

   Both descriptions satisfy the weak `Described` theory, and both agreement laws compare the host action with those same no-op descriptions. The observation law can still hold. Yet the intended `print` must append a line and `readFile` must read the place.

   There is a second scope gap: `agreement` observes only `d.places`. A host action that also changes an undeclared place escapes the protocol. Either observation must cover every place in the representation, or the action’s declared places must come from an independently checked declaration rather than from the same model being certified.

---

## 2. `world_model.lut`

1. **Laws that are wrong**

   Not applicable; this is a model file.

2. **Laws that do not determine what they claim**

   No model-local under-determination beyond the theory-level gaps above.

   In particular, the model correctly instantiates the descriptions from `console`:

   > `describe := console.printLine s`

   and

   > `describe := console.readFile p`

   but that is stronger than what `Host` currently requires.

3. **Roles**

   `State` is a record/alias, not a `data`; no constructor-role finding.

4. **The models against their theories**

   I find no pure law that `console`, `printDescribed`, `readFileDescribed`, or the representation itself breaks:

   - `printLine` appends `lineOf s` to `stdout` and leaves `files` unchanged.
   - `readFile p` returns `lookupFile st.files p` and leaves the state unchanged.
   - `printDescribed` declares only `"stdout"`.
   - `readFileDescribed p` declares only `p`.

   The three `HostAgrees`/`HostObserveChangesNothing` laws depend on the behavior of the Python routes:

   > `observe := extern "python:luthier.host.observe"`  
   > `print := extern "python:luthier.host.print_line"`  
   > `readFile := extern "python:luthier.host.read_file"`

   Those routes are not in the supplied material, so I cannot certify those three laws from the files.

5. **Against the specification**

   Nothing in the model contradicts chapter 10. Its comments match the intended first model of 10.S13.

6. **Implication over a type**

   None in this file.

7. **What I would change first**

   Do not change this model first. After `Host` is strengthened, instantiate the stronger theory here so the host remains explicitly tied to `console`.

8. **Cutoffs**

   None found.

9. **Certifying the host**

   Not applicable here; the missing law belongs in `world.lth`.

---

## 3. `certification.lth`

1. **Laws that are wrong**

   I find no internally unsatisfiable set of laws.

2. **Laws that do not determine what they claim**

   The aggregate grade of three or more passes is underdetermined. Both binding laws are explicitly restricted to an empty certificate:

   > `not (c.entries == nil and e.law == c.law ... ) or  
   >   k.grade (withEntry (withEntry c f) e) == just (weakest g h)`

   and similarly for `StrongestUnderOneBinding`.

   Let `grade0` be the reference algorithm in `certification_model.lut`. A model can instead use:

   ```text
   grade3 c =
     if anyFailure c c.entries then nothing
     else if at least three current passes occur in c.entries then just Proved
     else grade0 c
   ```

   This passes:

   - `AFailureRefutes`;
   - `OnlyCurrentEntriesCount` for non-current entries;
   - `NotRunAddsNothing`;
   - both two-entry binding laws, because their premises force `c.entries == nil`.

   Yet with three passes graded `Cases`, `Sampled`, and `Cases`, it upgrades the certificate to `Proved`, contrary to the stated rule that the grade across bindings is the weakest.

   More generally, the laws constrain only selected two-entry additions. They should define the fold for any list of current passes, or make `grade` an ordinary canonical definition rather than an unconstrained model operation.

3. **Roles**

   `Value` has no explicit constructor-role law:

   > `Value : U := data {  
   >   Number : Float64 -> Value ;  
   >   Printed : String -> Value ;  
   > }`

   `ReachesAsSets` uses `Number x` and `Printed s` as examples, but no law states the role of the two constructors as numeric versus printed-canonical values.

   More weakly, the payload roles of

   > `Failed : String -> Outcome`  
   > `NotRunFor : String -> Outcome`

   are not constrained. Nothing requires the first string to be the printed counterexample or the second to be the reason, although the comments assign those roles.

4. **The models against their theories**

   Not applicable here; see `certification_model.lut`.

5. **Against the specification**

   Literal tension with 6.S8:

   > “A new check never edits an entry: it writes a new one, and both are kept, the latest in front.”

   whereas:

   > `record (k : Certifying) (e : Entry) (st : Store k) : Store k :=  
   >   match known k (k.identity e) st { just f -> st ; nothing -> cons e st }`

   drops a later entry whose identity is already present. The file marks its contrary rationale as `[proposed]`; nevertheless it does not implement the chapter’s literal “both are kept” rule.

6. **Implication over a type**

   Several consequents are guarded by conditions that random generation will rarely satisfy:

   > `not (k.serves d e) or e.outcome == Passed`

   > `not (k.stale d.cone e) or not (k.serves d e)`

   > `not (k.serves d e) or (match e.grade ... )`

   > `not (e.law == c.law and e.cone == c.cone) or ...`

   The exact two-pass premises of `WeakestAcrossBindings` and `StrongestUnderOneBinding` are also unlikely to be met by an unrestricted random entry sampler.

   These should be stated over refined subtypes such as:

   ```text
   ServedEntry k d     := { e : Entry | k.serves d e }
   StaleEntry k h      := { e : Entry | k.stale h e }
   CurrentFailure c    := { e : Entry | current for c and Failed }
   CurrentPass c       := { e : Entry | current for c and Passed }
   ```

   with separate laws for those subtypes.

7. **What I would change first**

   Make certificate grading canonical. Either remove `grade` from the model interface and define it from entries in `certification.lth`, or add an inductive/list-fold law covering every number of current passes. This is the largest soundness hole: the current laws allow a three-entry certificate to be upgraded for free.

8. **Cutoffs**

   None found. The grade cutoff is correctly demand-supplied:

   > `Demand = { ..., accepts : Grade }`

   and compared only through `d.accepts`, not through a constant grade or rank.

9. **Certifying the host**

   Not applicable; the host is certified by `world.lth`.

---

## 4. `certification_model.lut`

1. **Laws that are wrong**

   Not applicable.

2. **Laws that do not determine what they claim**

   Not applicable, but see the theory-level grade under-determination above. The supplied `grade` itself appears to implement the intended weakest-across/strongest-under rule.

3. **Roles**

   Not applicable.

4. **The models against their theories**

   I find no pure law that `certifying` breaks. In particular:

   - `contains` satisfies `ReachesAsSets`;
   - `transport` satisfies the weaker-grade and reach-intersection laws;
   - `serves` matches the stated pass/current-hash/cutoff/reach conditions;
   - `refuse` matches the singleton, provisional, per-law, and state-listing laws;
   - `emptyStore := nil` satisfies both `Store` invariants.

   The host hash remains unverifiable from this file:

   > `hash := extern "python:luthier.certify.cone_hash"`

   Its canonical-form and change-sensitivity laws depend on the Python implementation.

   Possible completeness issue, not counted as a law break: `certification.lth` leaves

   > `C : U`  
   > `entryBound : Entry -> C`  
   > `entryEvidence : Entry -> C`

   as holes, and this model fills none. Given D-2026-10-14-c and D-2026-10-13-m, that may be intentional.

5. **Against the specification**

   No direct contradiction found. The Boolean simplifications are explicitly attributed to D-2026-10-14-c.

6. **Implication over a type**

   Not applicable.

7. **What I would change first**

   Defer model changes until `grade` is made canonical in the theory. Then remove or replace the model-supplied grade algorithm rather than patching this file independently.

8. **Cutoffs**

   None found.

9. **Certifying the host**

   Not applicable.

---

## 5. `10-world.md`

1. **Laws that are wrong**

   Not applicable.

2. **Laws that do not determine what they claim**

   The chapter does not say how agreement at only the declared places can detect a change at an undeclared place. This underlies the host-scope gap in `world.lth`.

3. **Roles**

   Not applicable.

4. **The models against their theories**

   Not applicable.

5. **Against the specification / internal tensions**

   - 10.S4 requires a token with no `==` and uniqueness, while 10.S6 says own actions are memoizable. If a memoized action returns the same token value at a later hit, it is unclear how the token remains unique and used once.
   - 10.S6 says repetition “leaves the same store” and therefore may be memoized. Same store is not enough to memoize the action’s result value.
   - 10.S13 names `lib/world.lut`, while the settled implementation file is `world.lth`; this is cosmetic but should be aligned.

6. **Implication over a type**

   Not applicable.

7. **What I would change first**

   Clarify whether a memoized own action reuses a token, returns a fresh token without running the effect, or is exempt from ordinary token uniqueness.

8. **Cutoffs**

   Not applicable.

9. **Certifying the host**

   The chapter should state that the host’s description is constrained by the world library’s theory—e.g. `Console`—not merely selected by the host model as any inhabitant of `Described`.

---

## 6. `06-certification.md`

1. **Laws that are wrong**

   Not applicable.

2. **Laws that do not determine what they claim**

   6.S8’s “write a new entry and keep both” does not define whether an exact repeat with the same seed, count, cone, and binding is a new check or an idempotent replay.

3. **Roles**

   Not applicable.

4. **The models against their theories**

   Not applicable.

5. **Against the specification / internal tensions**

   Literal tension between:

   > “Doing it twice with the same inputs leaves the same store”

   from D-2026-10-12-m, as used by 6.S15, and 6.S8’s requirement that every new check append a new entry and keep both. The intended behavior needs to distinguish “same check replayed” from “new evidence under a new identity.”

6. **Implication over a type**

   Not applicable.

7. **What I would change first**

   Add one sentence to 6.S8 saying whether an exact identity replay is absorbed by idempotence or recorded as a superseding entry.

8. **Cutoffs**

   The chapter correctly places the cutoff in the demand:

   > “The demand states the cutoff”

   consistent with D-2026-10-12-h and P11.

9. **Certifying the host**

   Not applicable.

---

## Not sure

1. Whether dropping the final token in these laws is legal:

   > `match agreement ... { (w1, holds) -> holds }`

   and

   > `match o.observe w1 places { (w2, second) -> first == second }`

   D4 says each token is used exactly once. If weakening/discarding `W` is forbidden, the `Host` laws are ill-formed rather than merely hard to sample. The file claims the runner keeps the token, but the Boolean law does not return it.

2. Whether unresolved holes such as `C`, `entryBound`, and `entryEvidence` must be filled by every `.lut` model under the current interpreter rules, or may remain open under D-2026-10-14-c.

3. The behavior of the Python routes `luthier.host.observe`, `luthier.host.print_line`, `luthier.host.read_file`, and `luthier.certify.cone_hash`; consequently, the externally dependent `Host` and `ConeHashing` laws cannot be verified from the supplied files.

4. Whether 7.S13 permits two entries with the same identity and outcome but different grades. `agreesWith` compares only:

   > `e.outcome == f.outcome`

   not the full entry or grade.

5. Whether evidence, budgets, date, interpreter, and host hashes are intended to have role laws in this layer. They are fields of `Entry`, but the narrow L2.7 item in the prompt asks specifically about constructors of a `data`.

6. Whether concurrent host-side changes during `observe; observe` are in scope. If they are, `HostObserveChangesNothing` can fail even though the observation itself changed nothing.