## world.lth

**1. Laws that are wrong**
- No law of §1–§4 is false of the pure model (checked in 4). Across the two theories: `AppliedWhenSettled`, `e.applied r h == (r.provisional or settled (e.verdictOf r h))`, makes a provisional extern applied; certification.lth's `ProvisionalIsRefused` makes any cone holding one refused. One runner cannot satisfy both (see 5, and the specification item at the end).

**2. Laws that do not determine what they claim**
- `HostObserveChangesNothing`: `first == second`. Any deterministic `observe` passes — one that writes a marker file at a place outside `places` on each call, or one that ignores the world and returns a fixed `S` (the latter fails only downstream, in `agreement` on `print`). It states "observing twice reads the same", not "changes nothing".
- `Externs`: `Route = { name : String, route : String, provisional : Bool }` carries no type, so no law connects `verdictOf` to the laws of the extern's declared type. Model: `verdictOf r h := if r.provisional then Assumes else Confirmed`, `applied r h := true`, `identity r h := h` — passes all three laws and validates nothing. The comment "An extern whose type has no law to validate against is not applied (L11.3)" has no law.
- `RecordCrossesByField`: `b.callField [(l, f)] l xs == b.callBack f xs` only ever sees a one-field record. `callField fs l xs := callBack (the first field's function) xs`, ignoring `l`, passes.
- `Persistence`: `WriteThenRead` and `WriteChangesOnlyItsPlace` are over the pure `write`; a `Persistence State` whose `write` updates the list passes by construction whether or not the disk persists. What 10.S13 wants assumed (the host's write survives the program) is not what these laws say.
- `Described`: `ChangesOnlyDeclared` bounds what changes; nothing bounds what is read. A description whose result depends on a place outside `places` passes; `agreement` then observes too little (it fails safe in practice, as a disagreement).

**3. Roles (L2.7)** — no `data`. `World (S : Concrete) : { read : S -> String -> Maybe String }` is in theory form with no `World := …`; by the Terms a theory is a structure with its law, so it is an alias as written. `Host.world` and `agreement`'s `(m : World S)` appear in no law's body (`agreement` never uses `m`); `read` and `observe` are related only indirectly, through `HostAgreesReadFile`.

**4. The model against the theory** — by hand: `console` passes the four `Console` laws; `printDescribed s` and `readFileDescribed p` pass `OwnIsIdempotent` (`own := false`) and `ChangesOnlyDeclared`. `host`'s laws need `luthier.host.*`; not evaluable here. There is no `Persistence State`, so §2 has no model and no certificate records its assumption.

**5. Against the specification**
- 10.S8 / L11.2: an extern is name, declared type, route. `Route` has no type (2).
- 10.S13: laws that cannot be tested "marked `assumed`". `Persistence` is a testable law of the representation; the comment's "never a sample" has no mechanism in the file.
- D-2026-10-13-b (each token used once): `match agreement … w0 { (w1, holds) -> holds }` binds `w1` and drops it. The law's `Bool` cannot hand a token on; the comment "the token after is the runner's, which goes on with it" is true of `agreement`, not of `HostAgreesPrint`.
- 10.S10: "refused if the host disagrees (naming the place)". `agreement` returns a bare `Bool`; no place is named.
- 10.S3: `observe : W -> List String -> W * S` takes and gives `W`, so it is an action; "The observation is not an action of the program" is a wish, not a type. Consequence: a world action with no description and no `own`.
- 10.S10 vs 6.S14 on provisional (1): this file follows 10.S10.
- `hash : String -> String`, "the core's, declared here until core names it", is used by no law.

**6. Implication over a type** — none in the wrong direction: `memberStr p d.places or …`, `p == c.stdout or …`, `p == q or …`, `h == k or …` exempt the rare case and test the common one. `not d.own or …` is vacuous on the model's descriptions, correctly, since all are `own := false`.

**7. Change first** — `agreement` returns `(w3, d.describe before == (after, x))` and drops `x`. The comment says "the action the protocol applies is the one the program asked for, applied once"; then `readFile w p` gets no `Maybe String` from the protocol. Either the world action runs twice (against 10.S6) or the result comes from somewhere `agreement` does not return. Return `(w3, x, holds)`, or state that the runner takes `resultOf (d.describe before)` (which `holds` guarantees equal). Reason: without it §5 cannot be what run.py evaluates, and the file says it is.

**8. Cutoffs** — none written as constants. The fixed sizes in laws (`[(l, f)]`, two observations) are coverage, not cutoffs; the literal `"stdout"` is a name (see world_model.lut 8).

**9. Certifying the host** — missing:
- (a) The host's counterpart of `ChangesOnlyDeclared`. `agreement` observes `d.places` before and after, so a host that also writes an undeclared place agrees with its description. §1's "an action that writes where nothing was declared is seen" holds of the description, not of the host. A law `HostChangesOnlyDeclared (o) (d) (host) (q : String) (w0)`: observe `cons q d.places`, act, observe, require `o.world.read after q == o.world.read before q` when `q` is not in `d.places`; the runner chooses `q` (the places the run has touched so far, a sample of paths), since no sampler draws `w0`.
- (b) A way for the one case to be an entry, and for `run` to start. certification.lth: "`run` starts only on a value of this type" (`Certified`) — every law of every cone name needs a serving entry before the run; `Host`'s laws take `w0 : W`, which `test` cannot run, so the first `run` of `hello.lut` is refused before the first application can validate. Nothing says a law over `W` is demanded at first application instead; and its `Entry` has no `binding`, no `reach` for `w0`, and a `Demand` with no `given`, so the one case at `s` serves every later `print s'`.
- (c) `HostObserveChangesNothing` is never scheduled: a law runs "the first time a run asks for the action", and no program asks for `observe`. If it is meant to run at the protocol's own first `observe`, say so.
- (d) The §2 assumption is not attached to `host`; `OwnIsIdempotent` has no host counterpart (not needed by this slice).

## world_model.lut

**1.** None. **2.** n/a. **3.** No `data`. **4.** See world.lth 4. **6.** n/a. **9.** See world.lth 9.

**5.** `observe w places` "reads the standard output and the files at `places`": stdout is observed whether or not declared, so for `readFileDescribed p` the observation exceeds `places`, and for `printDescribed s` the `["stdout"]` is redundant to it. Not wrong, but the theory says the observation is at `d.places`. Also `State` holds only observed files, so `theWorld.read st p == nothing` means absent *or* unobserved; harmless for the pure laws, worth a line.

**7.** `theWorld.read := fn st p { if p == "stdout" then just st.stdout else lookupFile st.files p }` special-cases the standard output while `console.readFile := fn p st { (st, lookupFile st.files p) }` does not; that is why `ReadGivesThePlace` needs `p == c.stdout or …` (refuted without it, as the [proposed] note says). Make stdout a place like any other (one map of places) and the exemption in the theory can go. Reason: an exemption in a theory that exists to fit one model's representation is the model leaking into the theory.

**8.** `"stdout"` appears three times (`theWorld.read`, `console.stdout`, `printDescribed`'s `places := ["stdout"]`); the laws agree by coincidence of the literal. `console.stdout` should be the source of the other two.

## certification.lth

**1. Laws that are wrong**
- `HashSeesTheCode`, `HashSeesTheHost`, `HashSeesTheInterpreter` state injectivity of `h.hash`, false of every hash by pigeonhole; the comment accepts it ("a sample that finds one refutes the model"). Fine as a sampled Boolean law, never provable.
- `ProvisionalIsRefused` vs world.lth `AppliedWhenSettled` (world.lth 1).
- No pair jointly unsatisfiable that I can find; the model satisfies all 22 by hand (certification_model.lut 4).

**2. Laws that do not determine what they claim**
- `grade` beyond two entries: `WeakestAcrossBindings` and `StrongestUnderOneBinding` fire only when `c.entries == nil`, i.e. on exactly two passes. Wrong model: the file's `grade` for ≤ 2 counting passes, the strongest overall for ≥ 3 — passes every law.
- `Entry = { … grade : Maybe Grade … }` is stored; no law relates it to `e.evidence` or `e.reach`. A tester that writes `Proved` for a sampled run passes every law of `Certifying` and of `Store` (`gradedAsOutcome` checks only `Passed` ↔ `just`). The theory determines the reader, not the writer.
- `record` (6.S8 "never edits", 6.S15 "idempotent") is a definition outside `Certifying`; the host's store writer is held to nothing.
- `RefusalIsPerLaw`: `k.refuse es [{ name := n, provisional := false, laws := nil }] == nil` — a name with no laws is never refused; for an extern this is 10.S10's "not applied" case (5).
- `Entry.cases` "which 7.S12 compares with the cases evaluated": no law here compares.

**3. Roles** — all four `data` have role laws: `Value` (`Number` has an order, `Printed` only equality) and `Reach` in `ReachesAsSets`; `Outcome` in `OnlyAPassServes`, `AFailureRefutes`, `NotRunAddsNothing`; `State` in `RefusalSaysWhy` (three) and `ProvisionalIsRefused`. `Value`'s comment should cite `ReachesAsSets`, where its roles live.

**4.** See certification_model.lut 4.

**5. Against the specification**
- 6.S7 / D-2026-10-12-r: "The grade is computed, not stored apart." Each entry stores `grade : Maybe Grade`; only the certificate's grade is computed.
- 10.S10: "An extern with no type to validate against is not applied." `laws := nil → nil` lets it run (2); `ConeName` cannot tell an extern from a definition.
- L10.10: "the constructor of `Certificate` is in no interface outside the theory of certification". `Certificate = {…}`, `Entry = {…}`, `withEntry` are plain exported records and functions; `Store` is a predicate any list can be checked against, not an abstract type. (L10.10's status is not in the excerpt.)
- 6.S14 / `Certified` as a precondition of `run` vs 10.S10's validation at first application (world.lth 9b).
- 6.S11's `c ⊕ c′` and 6.S15's two cutoffs are holes under D-2026-10-14-c, as the file says; `entryBound`, `entryEvidence` are declared and unused — fine.

**6. Implication over a type** — the systematic defect of the file. Every law whose premise needs `e.law == c.law and e.cone == c.cone`, `k.serves d e`, or `e.law == d.law and not (k.stale d.cone e)`, with `e`, `c`, `d` drawn independently, meets it with probability ≈ 0 (two random strings must coincide): `AFailureRefutes`; `WeakestAcrossBindings` (also `c.entries == nil`, two `Passed`, `e.grade == just g`); `StrongestUnderOneBinding` (also `e.binding == f.binding`); `StaleCertifiesNothing`, `OnlyAPassServes`, `CertifiesOnlyUnderItsBinding`, `ServesAtTheCutoff` (consequent trivially true on what is drawn); `ACoveringPassServes`; `ServesIsMonotoneInTheCutoff`. As sampled, a `serves` that serves a `Failed` entry passes. Quantify over the subtype: draw `(l : String) (h : Hash) (b : List Drawing) (g : Grade)` once and build `c`, `d`, `e`, `f` sharing them. Weaker cases of the same: `NotRunAddsNothing` (same-law `NotRunFor` rarely drawn), `RefusalSaysWhy` (`Current`/`Stale` branches rarely reached), `TransportOnTheIntersection` (parameter names of `b.on`, `i.on`, `given` rarely coincide, so `meet` is rarely exercised).

**7. Change first** — 6. Reason: as tested, the theory says next to nothing about `serves` and `grade`, so `certifying` would be certified with `serves` never tried on a matching entry.

**8. Cutoffs** — `accepts : Grade` is the demand's. None as constants; `coversAll`'s `nothing -> false` is a Boolean policy reading, marked [proposed], not a cutoff. The chapter's "up to four" (6.S8) rightly does not appear.

**9.** The certification side of world.lth 9b: what `binding`, `reach` and `grade` an entry has for a law the runner evaluates once at the action's arguments, and that `Certified` defers such laws to first application, is unstated.

## certification_model.lut

**1.** None. **2.** n/a. **3.** No `data`. **6.** n/a. **8.** None. **9.** See certification.lth 9.

**4.** By hand against all 22 laws: `grade` (`NoEntryNoGrade`, `AFailureRefutes`, `OnlyCurrentEntriesCount`, `NotRunAddsNothing`, both two-entry cases, assuming `weakest x x == x`); `serves`; `refuse` (`ProvisionalIsRefused`, `RefusalSaysWhy`, `RefusalIsPerLaw`); `contains` (`ReachesAsSets`); `transport` (`meet` is an intersection on `contains` for every constructor pair, so `TransportOnTheIntersection`, `NoEvidenceForFree`, `PathNeverRaises` hold). No break found. `hashing` needs `luthier.certify.cone_hash`.

**5.** "the host's certify.py, tester.py and `run`'s refusal are its specimen (6.S16, L14.3)" — the only route in the file is `cone_hash`; the reader and writer of `x.cert.json` are no extern here, so nothing of certify.py is validated against `Certifying` (contrast `host` in world_model.lut).

**7.** Give the store reader (and the writer, once the theory has one) as externs of a host model, as world_model.lut does for `print`. `emptyStore : Store certifying := nil` is the only store value, so the specimen is described, not held.

## On the specification (separate)

- 10.S10 vs 6.S14 on provisional: 10.S10 makes `extern provisional` the exception that is applied, as debt; 6.S14 refuses a cone with one, on D-2026-10-12-y, whose provisional part is "the model's reading, not answered". The two theory files split along the two sentences; D-2026-10-13-ad (sonolocalización runs uncertified) needs 10.S10's.
- 10.S10's validation at first application, with the program's arguments, is one case. With no `given` in the demand of later applications, that case serves all of them: grade `cases` on one point, read as `proved`. Either each application's demand carries its arguments (served only when the reach covers them), or the chapter says the host is trusted after one case.
- 6.S7 says the grade is derived; D-2026-10-14-c says first Boolean. The chapter should carry the decision's reading as its status, or files will keep storing what the chapter says is computed.

## Not sure

- `gradeRank` direction (I read higher = stronger from `ServesAtTheCutoff`); that `weakest x x == x`.
- `Verdict` constructors: `Cites r` with an argument, `Assumes` nullary.
- A record field typed by another field of the same record (`printDescribed : String -> Described S Unit world`).
- Whether an unused match-bound `W` (`w1`) is an error for the checker; whether "used once" is linear or affine.
- Generators for `State`, `Term` (the `ConeHashing` laws), functions (`f : A -> B` in `Crossing`), and functions into theories (`printDescribed : String -> Described …` — does `test` sample `s`?).
- The Python side: `observe`'s capture of stdout, the order of `files` (structural `==` on lists is order-sensitive), `print_line`'s newline.
- 7.S9–7.S15, 12.S11, 12.S17, 12.S18, 3.S23, 3.S34, 4.R5, D4/D8 of the archived plan, L11.3: cited, not in the material.
- `gradeOfOldName`: `"bounded"` → `ExhaustiveGrade`, `"witnessed"` → `Cases`.
- Whether `hashing` must itself be certified before any cone's hash is computed (the hash of the cone that holds `cone_hash`).
- Theories indexed by values (`Store (k : Certifying)`, `Described … (m : World S)`) in the grammar.
- Whether `Described`'s `(A : U)` should be `(A : Concrete)`, since `agreement` compares `S * A` with `==`.

I can put this in a markdown file for `record/IA/` if you want.