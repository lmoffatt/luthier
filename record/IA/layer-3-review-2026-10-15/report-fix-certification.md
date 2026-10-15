# Report: certification.lth after round 1

2026-10-15, by Claude Opus 5.5, an agent of the coordinating session, on
`prompt-fix-certification.md` of this folder. Inputs: `summary.md` (top screen, certification.lth
and certification_model.lut sections), `certification.lth` and `certification_model.lut` at
eeeb694, D-2026-10-14-c. Outputs: 262d3d3 (certification.lth, draft 1), 82c4cb4
(certification_model.lut). Every law stays Boolean; no cutoff became a constant.

Numbering. The brief's numbers are shifted against `summary.md`'s for four items. I followed the
descriptions: brief C3 is summary C2 (implications over a type), brief C7 is summary C6 (an
entry's grade tied to nothing), brief C10 is summary C11 (the latest in front), brief C8 is
summary C9 (the roles of `Value`), and the two left for Luciano (brief C2, C4) are summary C3
(`record`) and C4 (budgets). Below, "C" numbers are summary.md's.

## Accepted when

- Both files parse (`luthier parse`, exit 0) and `luthier check` is clean on both, and on
  demand.lth, demand_model.lut, plan.lth and plan_model.lut, which import certification.lth.
- `PYTHONPATH=src python3 -m pytest tests/test_certify.py tests/test_run.py -q`: 159 passed at
  eeeb694 before my edits. At HEAD it fails 32 to 42 tests (the count moved while world.lth was
  being edited alongside), every one a `run` refused on `host`'s laws, stale or uncertified
  (`HostAgreesPrint` stale, `HostChangesOnlyDeclared` and `ObserverIsFaithful` with no entry),
  which follows from 2ac8f12 and 44578c4 (world.lth, world_model.lut) and an uncertified
  world_model store. Control: a copy of the working tree with my two files at HEAD's version fails
  43; every test that fails with my change also fails in the control. My change adds no failure.
- certify.py and C5: no test of run's refusal must change. `test_the_refusal_is_per_law_and_says_why`
  (test_run.py 930) has law C with a failure and no pass, refused in both readings. certify.py's
  `refuse` (583) must follow the model: before "if not any(serves...)", a failure of the law at the
  demand's hash (`at`) refuses the law with state ("Current", that failure's outcome), and
  `show_refusal` then prints "failed at ...". A new test would put a passed, serving entry in front
  of a failed one of the same law and hash (two seeds) and expect the refusal. Left to the
  coordinator, as the brief says.

## Per item, the law changed

### 1. C1, the grade determined for every certificate

`WeakestAcrossBindings` and `StrongestUnderOneBinding` lose their `c.entries == nil` premise and
become one step of the fold: a pass `p` at the current hash added where no failure is. With
`NoEntryNoGrade`, `AFailureRefutes`, `OnlyCurrentEntriesCount` and `NotRunAddsNothing`, the
grade of every certificate is fixed by induction on its entries (the two right-hand sides read
certificates with fewer entries). New helpers in §2: `prepend`, `only`, `without`, `keepUnder`,
`refuted`, `failureAt`, `orWeakest` (`nothing` as unit), `orStronger`, `under`, `underAll`; and
`pool` in §5, which puts drawn passes under `p`'s binding (`ps`) and under drawn bindings (`qs`)
so both cases are met.

    StrongestUnderOneBinding (k : Certifying) (c : Certificate) (ps : List (CurrentPass c)) (p : CurrentPass c) : Bool :=
      refuted (pool c p ps nil)
        or (match p.grade { nothing -> true ; just g ->
              k.grade (withEntry (only p.binding (pool c p ps nil)) p)
                == just (orStronger g (k.grade (only p.binding (pool c p ps nil)))) })
    WeakestAcrossBindings (k : Certifying) (c : Certificate) (ps qs : List (CurrentPass c)) (p : CurrentPass c) : Bool :=
      refuted (pool c p ps qs)
        or k.grade (withEntry (pool c p ps qs) p)
             == orWeakest (k.grade (without p.binding (pool c p ps qs)))
                          (k.grade (withEntry (only p.binding (pool c p ps qs)) p))

The model's `grade` already is this fold and is unchanged. Checked by evaluation (scratch file,
`tester.load_program`): the model gives `true` on built cases; a model that takes the strongest
across bindings (Kimi's upgrade) gives `false` on `WeakestAcrossBindings`.

### 2. C2, implications over a type, now over subtypes

New domains (§5), built by the tester where a refinement equates a field (7.S6), filtered on the
rest (outcome, grade):

    EntryOf (c : Certificate) : U := { e : Entry | e.law == c.law and e.cone == c.cone }
    CurrentPass (c : Certificate) : U :=
      { e : Entry | e.law == c.law and e.cone == c.cone and e.outcome == Passed and not (e.grade == nothing) }
    CurrentFailure (c : Certificate) : U := { e : Entry | e.law == c.law and e.cone == c.cone and isFailure e.outcome }
    EntryOfLaw (l : String) : U := { e : Entry | e.law == l }
    EntryFor (d : Demand) : U := { e : Entry | e.law == d.law and e.cone == d.cone }
    FailureFor (d : Demand) : U := { e : Entry | e.law == d.law and e.cone == d.cone and isFailure e.outcome }

Coverage of a demand's values cannot be built by a refinement (a list is no literal), so the laws
of §3 draw the entry that would serve but for one condition as an image, `toward d e o g`
(`reshape` with the reach `withSupport d.given e.reach`), as 7.S6 allows ("the image of a
construction whose arguments the functor draws"). I did not define Kimi's `ServedEntry k d`: drawn
by filtering on `k.serves d e` it is empty at a stale hash, so the laws over it would not run. The
laws changed:

    AFailureRefutes (k : Certifying) (c : Certificate) (f : CurrentFailure c) (ps : List (CurrentPass c)) (es : List Entry) : Bool :=
      k.grade (prepend es (prepend (passEntries c ps) (withEntry c f))) == nothing
    OnlyCurrentEntriesCount (k) (c) (ps : List (CurrentPass c)) (e : Entry) (s : EntryOfLaw c.law) : Bool :=
      ((e.law == c.law and not (k.stale c.cone e)) or k.grade (withEntry (withPasses c ps) e) == k.grade (withPasses c ps))
        and (not (k.stale c.cone s) or k.grade (withEntry (withPasses c ps) s) == k.grade (withPasses c ps))
    NotRunAddsNothing (k) (c) (ps : List (CurrentPass c)) (e : EntryOf c) : Bool :=
      match e.outcome { Failed x -> true ;
        Passed -> not (e.grade == nothing) or k.grade (withEntry (withPasses c ps) e) == k.grade (withPasses c ps) ;
        NotRunFor r -> k.grade (withEntry (withPasses c ps) e) == k.grade (withPasses c ps) }
    StaleCertifiesNothing (k) (d) (e : EntryOfLaw d.law) : Bool :=
      not (k.stale d.cone (toward d e Passed (just Proved))) or not (k.serves d (toward d e Passed (just Proved)))
    OnlyAPassServes (k) (d) (e : EntryFor d) : Bool :=
      not (k.serves d (toward d e e.outcome (just Proved))) or e.outcome == Passed
    CertifiesOnlyUnderItsBinding (k) (d) (e : Entry) (f : EntryFor d) : Bool :=
      (not (k.serves d e) or (e.law == d.law and coversAll k.contains e.reach d.given))
        and (not (k.serves d (reshape f d.law f.reach Passed (just Proved))) or coversAll k.contains f.reach d.given)
    ServesAtTheCutoff (k) (d) (e : EntryFor d) : Bool :=
      not (k.serves d (toward d e Passed e.grade)) or (match e.grade { just g -> gradeRank d.accepts <= gradeRank g ; nothing -> false })
    ACoveringPassServes (k) (d) (e : EntryFor d) (g : Grade) : Bool :=
      not (gradeRank d.accepts <= gradeRank g) or k.serves d (toward d e Passed (just g))
    ServesIsMonotoneInTheCutoff (k) (d) (e : EntryFor d) (g : Grade) : Bool :=
      not (k.serves d (toward d e Passed e.grade) and gradeRank g <= gradeRank d.accepts)
        or k.serves (withAccepts d g) (toward d e Passed e.grade)

`RefusalSaysWhy` draws its store with entries of the law at the current hash (`xs`) and at drawn
hashes (`ys`) in front (item 3). The checker does not take `List (EntryFor d)` where `List Entry`
is asked (4.R9), so `passEntries`, `entriesFor` and `entriesOfLaw` lift the inclusion to lists.
A model that serves a failed entry now gives `false` on `OnlyAPassServes` (checked as in item 1).
`TransportOnTheIntersection` is unchanged: its weakness (parameter names rarely coincide) is no
guarded consequent.

### 3. C5, a current failure is refused whatever serves

    RefusalSaysWhy (k : Certifying) (n : String) (d : Demand) (xs : List (EntryFor d)) (ys : List (EntryOfLaw d.law)) (es : List Entry) : Bool :=
      k.refuse (drawnStore d xs ys es) [{ name := n, provisional := false, laws := [d] }]
        == (match failureAt d.law d.cone (drawnStore d xs ys es) {
              just f -> [{ name := n, law := just d.law, state := Current f.outcome }] ;
              nothing -> if anyServes k.serves d (drawnStore d xs ys es) then nil
                else [{ ... state as before: latest at the current hash, stale, uncertified }] })
    ACurrentFailureIsRefused (k : Certifying) (n : String) (d : Demand) (f : FailureFor d) (p : EntryFor d) (es : List Entry) : Bool :=
      k.refuse (cons (toward d p Passed (just Proved)) (cons f es)) [{ name := n, provisional := false, laws := [d] }]
        == [{ name := n, law := just d.law, state := Current f.outcome }]

`ACurrentFailureIsRefused` is claimed in `Certifying` and named in `State`'s roles; the comment on
`Certified` says such a cone is never of the type. [proposed] The state listed is the latest
failure at the current hash, not the latest entry (which may be the later pass and would read
"passed" in a refusal). The model's `refuseLaws` checks `failureAt` first. The model at eeeb694
gives `false` on both laws; the new one `true`.

### 4. C6, C11, C9

C6, in `Store`'s predicate, so the tester's store and one read from `x.cert.json` owe it:

    admits (ev : Evidence) (g : Grade) : Bool := match ev {
      Cited r -> g == Proved ; Assumed -> g == AssumedGrade ; NotRun r -> false ;
      _ -> grade Confirmed (coverageOf ev) == just g or grade Supported (coverageOf ev) == just g }
    heldAsRun (es : List Entry) : Bool := ... for each pass with grade g:
      admits e.evidence g
        and (not (coverageOf e.evidence == just Listed) or censusOfAtMost (pointCount e.evidence) e.reach)

The entry holds no verdict, so a pass's grade is one of the two test.lth's `grade` gives a
confirming or a supporting verdict over its coverage: Fable's `Proved` for a sampled run is out.
A pass over listed cases reaches a `Members` for each parameter, of at most the cases evaluated.
certify.py's `store_errors` would follow (coordinator's).

C11:

    notBefore : String -> String -> Bool
    latestInFront (es : List Entry) : Bool :=
      match es { nil -> true ; cons e rest ->
        (match rest { nil -> true ; cons f more -> notBefore e.date f.date }) and latestInFront rest }
    Store (k : Certifying) : U := { es : List Entry | determined k es and gradedAsOutcome es and heldAsRun es and latestInFront es }

The kernel orders numbers and not `String` (kernel.py evaluates `<=` on numbers only), so the
order of dates is a hole, like `C`. Until it is filled, the predicate on a store of two entries or
more does not evaluate; on `emptyStore` it holds.

C9: `Value`'s comment ends "Roles: `ReachesAsSets` (§5)."

### 5. Left for Luciano, untouched

C3 (`record` on a known identity: 6.S8 against 6.S15) and C4 (budgets in the identity).

## Notes for the coordinator

- demand.lth 145 `LoweringLosesNothing` passes `(e : Entry)` to `ServesIsMonotoneInTheCutoff`,
  which now takes `(e : EntryFor d)`. The checker accepts it; the obligation `e.law == d.law and
  e.cone == d.cone` is met almost never by a drawn entry. demand.lth should draw
  `(e : EntryFor (m.lawDemand d law cone))`. Not my file.
- Drawing any `Entry` draws an `Evidence`, whose `At` and `Points` take an `(A : U)`, which has no
  generator (7.R2). A test line for these laws will need a binding for the evidence. This was so
  before this change.
- No test line exercises `Certifying` yet (no certification_laws.lut, no certification_model
  store); the checks above are by evaluation in a scratch copy.

## Decisions I took

- The step laws in place of `grade` defined in the theory (the brief allowed either).
- `toward`/`reshape` images for the coverage the tester cannot build, and no `ServedEntry`.
- The state of a refusal by a current failure is that failure.
- `admits` allows either verdict's grade, since the entry does not record the verdict.
- The date order as a hole in `Store`'s predicate.
