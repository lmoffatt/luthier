# The port of validate_graph.lut and distance_graph.lut: report

2026-10-14, Claude Opus 5.5, an agent of the coordinating session, on `prompt.md` of this
directory (a914edc). Sources read only, in sonolocalización at 5ffc36ef70e16e11182bc09e4a927c381e35df1c:
`prototipo-cero/luthier/{validate_graph,distance_graph,distance_graph_python,positions}.lut` and
`prototipo-cero/src/distance_graph.py`. Nothing was changed there, nor in `src/luthier/` or `tests/`.

## What was written

| file | commits | parse | check |
|---|---|---|---|
| `examples/sonolocalizacion/A/graph/{nodes,measurements}.csv`, `SOURCE.md` | 2b9a2c5 | | |
| `examples/sonolocalizacion/positions_slice.lut` | 962dbae | passes | 3 refusals, 4.R3 |
| `examples/sonolocalizacion/distance_graph.lut` | 2f1127f, 81d9d8c | passes | passes (notes `loose`/`unclaimed` only) |
| `examples/sonolocalizacion/validate_graph.lut` | 66dee14 | passes | 2 refusals, 4.R9 |

`run` stops with `stuck match` (below).

## Renames

The six mechanical rewrites the inventory listed: `\` to `fn`; flat `import "x"` to named imports
of the theories in `src/luthier/lib/` (`tables.lth`, `tables_model.lut`, `arrays.lth`,
`arrays_model.lut`, `numbers.lth`, `numbers_model.lut`, `world_model.lut`); `< a : A | b : B >`
to `{ schema : String || inRow : RowViolation }`; the one-arm `match e { x -> body }` used as a
`let` to blocks (`measurementViolation`, `nodeViolation`, `unseenDirections`, `distanceJacobian`);
the tuple literals `(n, \ k { ... })` and `(r, c, \ a b { ... })` to `vec A n (fn k { ... })` and
`mat A r c (fn a b { ... })` (arrays.lth §1). Every other name is v0.1's: `DistanceGraph`,
`HasNodeColumns`, `HasMeasurementColumns`, `GraphWithColumns`, the six invariants and their row
predicates in v0.1's order, `ValidGraph`, `ValidDistanceGraph`, `RowViolation`, `Violation`,
`firstViolation`, `ReportsValidity`, `describe`, `summary`, `distinctPairs`, `MapInput`,
`toMapInput`, `designOf`, `unseenDirections`, `rigidMotions`, `unseenAlways`; of positions.lut
`Positions`, `Node`, `point`, `foot`, `pairDistance`, `Pairs`, `Separated`, `SeparatedPairs`,
`distanceJacobian`, `PairsAmong`, `Design`, `flatten`; of the libraries `Table`, `hasColumn`,
`intAt`, `realAt`, `textAt`, `firstFailing`, `forallBelow`, `existsBelow`, `sumToInt`, `distance`,
`Vec`, `Mat`, `VecOf`, `MatOf`, `MatRows`, `toFloat64`, `Maybe`, `Fin`, `not`.

## What was more than a rename

1. `readGraph (w : W) (dir : String) : W * Maybe DistanceGraph` is an action (10.S3): two
   `host.readFile` and `csv.parse` on each. `GraphDir`, `isGraphDir` and the extern
   `read_graph_record` are gone. A graph that cannot be read prints a new line,
   `FAIL ReadGraph: <dir> has no nodes.csv and measurements.csv that read as typed tables`, where
   v0.1 stopped with the extern's `ValueError` naming the file and the parse error; `csv.parse`
   gives a `Maybe`, so that detail is lost.
2. `main (w : W) : W * Unit` prints with `host.print` the line v0.1's `main : String` returned.
3. `rowText` is written in Luthier (`cellText`, `rowCells`) in place of the extern `row_text` of
   `src/distance_graph.py`, which lives in the other repository (P7, each repository is
   self-contained). Same text: `name=value` per column, joined by `, `.
4. `fastCheck` (the extern `first_violation`) is not ported, for the same reason; `main` uses the
   native `firstViolation`. The branch `the check reported nothing on a graph that is not valid`
   is kept, though the native check makes it unreachable, to keep v0.1's lines and the flow
   refinement `summary g` asks for.
5. `retainedRank` takes its floor first (arrays.lth §4). `unseenDirections` takes the floor as
   its first parameter, and `validate_graph.lut` names it, `rankFloor g`, with v0.1's value:
   `3N` times `doubles.epsilon` (numbers_model.lut), the `n eps` of arrays.py's `_retained`.
6. `intToString` and `realToString` route to `builtins.repr` with their parameter written. The run
   refuses `builtins.str`: it is a type and has no signature (`extern python:builtins.str failed:
   no signature found for builtin type <class 'str'>`). `repr` gives v0.1's text for an int and a
   float.

## Readings where the spec or the theories did not decide (mine; each undone by one commit)

- `distance_graph.lut` is imported by `validate_graph.lut` but has no `.lth`. 12.S23 says what
  another file imports has its theory in a `.lth`, and 12.S22 that the importer sees only what the
  theory names. I followed the brief's file names and imported its definitions by name. A
  `distance_graph.lth` (record, invariants, `Violation`) with the actions in a `.lut` is the
  alternative.
- `readGraph` sits in `distance_graph.lut`, beside the schema, since `experiment_zero.lut` will
  read the graph too; it could equally sit in `validate_graph.lut`.
- The leaves are reached as `numpy.transpose`, `numpy.matMul`, `numpy.retainedRank` and not as
  `transpose jac * jac`: whether an importer sees an imported file's `operator` acts is not stated
  (arrays_model.lut says so itself), and the brief's import names only `numpy : Arrays`.
- `rowText` takes the row as `Int`, since `RowViolation.row` is an `Int`, and guards
  `0 <= r and r < t.nRows` before reading a cell (`""` outside).
- In `toMapInput` the node vectors are `vec (Fin g.nodes.nRows) ...`, and in `unseenDirections`
  they are rebuilt as `vec (Node p) ...`. v0.1 wrote an untyped pair and let the expected type
  decide. `vec` takes its element type explicitly (arrays.lth).
- `positions_slice.lut` carries what the five named definitions depend on: `Positions`, `Node`,
  `point`, `foot`, `Pairs`, `Separated`, `SeparatedPairs`. Left out: `positionsModel` (needs
  probability), `pairDistances`, `nodesOf`, `PositionsOf`, `unflatten`, `layout`.
- `graphDir` is `"examples/sonolocalizacion/A/graph"`, relative to the root of this repository,
  where the run must start.

## What check says (reported, not fixed)

- `positions_slice.lut:26, 39, 63`, 4.R3 on `Positions`, `Pairs`, `PairsAmong`: a refinement of a
  `Vec` by its length touches `n` and not `f`. arrays.lth's `VecOf`, `MatOf`, `MatRows`,
  `Square` get the same refusal. As stated, 4.R3 refuses every shape refinement of an array.
- `validate_graph.lut:35, 43`, 4.R9 on `summary` and `report`: a subtype imported from another
  file is not taken as refining its imported base, nor is a condition's refinement (4.R11) seen
  across the import. The same program in one file passes. Smallest:

      -- a.lut
      R = { x : Int, y : Int }
      P (r : R) : Bool := r.x < r.y
      S : U := { r : R | P r }
      -- b.lut: refused, 4.R9
      import "a.lut" R S
      f (r : R) : Int := r.x
      s (r : S) : Int := f r

- A gap found on the way: `x : Int := "three"` passes check (no refusal for a literal against the
  declared type).

## What stopped the run

`PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/validate_graph.lut` on the
tree at 81d9d8c (run.py bite 4, 2821823, included) prints `stuck match`. Reading the graph works:
both files are read through the host and parsed by `csv.parse`, and the tables cross as
`{ nRows := 10, names := ..., kinds := ..., cell := <host> }` and `{ nRows := 22, ... }`. The run
stops at the first invariant, `HasNodeColumns`, on `hasColumn g.nodes "name" "str" and ...`.

**First stop: a connective whose left operand is a match on a list.** Smallest program, no host
data:

    import "world_model.lut" HostConsole host : HostConsole
    nonEmpty (xs : List Int) : Bool := match xs { nil -> false ; cons y rest -> true }
    main (w : W) : W * Unit := host.print w (if nonEmpty (cons 1 nil) and true then "yes" else "no")

prints `stuck match`; without `and true` it prints `yes`. kernel.py:773 steps `and`/`or`'s left
operand with the kernel's own `_step`, and the kernel treats `cons`/`nil`/`true`/`false` as
constructors only when a `data` defines them. The run never loads `core.lut`, so none does. The
Runner's own `Match` path (`demanded_pattern`) matches them, but it is not reached for an operand.

**Behind it**, found in a scratch probe that patched the run in memory (nothing in `src/` was
changed, and the probe is not committed), each stop removed in turn:

1. `not` is undefined in a run, again because `core.lut` is not loaded (12.S22 has core
   enclose every file).
2. `run_file` defines only `+ - * == <` as primitives (run.py, `run_file`), not
   `kernel.BOOTSTRAP_PRIMITIVES`. So kernel bite 9's `>=`, `<=`, `>`, `/=`, `/`, `mod` and
   `toFloat64` reach `luthier eval` but not `luthier run`: `0 >= 3` is stuck.
3. With core's data loaded and the full primitive set, the probe went past the schema and
   stopped in `firstFailing` over `rowIndicesInRange`, the first row-wise invariant: a host cell
   under a primitive operator. Smallest, unpatched:

       import "world_model.lut" HostConsole host : HostConsole
       import "tables.lth" Table intAt
       import "tables_model.lut" csv : Codec
       showInt (x : Int) : String := extern "python:builtins.repr" x
       main (w : W) : W * Unit := host.print w (match csv.parse "a:int\n7\n" { nothing -> "no table" ; just t -> showInt (intAt t "a" 0 + 1) })

   gives `not an Int at the crossing: App(App(Primitive('+'), Match(App(App(TypedExtern('host:1', ...` .
   With `intAt t "a" 0` alone it prints `7`.

One cause runs under all three: `Runner.whnf` drives the head of a term and hands an operator's
application to `kernel.step`, which steps the operands with the kernel alone. The kernel neither
calls the host nor knows core's data. Two changes to run.py would clear them (proposed, for
run.py's owners): load `core.lut` into every run, and have the Runner bring the operands of
primitives and connectives to weak head normal form itself. Not reached yet: the row loops of the
invariants, the native Jacobian (22 x 30 entries), the crossing of `Mat Float64` to
`retained_rank_at`, and whether the default fuel of 10,000 steps is enough.

Seen in passing (unsure it matters): in the error above, the declared type of the host table's
`cell`, `String -> Fin nRows -> Maybe Cell`, is held as
`Pi(_, String, implies (Fin 1) (Maybe ...))`. The inner `->` was read as implication.

## What the run should print

v0.1's line for a valid graph is `valid: 10 nodes, 22 measurements, P distinct pairs; directions
the distances do not see: U (of which 10 are the heights and 3 the rigid motions of the plane)`.
I did not compute P and U outside Luthier, since data scripts are Luciano's to run. A run of v0.1's
`validate_graph.lut` on this graph gives the reference.

## Decisions I took on my own

The six readings above, the items of "more than a rename" that the brief did not fix (the
`FAIL ReadGraph` line, `rowText` native, `fastCheck` dropped, `builtins.repr`), and the file
placement of `describe`, `rowText` and `readGraph` in `distance_graph.lut` and of `summary`,
`report` and `rankFloor` in `validate_graph.lut`.
