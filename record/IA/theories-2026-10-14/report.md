# Report: Coverage's roles in laws.lth (D-2026-10-14-b) and the callback crossing's laws (D-2026-10-14-a)

Written 2026-10-14 by Claude Fable 5.1 (the agent of `prompt.md`), on commits 41a233f, 23edcf0,
f216f7b, d58229e over 374426f. Every file named parses and `luthier check` comes clean (laws.lth,
test.lth, test_model.lut, world.lth, world_model.lut, term.lth, term_model.lut). world_model.lut
is unchanged: the model of the new theory is the bridge in run.py, a specimen, not a Luthier
value (see the last section).

## What was written

laws.lth (41a233f, D-2026-10-14-b). `rankOf` and `weaker` moved here from test.lth, under
`Coverage`, with a theory `Covering : { rank : Coverage -> Nat }` and one law,
`CoveragesAreOrdered`: `rank (Drawn s) < rank Listed < rank (Bounded n) < rank Exhaustive`,
stated by the constructors, so `Bounded`, `Listed` and `Drawn` have their roles in the file that
defines them (4.R3, 7.S10). `Exhaustive` keeps `ForallOnPoints`. The comment on `Coverage` names
the roles and says the grade each coverage gives is still test.lth's `GradesAsTerms`, which is
not repeated. The 4.R3 refusal on laws.lth:101 is gone.

test.lth (23edcf0). Imports `rankOf` and `weaker` from laws.lth; the two definitions are deleted
and a comment points at laws.lth. `CoverageIsTheWeakest`, `bindingsCoverage` and `Grading` are
unchanged. test_model.lut still checks clean.

world.lth (f216f7b, D-2026-10-14-a), §3 after `Externs`: a theory `Crossing (A B : Concrete)`
with `callBack : (A -> B) -> List A -> List B * Nat` (what the bridge gives the host when the
host calls a Luthier function at the arguments `xs`, with the count) and
`callField : List (String * (A -> B)) -> String -> List A -> List B * Nat` (the same through a
field of a record of functions). Three laws: `CallbackGivesTheFunction` (the values are
`map f xs`), `CallsAreCounted` (the count is `length xs`), `RecordCrossesByField` (calling a
field of `[(l, f)]` is `callBack f`, values and count). The prose states what the decision says
and the theory cannot: the callback takes no token (10.S1, D4), so the host's calls change no
place and the host action stays one action under `Described`, certified by §5's protocol; the
count goes to the run's record (12.S18, P2).

term.lth (d58229e, D-2026-10-14-a), §5 beside `ExternIsValue`. `ExternIsValue` now also states
that a program defining a name spelled like the route does not unfold the extern (a route is not
a name, 3.S40): that is the law of the opaque host function, which is an extern by handle. Two
new laws, claimed in `Reduction`: `ExternPartialIsValue` (an extern declared with a type of two
parameters, applied to one, is a value: D-a's partial application, the arity from the declared
type) and `HostGivesBackAValue` (an application of an extern that the step does not leave as it
is, with a constant or a lambda as argument, steps to a value: the host's answer, including the
callback's result). term_model.lut leaves every extern application as it is, so it keeps both
trivially; the laws bind run.py.

## Every [proposed], with the item it reads

- world.lth, `Crossing`'s comment: the count is per callback crossing, recorded with the route of
  the extern that received it (D-2026-10-14-a names the count and the record, 12.S18, not the key
  under which it is written).
- term.lth, `ExternIsValue`'s comment: a host function crossing in is an `Extern` whose route is
  a handle minted by the bridge, typed by the declaring extern's result type (D-2026-10-14-a names
  no representation; run.py already does this, `host:n` at run.py:555).
- term.lth, `ExternPartialIsValue`: the step reads the arity of `Extern r` from the `Define`
  whose body it is, so the law hands the step the program (D-2026-10-14-a says the arity comes
  from the declared type, not where the step finds it).
- term.lth, `HostGivesBackAValue`: the host's answer is a value in one step, whatever the
  argument (D-2026-10-14-a says the host function crossing in is a value, not that every answer
  is).

Readings taken without a mark, as routine: a theory `Covering` with a single field `rank`
(instead of extending `Settling`, which has models elsewhere I may not touch); `Crossing` is
parameterized by the two types like `World (S : Concrete)`, rather than polymorphic in its
fields; world_model.lut left without a model of `Crossing` (a pure reference model would restate
the laws; the honest model is the bridge). Each is undone by one commit and nothing depends on it.

## What the specimens must do, one line per law

- `CoveragesAreOrdered` (laws.lth): tester.py's coverage ranking keeps exhaustive above bounded
  above listed above drawn; a model `Covering` is `{ rank := rankOf }` if one is wanted in a .lut.
- `CallbackGivesTheFunction` (world.lth): run.py's `to_host` turns a lambda over an infinite
  domain into a Python callable that evaluates the lambda at each argument crossing in by the
  declared domain type, and returns the value crossing out by the codomain, instead of refusing
  or materializing (3.S23's `Fin n` case stays as it is).
- `CallsAreCounted` (world.lth): that callable counts its calls, and run.py writes the count,
  keyed by the receiving extern's route, into the `x.run.json` entry of the run (12.S18).
- `RecordCrossesByField` (world.lth): `to_host` of a `RecordValue` whose fields are functions
  gives a Python object whose attributes are those callables (lm.py reads `objective.f`), each
  counted on its own.
- `ExternIsValue`, the new conjunct (term.lth): kernel.py's `whnf` never looks a route up as a
  name; already so (`Extern` is a leaf, kernel.py:31) and run.py's `host:n` handles are never
  defined names.
- `ExternPartialIsValue` (term.lth): run.py already returns the partial application as a value
  when `len(args) < arity` (run.py:905); kernel.py alone, with no `TypedExtern`, must read the
  arity from the `Define` that holds the extern or leave the application stuck.
- `HostGivesBackAValue` (term.lth): `from_host` gives a value for every Python result it accepts
  (constants, tuples, lists, arrays, callables as `host:n`), and the one-step reading asks that
  `whnf` not re-enter the host on that result; a result it does not accept stays a `RunError`,
  which is a refusal and not a step.

## Decisions taken on my own

Those listed as routine above, and the placement: the count and the record of functions in
world.lth, the partial application, the opaque function and the host's answer in term.lth, the
brief having left the choice open.
