# Internal review of the layer 2 and 3 theories

2026-10-13, by a Claude Opus 5.5 subagent, on the brief `review-layers-2-3.md` in this directory.
Read only. Files read at commit f2141e2: `src/luthier/lib/generators.lth`, `generators_model.lut`,
`test.lth`, `world.lth`, `world_model.lut`, `library.lth` (its §4 landed in f70ca34 while this review
ran, and is included), `examples/hello.lut`, and `src/luthier/host.py` (45f60dc) as the specimen
behind `world_model.lut`; against `docs/spec/07-tests.md`, `10-world.md`, `12-files-and-tools.md`,
`docs/principles.md` (Terms, L2, L9, L10, L11, L14) and the decisions they cite. `laws.lth` (layer 1)
was read where `test.lth` depends on it.

The questions are those of the brief: (1) laws false of the intended model or unsatisfiable
together; (2) laws that do not determine what they claim, with the wrong model that passes; (3)
constructors with no law of their role (L2.7, "a `data` with no law of its constructors' roles is a
collection"); (4) the models against their theories; (5) where a file says other than its chapter
or a cited decision; (6) laws stated over a type with an implication a random case rarely meets,
where the subtype belongs (7.S12, L9.6: "the grade of a sampled certificate depends on the
distribution sampled"); (7) one thing to change first. Each finding below was checked against the
file; the one numerical claim (gen.1) was run in Python with IEEE doubles. What I could not verify
is in "Not sure". Findings are numbered per file; the heading in brackets is the question.

Overall: three families recur. Theories whose operation is a fixed definition outside the
structure, so the laws are theorems of that definition and every value is a model (gen.3). Laws
with no lower bound, so an empty or vacuous run passes (test.1, test.2). And the world laws, which
apply actions to one token more than once, against D-2026-10-13-b ("each value of it is used
once") and 10.S5 ("two applications to one token are two nodes"); on host.py they read the current
state whatever the token, so they are vacuous or depend on evaluation order (world.1).

## generators.lth and generators_model.lut

**gen.1 [1] `PickedHasWeight` is false of the file's own `pick` in Float64.** Line 78 to 80:

    PickedHasWeight ... :=
      not (0.0 <= v and v < 1.0)
      or (match pick T s.weights (total T s.weights * v) { nothing -> total T s.weights == 0.0 ; ... })

With weights `[0.2069275338996801, 0.30170813156887355, 0.11080832909580751, 0.9300779837079021]`
and `v = 1 - 2^-53`, `total * v` minus the first three weights leaves exactly `0.9300779837079021`,
`u < w` is false, and `pick` gives `nothing` while the total is positive. In a run of 100000 random
supports (one to six weights), about 4% of those drawn with `v` that close to 1 miss. A sample with
`v` uniform in [0, 1) almost never meets it: an edge of the kind L9.6 names. Either `pick` returns
the last positive-weight value when the subtraction runs out, or the law says so.

**gen.2 [1] `UniformAtLevel` is false of a correct source.** Line 56:

    UniformAtLevel (r : Random) (s : Seed) (n : Nat) (alpha : Float64) : Bool := uniformPValue (draws r s n) >= alpha

For a uniform source the p-value is below `alpha` on a fraction `alpha` of seeds, so as a law over
every `s` it is false for every `alpha > 0`; for `alpha > 1` it is false at every seed, and at `n = 0`
the p-value is undefined. 7.S17 makes it a statistical law returning its statistic, level and
outcome, and 7 §11 makes `alpha` "a parameter of the demand, never a constant": it should be a
parameter of the certification, not a quantified variable, and `n` should have a lower bound.

**gen.3 [2, 4] `Support`, `Filter` and `Resolution` hold of every value.** Their structure holds
data only, and the operation each laws speak of is a fixed definition of the file:
- `Support (T) : { weights }` with `pick` defined at line 64. `PickOfOne` (line 82 to 83) does not
  mention its `s` at all: `pick T [(x, 1.0)] v == just x`.
- `Filter (T) : { base, keep }` with `filtered` at line 128. `FilterKeeps` and `FilterStops` are
  true for every base and predicate by the definition of `filtered`.
- `Resolution : { whereBs, profile }` with `resolve` at line 164. `ParameterWins` puts its binding at
  the head of `whereBs`, where `firstBinding` finds it first; `WhereWins` ignores `r`.

So the only law that constrains a model is `NonNegative`. This is the shape the review of layers
0-1 found in `FoldNil` and `FoldCons` ("they hold by definition"). Either the operation becomes a
field and the laws characterize it, or these become definitions with tests, not theories (4.R10).

**gen.4 [2] What `Support` claims to characterize is not stated.** Line 69 to 71 promise "a value is
drawn for a part of [0, C) as wide as its weight", and line 81 "a value after one of weight zero is
the next drawn". No law states either. With `pick` as a field, the model "return the first value
of positive weight" passes `PickedHasWeight` and `PickOfOne`. The proportionality of 7.S2 is the
law (for instance: `pick` at `u` gives `x_i` exactly when the running sum before `x_i` is at most `u`
and the running sum through `x_i` exceeds it).

**gen.5 [2] `Metric` is passed by a constant.** Line 94 to 98: `WithinBounds` and `Grows`. The model
`place lo hi v := lo` is within the bounds and weakly increasing, so it passes. What separates the
two metrics is their invariance, which 7.S4 states and P10 asks for: `linear` commutes with
translation (`place (lo + c) (hi + c) v == place lo hi v + c`), `log` with scaling
(`place (k * lo) (k * hi) v == k * place lo hi v`), and each sends 0 to `lo`. Those laws would also
tell `linear` from `logarithmic`, which today pass the same laws.

**gen.6 [5] `Interval` forbids what `linear` is for.** Line 91:
`Interval : U := { lo hi : Float64 | 0.0 < lo and lo < hi }`. Both metrics take an `Interval`, so
`linear` cannot place over [-1, 1] or [-s, s], which 7.S3 ("the metric over [-s, s]") and 7.S4 (a
coordinate, a residual, a log-likelihood) need. Only `log` needs `0 < lo`, and 7.S4 also gives it an
atom at 0 and a sign. The positivity belongs to the log metric's domain, not to `Interval`.

**gen.7 [2] `Exhaustive` and `Sized` let the model choose its own size.** Line 109 and 118: `size :
T -> Nat` is a field. With `size x := 0`, `SizeBounded` (line 119) holds for any generator. 7.S3
fixes the size by the type ("the size bounds lengths and depths"), so the size is the type's, one
function per form, not the model's. `Exhaustive` also admits duplicates (`values n` listing each
value twice passes), which would double the counted cases of 7.S12.

**gen.8 [5] `Exhaustive` admits infinite types, and the grade then says confirmed.** `Exhaustive (T :
Concrete)` with `size := length` on `List Bool` or `size := abs` on `Int` passes all three laws. 7.R3
and the table of 7.S3 make `exhaustive` over an unbounded `Int` an error, and 7.S10 reads the sized
case as "bounded is exhaustive on the box the domain names". See test.3 for what the grade does
with it.

**gen.9 [5] The functors of 7.S3 are not stated.** The header (line 15 to 17) says "the functors of
7.S3 are stated per form, with the instances the core's types need". No instance exists for any
form (`Bool`, `Fin n`, product, sum, `List`); the only models are the two metrics. 7.R3's covering
array, 7.S6's recorded acceptance rate, 7.S7's redraws (the `redraws` budget is used by nothing:
`dependent`, line 137, does not redraw) and 7.R4's family members (`from f`) are not stated either.
The index marks §3 to §5 done.

**gen.10 [1, 5] A census drawn at random is graded as listed.** Line 153: `fromCensus` draws with
equal weights through `drawWeighted`, so it repeats members and misses others. The table of 7.S3
gives a census as "each value of the list in turn, or draws from it by its weight", and test.lth's
`CensusMode` gives coverage `Listed` and grade `Cases`, which claims every member was covered. The
walk in turn is what `RuleCases` does at size 0 (line 211); `fromCensus` should do the same.

**gen.11 [2] `CensusFirst` does not make the walk advance.** Line 212 to 214 fix the value at seed
`i`, and ignore the next seed. A model that gives the `i`-th program with next seed `i` passes, and a
test drawing `n` cases from seed 0 then sees the first program `n` times. The law needs "the next
seed at size 0 is `i + 1`".

**gen.12 [5] `Budgets` against 7.S8 and its own comment.** Line 183 says "Each is positive", and
`positiveBudgets` (line 185) leaves out `largestSize`. 7.S8 also lists the total probability of
special values, the atom at 0 of a `log` metric, the runs that estimate a level, the seeds per
control and the draws that certify a generator's distribution; none is in `Budgets`.
`largestSize` duplicates `TestSpec.size` of test.lth, and no law says which governs.

**gen.13 [2] `Random` does not state independence.** 7.S1: "uniform values, independent successive
draws". `SeedMoves` and `UniformAtLevel` are passed by an additive Weyl sequence (`next s := (s +
1327217885) mod 2^31`, `uniform s := s / 2^31`): its values are equidistributed, so the
goodness-of-fit p-value is high, and each draw is a fixed function of the previous one. A serial
law (pairs of successive draws uniform in the square, or a serial correlation test) is missing.

**gen.14 [6] Unit-interval guards over raw `Float64`.** `PickedHasWeight` (line 79), `PickOfOne`
(line 83), `WithinBounds` (line 95) and `Grows` (line 97) take `v : Float64` and guard it with `0.0 <=
v and v < 1.0`. A `Float64` without bounds has no generator (7.S3, 7.S4), so as written they cannot
be sampled, and with any wide binding the guard is rarely met. The subtype `{ v : Float64 | 0.0 <= v
and v < 1.0 }` is an interval, drawn with no rejection (7.S6); `Grows` wants an ordered pair of it.

**gen.15 [4] The models.** `linear` and `logarithmic` (generators_model.lut lines 9, 11) pass
`WithinBounds` and `Grows`: 200000 random intervals with `0 < lo < hi`, `v` including `1 - 2^-53`,
gave no value outside. They pass because the laws are weak (gen.5). No model exists of `Random`,
`Support`, `Exhaustive`, `Sized`, `Filter`, `Resolution` or `RuleCases`.

**gen.16 [5] The chapter lags the file.** 7.S5 says the generic generators are "to be written in
`lib/generators.lut` ... `[proposed]` and not written"; they now have a theory file and a model file.

## test.lth

**test.1 [2] A tester that returns no points passes.** Line 71 to 77:

    ModeGivesCoverage ... := match coverageOf (t.run s) { nothing -> true ; just c -> ... }
    CountsCases ... := match s.mode { SampledMode k -> pointCount (t.run s) <= s.cases ; _ -> true }

`run _ := Assumed`, or `Cited "x"`, or `Evaluated true`, gives `coverageOf = nothing` and `pointCount
= 0`, so both laws hold. No law says the evidence is about `s.law`, that it is a `Points`, or that
it was drawn with the spec's seed and bindings.

**test.2 [1, 5] An empty sample is supported, and graded sampled.** `CountsCases` has an upper bound
only. 7.S12: "an entry is accepted only if its evaluated cases reach the directive's `n`", and "a law
none of whose cases evaluates is not run". With `Points A nil (Drawn s)`, laws.lth's
`forallVerdict` gives `Supported` (no refutation, and `allConfirmed nil` is true), and `grade`
(line 95) gives `Sampled`. With `ExhaustiveMode`, a run whose budget gave nothing gets `Confirmed`
and `ExhaustiveGrade`. L10.9: "no operation on certificates raises a grade ... without new
evidence". The lower bound (`pointCount >= s.cases` or a not-run outcome) is the missing law.

**test.3 [1, 5] The coverage ignores the bindings and the type.** Line 67 to 72: `modeCoverage` maps
`ExhaustiveMode` to `Exhaustive` whatever the bindings and whatever the type. An exhaustive test
with one parameter bound to `sampled log` is graded exhaustive, where 7.S10 says "when the
parameters of a law are drawn differently, its entry lists the reach of each, and the grade is
summarized by the weakest". And with gen.8, an exhaustive run over `List Bool` up to size 10 is
`Confirmed`, where L9.12 says a `forall` over an infinite domain is "confirmed only by statistics"
and 7.S10 says bounded is exhaustive on a box the domain names. `Coverage` has no box.

**test.4 [1] A witness drawn at random is graded sampled.** Line 93: `Confirmed` with `just (Drawn
s)` gives `Sampled`. An `exists` is confirmed by any witness whatever the coverage (laws.lth,
`existsVerdict`), and L9.12 says its cost is "determinate rather than statistical"; 7.S10: "witnessed
is cases with a witness". It should be `Cases`.

**test.5 [3] `MetricName` has no law of its role, and `Grade`'s role law only lists.**
- `LinearMetric` and `LogMetric` (line 31 to 34) appear in no law; `modeCoverage` drops the argument
  of `SampledMode`, and nothing ties them to `linear` and `logarithmic` of generators_model.lut.
- `GradesAsTerms` (line 101 to 104) is a table of six cases. The role of a grade is its order
  ("summarized by the weakest", 7.S10) and its evidence cost (L10.2: 0 for proved and exhaustive on
  their domain, 0 on the cases listed and infinite outside, finite for sampled). Neither is stated,
  so the "weakest" of 7.S10 has nothing to work on.

**test.6 [4] `grade` is not a model.** By hand, `grade` passes the six cases of `GradesAsTerms`, but
no `Grading` value is defined from it, and no model of `Tester` exists.

**test.7 [5] Against chapter 7.**
- `CensusMode` is not a mode in 7.R1 or 7.S20, where a census is a per-parameter binding and the
  modes are `exhaustive` and `sampled` with its metric.
- 7.S20 says `test` is "a function of `lib/test.lut`"; here it is in a theory file and returns a
  `TestSpec`, the data reading of D9 (top-level `test` lines are data, `test "x.lut"` the action).
  The chapter does not yet say that `test` builds data.
- 7.S12 counts apart the cases not drawn, skipped, and with a false premise; `pointCount` counts
  every point, and `Evidence` has no form for a skipped case.

## world.lth, world_model.lut, examples/hello.lut

**world.1 [1, 5] The laws use one token more than once.** `OwnIsIdempotent` (line 77 to 78):

    not a.own or sameAt m (after A (a.run w)) (after A (a.run (after A (a.run w)))) m.places

applies `a.run` to `w` twice and once more to the result. `ChangesOnlyDeclared` (line 89 to 90),
`PrintAppends` (line 159 to 161), `PrintChangesOnlyStdout`, `ReadGivesThePlace`,
`ReadChangesNothing`, `WriteThenRead` and `WriteChangesOnlyItsPlace` all read at `w` and also act on
`w`. D-2026-10-13-b: each value of `W` "is used once"; D4 (in force, plan from zero): "each token of
`W` is consumed exactly once"; 10.S5: `act` "gives a new token each time, so two applications to one
token are two nodes the memo never merges". So `OwnIsIdempotent` runs the action three times, and
compares the first run with the third. These laws are also predicates into `Bool` that perform
actions, which 10.S1 (evaluation has no effect) and 10.S3 (a function either gives a `W` or holds no
effect) do not allow. On host.py the consequence is concrete: `read_place` ignores its token (line 18
to 19 read module state), so "before" and "after" read the same state. `ChangesOnlyDeclared` and
the other comparisons are then vacuous, and `PrintAppends` holds or fails depending on whether the
read at `w` is evaluated before or after `print`. D-2026-10-13-a already gives the form: "an action
is a directed request, checked by comparing the representation before and after". See section 7.

**world.2 [5] `act` is an action in a theory file.** Line 52: `act (A : U) (a : Action A) (w : W) : W
* A := a w`. Its type takes and gives a `W`, which 10.S3 makes an action, and 12.S23 says the checker
rejects an action in a `.lth`.

**world.3 [5] The world laws quantify over a type.** `OwnIsIdempotent (m : World) (A : U) (a :
Declared A) (w : W)`, and `ChangesOnlyDeclared` the same, are claimed by `World`, which has no
parameter, so `A : U` is a quantified variable of the law. 7.R2: "a test of a law quantified over a
parameter of type `U`" is a static error. And every law of the file quantifies over `w : W`, which
nothing can generate: `W` "has no introduction" (D-2026-10-13-b). Only `Persistence` says its
evidence is an assumption; the others have no certifier at all as stated.

**world.4 [1] `RefusedWhenRefuted` and `ProvisionalIsApplied` are unsatisfiable on a refuted
provisional extern.** Line 134 to 138: a provisional route whose verdict is `Refuted` must be both
not applied and applied. A model passes only by never refuting a provisional route, that is, by not
validating provisional externs. That may be the intent (4.R5: provisional is "never certified"), but
no law or chapter text says the validation is skipped, and 10.S10 says the first action that asks
for an extern validates it.

**world.5 [2] `Externs` is passed by never applying anything.** `applied r := r.provisional` passes
all four laws: nothing says a `Confirmed`, `Supported` or `Cites` verdict leads to application.
Further, the `read` field has no law, so nothing ties `identity` to the hash of what `read` gave;
`verdictOf : Route -> Verdict` does not depend on the bytes read, so a stale verdict after the file
changes passes (10.S10: "its certificate stays by hash"); and the comment at line 122 to 123 ("the
validation is a test of test.lth, its verdict read from the evidence by laws.lth's `Settling`") is
stated by no law; `TestSpec` and `Tester` are imported and unused. `IdentityCarriesHash` (line 141 to
142) also asks `hash`, a hole of the core, to be injective on any two strings, which no real hash is.

**world.6 [2] `ChangesOnlyDeclared` sees only the listed places.** Line 89 to 90 compare
`except m.places a.places`. An action that writes a file not in `m.places` passes: with `places =
["stdout"]`, a `print` that also overwrites `/tmp/x` satisfies `PrintChangesOnlyStdout`. On host.py
`places()` is the standard output plus the files read so far, so the set grows as the run goes.

**world.7 [4] world_model.lut through host.py breaks `Console`.**
- `PrintAppends` asks `appendStr prior s`; `print_line` appends `s + "\n"` (host.py line 24). With
  `appendStr` the concatenation core will give, the law fails at every print. (`appendStr` is a hole
  of the theory file, so today the law constrains `print` only relative to an undefined append; with
  `appendStr p s := p`, a `print` that does nothing passes, since `read_place("stdout")` is never
  `nothing`.)
- `ReadGivesThePlace`: before the first `read_file` of a path, `read_place(path)` is `None`, while
  `readFile` gives the text. The law holds only if the read at `w` is evaluated after the action.
- `ReadChangesNothing`: `read_file` adds the path to `_files` (line 30), changing `places()` and what
  is read at that path.
- `readFile : W -> String -> W * Maybe String`: the host returns the text and raises on a missing
  file; there is no `nothing` path.

**world.8 [6] `WriteThenRead` is vacuous on random paths.** Line 101: `not (memberStr p
s.world.places) or ...`. A random string is almost never a listed place, and a write to a new file
has no law at all. The domain is the subtype of paths in `places`, or the law drops the guard.

**world.9 [5] Chapter 10 lags the files and a decision.**
- 10.S2: "The language has no action a program can name ... no library defines `print`." world.lth §4
  and world_model.lut define it, and hello.lut uses it.
- 10.S13: "`lib/world.lut` ... does not exist". It exists as `world.lth`, a theory file (12.S23).
- 10.S8: "Because it opens a file, `extern` is an action (D-2026-10-12-ab)." D-2026-10-12-ac, which
  resolved that question, makes an `extern` "a definition like any other: its name, its declared type
  and the route"; world_model.lut follows -ac, with `extern` inside a top-level record, where 10.S2
  refuses actions.
- D8 put `print` in core; world.lth puts it in a library theory with a model. The file is the
  better reading under D-2026-10-12-al (the world's form is a library's); the chapter should say so.

## library.lth

**lib.1 [2] The policy laws of §4 are vacuous with the model's `isCore` and `isLibrary`.** Line 196
to 211, with line 182: "Which of these paths is core or a library is the model's." `isCore _ := true`
makes `PrimitiveOnlyInCore` and `AxiomOnlyInCoreAndLibraries` hold while admitting
`n3_primitive_outside_core.lut` and `n4_axiom_outside_lib.lut`. At least the negative cases need
fixing in the law: `not (l.isCore "n3_primitive_outside_core.lut")`, `not (l.isLibrary
"n4_axiom_outside_lib.lut")`.

**lib.2 [2] Two admission functions, unrelated.** `admits : FileKind -> SurfaceProgram -> Bool`
(line 60) carries `TheoryFileRejectsExtern`; `admitsAt : String -> SurfaceProgram -> Bool` (line 67)
carries the §4 laws. No law relates them, so a loader whose `admitsAt` ignores the kind (and admits
an extern in `r_arrow.lth`) passes, and `admits` may be used by nothing. `admits _ _ := false` for
`TheoryFile` also passes every law: no law says a theory file admits anything.

**lib.3 [1, 2] `VerifiesTheModel` and the sample's unbound names.** Line 99:
`define "Numpy" [] (just (name "LinearAlgebra")) (termBody (recordValue [("f", name "one"), ("g",
name "two")]))`. `one` and `two` are defined nowhere (there is no `core.lut` yet), so a `verifies`
that type-checks the model, as 12.S22 says ("verifies that it defines that name as a model of that
theory"), answers false and the law fails. If instead `verifies` only checks that the name is
defined with that annotation, the three cases pass a verifier that never looks at the fields: a
`Numpy` without `f`, or with `f := "text"`, would be verified. A negative case with a missing or
mistyped field, and well-typed bodies in the sample, would close both.

**lib.4 [5] `externBody` reads only the head of a body.** Line 70 to 71 say "found anywhere in a
body"; the code is `match t { app f a -> externBody f ; name s -> s == "extern" ; _ -> false }`. An
extern inside a record value, which is exactly how world_model.lut writes its models (`places :=
extern "..."` inside `{ ... }`), is not found, so a theory file holding one is admitted by
`TheoryFileRejectsExtern`. `hasBodyOf` (line 140) has the same reach for `primitive` and `axiom`,
which is right for 3.S39's bodies but not for `extern`.

**lib.5 [3] `DataFile` has no law of its role.** Line 41: its only appearance in a law is `l.kind
"refs.bib" == DataFile` (line 81), an extension. 12.R1 gives it a role (a `.bib` imports as one
`Reference` per entry); neither `admits`, `reads` nor `visible` says anything of a data file.

**lib.6 [2] Every law is a closed case over one sample.** `KindByExtension` still tests literal paths
(the review of layers 0-1 asked for "the kinds from the extension in general"), and §2 and §3 are
over `sample` only. A loader that pattern-matches on `"main.lut"` passes. The file says so ("case
laws over a small set of files"); the generalization would quantify over generated file systems,
with `sample` as the census, as generators.lth §7 does for programs.

**lib.7 [6] `TheoryFileRejectsExtern` over a random program.** Line 85: `not (hasExtern p) or not
(l.admits TheoryFile p)`. A random `SurfaceProgram` almost never has an extern body, so the law
passes on nearly every case without testing anything. The domain is `{ p : SurfaceProgram |
hasExtern p }`.

**lib.8 [5] Chapter 12 lags and the file omits 12.S1.**
- 12.S1 names the theory `lib/library.lut`, "not written yet"; it is `library.lth`.
- The header cites 12.S1 ("a file denotes a value of a record type") as a source, but no law states
  it: `FileSystem` is a list of parsed programs, and nothing relates a file to a record whose fields
  are its definitions.

## Not sure

- Whether D4's "checked by the checker per block" covers definitions at `Bool` outside blocks. If it
  does not, world.1 still stands on 10.S5 (two applications of one token are two nodes) and on
  host.py's behaviour.
- How the bridge handles `places := extern "python:luthier.host.places"`, a zero-argument Python
  function, where `World.places` is a `List String` value; I did not trace run.py's bridge.
- Whether 12.S21 ("a model file is read at the first demand for one of its names, the checker needing
  it or `run` needing its value") contradicts 12.S22 ("the importer is checked against the theory
  alone, without reading the model's file") and `CheckingReadsTheories`. It may mean the
  verification at first demand of 12.S22; the wording reads as if checking reads model files.
- `defaultBudgets` (test.lth line 48 to 49) is said to hold "the numbers today's code holds".
  `coveringAbove := 20000` looks like 7.S3's limit on function tables, not a covering-array
  threshold (the code has none, per 7.R3); I did not find `drawsPerCase := 10` in 7.S8 or the code.
- gen.1 assumes Luthier's `Float64` arithmetic is IEEE binary64 with round to nearest, as 11.R1's
  `primitive "ieee754-binary64"` says.

## What I would change first

world.1: restate the laws of world.lth over the representation, as D-2026-10-13-a reads an action
("checked by comparing the representation before and after"). The library's representation `S` is a
value in `U` with structural equality; an action's description is a function `S -> S * A`; the laws
(own actions idempotent, only the declared places change, print appends, read gives the place) are
laws of those functions, testable by sampling `S`; and a host action is certified against its
description along one chain of tokens: observe, act once, observe again, compare. That removes the
reuse of tokens, the actions inside `Bool` predicates and the quantification over `W`, which no
generator can give, and it gives host.py something it can satisfy. It goes first because host.py
and run.py are being written against this theory now (D-2026-10-13-ad, execution first), and every
other world law would be rewritten in the same move.
