### `world.lth`

1. **Laws that are wrong**: none clear.  
2. **Laws that do not determine what they claim**: `HostObserveChangesNothing` only says two observations at the same places agree: `first == second`. A host whose `observe` writes an undeclared place but returns the same `S` passes. `RecordCrossesByField` only tests one field: `b.callField [(l, f)] l xs == b.callBack f xs`; a model ignoring other fields passes.  
3. **Roles (L2.7)**: none; no `data` here.  
4. **The models against their theories**: none clear; see “not sure” on `p = "stdout"`.  
5. **Against the specification**: `10.S7` says a changes-only-declared law is a law of the world’s library, but `Host` only checks agreement on declared places: `Host (S : Concrete) := HostAgreesPrint S & HostAgreesReadFile S & HostObserveChangesNothing S`. It does not enforce that the host action changes only its declared places.  
6. **Implication over a type**: `OwnIsIdempotent` (`not d.own or ...`), `ChangesOnlyDeclared` (`memberStr p d.places or ...`), `ProvisionalIsAssumed` (`not r.provisional or ...`), `IdentityCarriesHash` (`h == k or ...`), `ReadGivesThePlace` (`p == c.stdout or ...`) all quantify over a type and use a rarely-met premise.  
7. **What you would change first**: add a host-action changes-only-declared law; without it `Host` does not certify the host against the description.  
8. **Cutoffs**: none.  
9. **Certifying the host**: missing law that each host action changes only its declared places, and that `observe` itself changes nothing beyond returning the representation. `HostObserveChangesNothing` is too weak.

### `world_model.lut`

1. **Laws that are wrong**: none clear.  
2. **Laws that do not determine what they claim**: none clear.  
3. **Roles (L2.7)**: none.  
4. **The models against their theories**: none clear; see “not sure” on `readFileDescribed "stdout"`.  
5. **Against the specification**: none clear.  
6. **Implication over a type**: none.  
7. **What you would change first**: none.  
8. **Cutoffs**: none.  
9. **Certifying the host**: not applicable here; the missing host law is in `world.lth`.

### `certification.lth`

1. **Laws that are wrong**: none clear; `AFailureRefutes` is incomplete but not false.  
2. **Laws that do not determine what they claim**: `WeakestAcrossBindings` and `StrongestUnderOneBinding` only constrain certificates with `c.entries == nil`; a wrong `grade` can return `just Proved` for any non-empty certificate with a pass and satisfy every law. Quote: `not (c.entries == nil and e.law == c.law ... )`.  
3. **Roles (L2.7)**: `Value` is a `data` with no law of its constructors’ roles: `Value : U := data { Number : Float64 -> Value ; Printed : String -> Value }`.  
4. **The models against their theories**: not applicable.  
5. **Against the specification**: `6.S6` says a certificate holds law, domain, bound, evidence and identity; here `Certificate = { law : String, cone : Hash, entries : List Entry }` stores none of domain, bound, evidence, identity directly.  
6. **Implication over a type**: many laws are `not P or Q` over broad types, e.g. `OnlyAPassServes` (`not (k.serves d e) or e.outcome == Passed`), `ServesAtTheCutoff`, `CertifiesOnlyUnderItsBinding`, `ACoveringPassServes`, `ServesIsMonotoneInTheCutoff`.  
7. **What you would change first**: rewrite the grade laws so they constrain all certificates, not only `c.entries == nil`.  
8. **Cutoffs**: none; `Demand.accepts` is the parameter.  
9. **Certifying the host**: not applicable.

### `certification_model.lut`

1. **Laws that are wrong**: none clear.  
2. **Laws that do not determine what they claim**: none clear; the underdetermination is in the theory, not this model.  
3. **Roles (L2.7)**: none.  
4. **The models against their theories**: none clear; the `hashing` extern is unverifiable here.  
5. **Against the specification**: none clear.  
6. **Implication over a type**: none.  
7. **What you would change first**: none.  
8. **Cutoffs**: none.  
9. **Certifying the host**: not applicable.

### `10-world.md`

1. **Laws that are wrong**: none.  
2. **Laws that do not determine what they claim**: none.  
3. **Roles (L2.7)**: none.  
4. **The models against their theories**: none.  
5. **Against the specification**: none in the chapter itself; the gap is in `world.lth` against `10.S7` and `10.S10`.  
6. **Implication over a type**: none.  
7. **What you would change first**: none.  
8. **Cutoffs**: none.  
9. **Certifying the host**: not applicable.

### `06-certification.md`

1. **Laws that are wrong**: none.  
2. **Laws that do not determine what they claim**: none.  
3. **Roles (L2.7)**: none.  
4. **The models against their theories**: none.  
5. **Against the specification**: the chapter’s `6.S6` says a certificate holds law, domain, bound, evidence and identity; `certification.lth` contradicts this with `Certificate = { law, cone, entries }`.  
6. **Implication over a type**: none.  
7. **What you would change first**: none.  
8. **Cutoffs**: none.  
9. **Certifying the host**: not applicable.

## Not sure

- Cannot verify the Python host implementations behind `world_model.lut` (`observe`, `print`, `readFile`), so `HostAgreesPrint` and `HostAgreesReadFile` cannot be confirmed.
- `world_model.lut` may break `HostAgreesReadFile` at `p = "stdout"` if a file named `"stdout"` exists, because `readFileDescribed "stdout"` describes reading from `files`, while `observe` at place `"stdout"` reads the stdout representation.
- Cannot verify `python:luthier.certify.cone_hash` in `certification_model.lut`, so the `ConeHashing` laws cannot be confirmed.
- Cannot verify `weakest`, `gradeRank` or `Grade` from `test.lth`; they are imported and used but not shown.
- Whether the forward reference to `anyIs` in `certification.lth` is accepted by the parser is not verified here.