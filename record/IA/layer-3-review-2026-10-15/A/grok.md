**world.lth**

1. **Laws that are wrong**: None detected as false of the intended model or jointly unsatisfiable. `OwnIsIdempotent`, `ChangesOnlyDeclared`, `Persistence` laws, `Externs` laws, `Crossing` laws, `Console` laws, and `Host` laws are consistent with the intended representation and protocol.

2. **Laws that do not determine what they claim**: `ChangesOnlyDeclared` quantifies over every `p : String`; a model that mutates an undeclared place only for strings outside the finite sample still passes. `Persistence` laws are similarly under-determined without a finite domain for places. `HostObserveChangesNothing` only checks equality of two successive observations; it does not force the observation itself to be free of side-effects on unobserved places.

3. **Roles (L2.7)**: No bare `data` constructors lacking a role law. `Route`, `World`, `Described`, `Persistence`, `Console`, `Host`, `Crossing` are records; their fields are constrained by the conjunctions that define the theories.

4. **The models against their theories**: Not applicable (theory file).

5. **Against the specification**: Matches 10.S1–10.S13 and the cited decisions (token used once, `own`, places, extern routes, validation at first action, agreement protocol). §6 and §7 remain `todo` as stated. The `appendStr` body is present (proposed).

6. **Implication over a type**: `ChangesOnlyDeclared` and the two `Persistence` laws quantify over `String` with an implication whose premise is rarely met by a random draw; the subtype of declared places (or of places that exist in the representation) should be the domain.

7. **What you would change first**: Make the domain of `ChangesOnlyDeclared` and the `Persistence` laws the finite list of places that appear in the model’s representation (or the action’s declared places), so the quantifier is over a subtype that sampling can exhaust.

8. **Cutoffs**: None; every law is Boolean and carries no constant tolerance/resolution/rank/level.

9. **Certifying the host**: The three `Host` laws (`HostAgreesPrint`, `HostAgreesReadFile`, `HostObserveChangesNothing`) together with the definition of `agreement` are exactly the required agreement of each action with its description. No law is missing for the host to be certified against its description.

**world_model.lut**

1. **Laws that are wrong**: None.

2. **Laws that do not determine what they claim**: The pure descriptions in `console` satisfy `Console` by construction. The host externs are not themselves models of any law inside this file; they rely on the runner’s evaluation of `Host` laws.

3. **Roles (L2.7)**: No `data` constructors.

4. **The models against their theories**: `console` satisfies every law of `Console State` (the descriptions match the pure functions). `host` is an instance of `Host State`; whether its externs satisfy the three `Host` laws can only be checked by the runner at first application (the pure descriptions and the observation are consistent by construction). No concrete counter-example is present in the file itself.

5. **Against the specification**: Conforms to 10.S5, 10.S8–10.S10 and the agreement protocol of §5.

6. **Implication over a type**: None in the model.

7. **What you would change first**: Nothing essential; the model is the minimal concrete specimen expected by the theory.

8. **Cutoffs**: None.

9. **Certifying the host**: The model supplies exactly the fields required by `Host`; the missing piece is only the runtime evaluation of the three agreement laws (already stated in the theory).

**certification.lth**

1. **Laws that are wrong**: None of the Boolean predicates is false of the intended store/certificate model. The conjunction that defines `Certifying` is satisfiable.

2. **Laws that do not determine what they claim**: `WeakestAcrossBindings` and `StrongestUnderOneBinding` are implications whose antecedents are rarely true for a random triple of certificates; a model that returns an arbitrary grade when the antecedents fail still passes. `RefusalSaysWhy` and `RefusalIsPerLaw` fix the shape of the refusal list but leave the concrete state computation free when the “anyServes” premise fails. `TransportOnTheIntersection` only checks coverage equality, not that the intersection is the greatest lower bound under the reach order.

3. **Roles (L2.7)**: `Value`, `Reach`, `Outcome` and `State` are `data` types. Role laws appear only for the store (`determined`, `gradedAsOutcome`) and for the high-level operations; the individual constructors of `Value`/`Reach`/`Outcome`/`State` have no dedicated “role” laws beyond the uses in `ReachesAsSets`, `OnlyAPassServes`, `AFailureRefutes`, `NotRunAddsNothing`, `RefusalSaysWhy` and `ProvisionalIsRefused`. By L2.7 a bare collection of constructors is an alias, not a theory.

4. **The models against their theories**: Not applicable (theory file).

5. **Against the specification**: Conforms to the Boolean specialisation required by D-2026-10-14-c and realises 6.S1–6.S16 (with `C` left as a hole). The grade derivation, transport, `serves`, refusal and cone-hash laws match the chapter. Older grade names are mapped.

6. **Implication over a type**: Several laws (`WeakestAcrossBindings`, `StrongestUnderOneBinding`, `ACoveringPassServes`, `ServesIsMonotoneInTheCutoff`, parts of the refusal laws) are written as implications over the full type of certificates/entries; the subtype of “entries that actually belong to the certificate / that actually passed / that share a binding” should be the quantified domain.

7. **What you would change first**: Supply explicit role laws (or turn the four `data` types into aliases) for the constructors of `Value`, `Reach`, `Outcome` and `State`, satisfying L2.7.

8. **Cutoffs**: None written as constants; the sole cutoff is the grade accepted by a `Demand`, supplied by the demand (D-2026-10-14-c).

9. **Certifying the host**: Not applicable (certification theory, not host).

**certification_model.lut**

1. **Laws that are wrong**: None.

2. **Laws that do not determine what they claim**: The pure functions implement the intended behaviour; a wrong model would have to deviate from the recursive definitions of `grade`, `serves`, `refuse` and `transport`.

3. **Roles (L2.7)**: No new `data` constructors.

4. **The models against their theories**: `certifying` satisfies every law of `Certifying` by construction (identity, stale, grade derivation by weakest-of-bests, contains, serves, refuse, transport). `hashing` is an extern; its four laws are not evaluated inside the model file.

5. **Against the specification**: Matches 6.S6–6.S16 for the Boolean case and the store operations of 7.S9/7.S12/7.S13/12.S11/12.S17.

6. **Implication over a type**: None in the model.

7. **What you would change first**: Nothing essential; the model is the reference specimen.

8. **Cutoffs**: None.

9. **Certifying the host**: Not applicable.

**not sure**
- Whether the host externs in `world_model.lut` (`observe`, `print_line`, `read_file`) and the cone-hash extern actually satisfy their respective theories at runtime (requires the Python implementations and a concrete run).
- Whether the finite-sample behaviour of `ChangesOnlyDeclared` / `Persistence` is considered adequate under the project’s sampling regime.
- Exact interaction of provisional externs with the `Host` agreement protocol when a provisional route is used.
- Whether the missing role laws for the four `data` types in `certification.lth` are regarded as already discharged by the surrounding uses, or must be stated explicitly.