# world.lth after round 1: Host against the Console, the laws as predicates over observed cases. Report

2026-10-15, Claude Fable 5.1, an agent of the coordinating session (luthier-3e), on
`prompt-fix-host.md` of this folder. Inputs: `summary.md` at b90f82a (its W numbers are those of the
first synthesis, 2982741, which the prompt uses; this report names each item by its content), the
replies `A/kimi.md` (the no-op host) and `A/gpt.md` (the pure predicate), `A/fable.md` (the frame
law, the dropped result), world.lth and world_model.lut at b90f82a (unchanged since the frozen
055589c), spec 10.S5 to 10.S10, D-2026-10-13-a and D-2026-10-14-c, host.py and run.py read only
(`_Theories.action_law`, `FirstActions`), and `record/IA/certification-2026-10-14/report-first-action.md`.
Commits: 2ac8f12 world.lth, 44578c4 world_model.lut. No Python changed. Nothing of the provisional
extern (10.S10 against 6.S14, Luciano's) was touched: `AppliedWhenSettled` keeps `r.provisional or`.

## Accepted when

- `luthier parse src/luthier/lib/world.lth`: exit 0. `luthier check` on world.lth and on
  world_model.lut: clean (exit 0, no output).
- Files that import them, checked after the change: tests/tester/world_laws.lut, tests/tester/
  plot_laws.lut, plot_model.lut, examples/hello.lut, tests/run/observe.lut, read_first_line.lut,
  holes.lut, callbacks.lut, record_of_functions.lut, plot_two_tables.lut, examples/sonolocalizacion/
  experiment_zero.lut: clean. One breaks: `src/luthier/lib/plot.lth:562: 4.R9 renderAgrees`, which
  applies the old `agreement` (seven arguments, `W * Bool`); it needs the new form (below), a file
  outside this bite. tests/run/first_action_models.lut checks clean but imports `printDescribed` and
  `readFileDescribed`, which no longer exist, and builds `Host State` with the old fields: it fails
  when a demand reaches it (12.S22). The entries of `world_model.cert.json` are stale (the laws'
  cones changed). `luthier run examples/hello.lut` was not run (runs write stores); as run.py stands
  it will be refused upfront, since no law of `Host` takes the token any more and `action_law`
  recognizes nothing: the next bite.

## The laws as they read now, by item

### Item 1 (W1): `Host` over the `Console` model, the frame law, the root of trust

`Host` has no descriptions of its own; it carries the console (world.lth 313-318):

    Host (S : Concrete) : {
      console : Console S,
      observe : W -> List String -> W * S,
      print : W -> String -> W * Unit,
      readFile : W -> String -> W * Maybe String,
    }

The descriptions are built from the console in world.lth §4 (268-273), never by the host's model:

    printDescription (S : Concrete) (c : Console S) (s : String) : Described S Unit c.world :=
      { describe := c.printLine s, own := false, places := [c.stdout] }
    readFileDescription (S : Concrete) (c : Console S) (p : String) : Described S (Maybe String) c.world :=
      { describe := c.readFile p, own := false, places := [p] }
    observeDescription (S : Concrete) (c : Console S) (ps : List String) : Described S S c.world :=
      { describe := fn st { (st, st) }, own := false, places := ps }

Kimi's no-op host now fails `HostAgreesPrint`: its case is held to `console.printLine s`, which
appends a line. world_model.lut's `host` is `{ console := console, observe, print, readFile }`;
`printDescribed` and `readFileDescribed` are gone from it.

The host's side of 10.S7, over the places the certifier supplies (365-366):

    HostChangesOnlyDeclared (S : Concrete) (o : Host S) (A : Concrete) (h : Held S A o.console.world) (extra : List String) (c : Observed S A) : Bool :=
      readsAlike S o.console.world c.before c.after (undeclared h.described.places extra)

`extra` is the certifier's parameter (the places the run has touched, a sample of paths);
`agreement` observes `extra` together with the declared places, so the case holds them. The law is
generic over the held action `h`, the one the case was gathered from.

The root of trust, marked in the language and in the comment (378-380): `readsTheWorld` is an
`axiom` (11.R3: stated, never tested, obligations graded assumed), and the law asserts it:

    readsTheWorld (S : Concrete) (o : Host S) (p : String) : Bool :=
      axiom "the host's observation at a place is what is at the place outside the program"
    ObserverIsFaithful (S : Concrete) (o : Host S) (p : String) : Bool := readsTheWorld S o p

The comment says why no law inside Luthier can test it (every law compares the host's observation
with the host's observation; in the specimen `observe` reads back the string `print` wrote, and the
terminal is written by `run` at the end) and what its evidence is: a citation of the host's source
(6.S9) or an assumption graded assumed (6.S10), which the run's demand must accept.

### Item 2 (W2): laws as pure predicates, `agreement` the action that gathers the case

The case and what the host is held to (304-307):

    Observed (S : Concrete) (A : Concrete) = { before : S, result : A, after : S }
    Held (S : Concrete) (A : Concrete) (m : World S) = { act : Action A, described : Described S A m }
    held (S) (A) (m) (act : Action A) (d : Described S A m) : Held S A m := { act := act, described := d }

`agreement` threads the token and returns it with the case, the result inside it (319-323):

    agreement (S : Concrete) (A : Concrete) (m : World S) (o : Host S) (h : Held S A m) (extra : List String) (w0 : W) : W * Observed S A :=
      match o.observe w0 (concatStrs extra h.described.places) { (w1, before) ->
      match h.act w1 { (w2, x) ->
      match o.observe w2 (concatStrs extra h.described.places) { (w3, after) ->
        (w3, { before := before, result := x, after := after }) } } }

The predicates (331-338) compare the result and read at the places:

    agrees (S) (A) (m) (h : Held S A m) (c : Observed S A) : Bool :=
      match h.described.describe c.before { (described, x) ->
        x == c.result and readsAlike S m described c.after h.described.places }
    observes (S) (m) (h : Held S S m) (c : Observed S S) : Bool :=
      readsAlike S m c.result c.before h.described.places and readsAlike S m c.before c.after h.described.places

The laws (348-358), none taking the token, each building the `Held` it is about (so the law names
its action and projects it, which 4.R3 requires of a theory's fields and run.py reads):

    HostAgreesPrint (S : Concrete) (o : Host S) (s : String) (c : Observed S Unit) : Bool :=
      agrees S Unit o.console.world (held S Unit o.console.world (fn w { o.print w s }) (printDescription S o.console s)) c
    HostAgreesReadFile (S : Concrete) (o : Host S) (p : String) (c : Observed S (Maybe String)) : Bool :=
      p == o.console.stdout
        or agrees S (Maybe String) o.console.world (held S (Maybe String) o.console.world (fn w { o.readFile w p }) (readFileDescription S o.console p)) c
    HostObserveChangesNothing (S : Concrete) (o : Host S) (ps : List String) (c : Observed S S) : Bool :=
      observes S o.console.world (held S S o.console.world (fn w { o.observe w ps }) (observeDescription S o.console ps)) c
    Host (S : Concrete) := HostAgreesPrint S & HostAgreesReadFile S & HostObserveChangesNothing S & HostChangesOnlyDeclared S & ObserverIsFaithful S

Where a case law sits in certification is in the comment at 293-302: the runner gathers one case at
the first application with the run's own arguments and evaluates the law on it; the entry is that
case, graded cases, bound to the model, the arguments and the places added, kept by the model's cone
hash. Whether one case serves the rest of the run is left as Luciano's question, as the brief asks.
The comment also says that a law with an `Observed` parameter is run by the certifier alone, as a
law with the token was: a drawn case is no observation, and `luthier test` must not draw it.

### Item 3

W3, the declared type in `Route` (144-145), the core's term after elaboration:

    Route = { name : String, declared : Term, route : String, provisional : Bool }

with `Externs.lawsOf : Term -> List String` (the laws the type states, 6.S1) and the law that an
extern with no law is not applied (177-178), which the old file claimed in a comment only:

    NoLawNoGrade (e : Externs) (n : String) (t : Term) (route h : String) : Bool :=
      not (e.lawsOf t == nil) or e.gradeOf (routeOf n t route false) h == nothing

W4, quantifying over provisional routes: built from their parts (181-182):

    ProvisionalIsAssumed (e : Externs) (n : String) (t : Term) (route h : String) : Bool :=
      e.gradeOf (routeOf n t route true) h == just AssumedGrade

Over own descriptions: not done as a type change. `d` in `OwnIsIdempotent` is the model under
certification, so `d.own` is its declaration and not a draw (Fable's reading, which summary.md at
HEAD adopts under its W6: no finding); and `Described`'s shape (`describe`, `own`, `places`, three
type parameters) is built by plot.lth's `drawn`, outside this bite. The comment at 97-101 says so.

W5, `RecordCrossesByField` over a field anywhere in a record of any size (225-226):

    RecordCrossesByField (A B : Concrete) (b : Crossing A B) (before after : List (String * (A -> B))) (l : String) (f : A -> B) (xs : List A) : Bool :=
      hasLabel A B l before or b.callField (concatFields A B before (cons (l, f) after)) l xs == b.callBack f xs

The count is `callBack f xs`'s: the calls to `f` and no other field's (counted apart). A bridge
that calls the first field whatever the label fails it as soon as `before` is not empty.

W6, `OwnIsIdempotent` with the result (103-104):

    OwnIsIdempotent (S : Concrete) (A : U) (m : World S) (d : Described S A m) (s : S) : Bool :=
      not d.own or d.describe (stateAfter S A (d.describe s)) == d.describe s

W8, `settled` at the demand's cutoff (169-173); `Externs.gradeOf` gives the validation's grade
(test.lth's `grade` of verdict and coverage; `nothing` when refuted or not run), since a `Verdict`
alone does not carry the coverage a grade needs:

    settled (accepts : Grade) (g : Maybe Grade) : Bool :=
      match g { just k -> gradeRank accepts <= gradeRank k ; nothing -> false }
    AppliedWhenSettled (e : Externs) (accepts : Grade) (r : Route) (h : String) : Bool :=
      e.applied r h == (r.provisional or settled accepts (e.gradeOf r h))

M1, `readFile` at the standard output's place: the premise `p == o.console.stdout or` in
`HostAgreesReadFile` above, the exemption `ReadGivesThePlace` already makes. In world_model.lut the
literal "stdout" now appears twice (`theWorld.read`, `console.stdout`), the description's copy gone.

## What run.py's first-action validation must change, one line per law

- `HostAgreesPrint`: `action_law` recognizes the law by its `Observed` parameter instead of a `W`
  one (model, the action's arguments between model and case, the field projected: `print`); at the
  first `print`, evaluate `agreement S Unit m o (held ...) extra w` with the `held` term taken from
  the law's body, hand the program `(w3, c.result)`, evaluate the law at `c`, record the entry with
  `extra` in the binding.
- `HostAgreesReadFile`: the same, field `readFile`; when the argument equals `o.console.stdout` the
  law is true by its premise and the case still gathers the program's result.
- `HostObserveChangesNothing`: the same, field `observe`, at the program's own first `observe`
  (the protocol's inner observations are not applications of the program).
- `HostChangesOnlyDeclared`: no action field; run it on every case gathered, with `h` the held of
  that case and `extra` the certifier's places (a parameter: today none, so choose and record it);
  name the differing places from `undeclared h.described.places extra`.
- `ObserverIsFaithful`: no case; `certification()` must accept an entry graded assumed (or a
  citation) in the model's store, served only under `--accept assumed`; without one, every run of a
  `Host` model is refused, which is 6.S10 as written.
- `disagreement`: read `m` and `h` from the law's `agrees`/`observes` application instead of
  `agreement`'s `m` and `d`; compare at `h.described.places` by `m.read`, and the result.
- Beyond run.py: plot.lth 562 `renderAgrees` takes a `Held` (`held S Unit m (fn w { r.render w p
  (pathOf stem ext) }) (drawn S r.drawing p stem ext)`) and `extra`, and gives `W * Observed S Unit`;
  tests/run/first_action_models.lut builds `Host State` with `console := console`; the entries of
  world_model.cert.json are regenerated.

## Decisions of my own

- The pairing of a law with its action stays structural (the one action field the law's body
  projects), through a `Held` built in the law; the checker's 4.R3 requires every field of `Host`
  touched by its laws, and a pure predicate cannot apply the action, so the pairing record is the
  one honest mention. A record literal in argument position fails 4.R9 when the parameter's type is
  a parameterized record (probed), hence `held` and the three `*Description` definitions.
- `agrees` compares at the declared places by `m.read`, not the whole state, so that it and the
  frame law each read their own places and the runner can name the place that differs.
- The observation has its own predicate, `observes`, since its result is the world at its places
  while the case's `before` holds the places added as well.
- The root of trust as an `axiom` (11.R3), the language's own marker for assumed, rather than a
  declared hole, so that `check -v` lists it and the grade is the spec's.
- `Externs.verdictOf : ... -> Verdict` became `gradeOf : ... -> Maybe Grade`: a cutoff is a grade
  (certification.lth's `accepts`) and a verdict without its coverage has no grade. laws.lth is no
  longer imported by world.lth; test.lth (`Grade`) and term.lth (`Term`) are, with no cycle.
- `NoLawNoGrade` added as the law of L11.3, which the file claimed in prose.
- `Described` kept at `(A : U)`; the comparison of results in `OwnIsIdempotent` presumes `A`
  concrete and the checker accepts it as written (the "not sure" item of summary.md stands).
