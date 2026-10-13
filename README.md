# Luthier

> Being rebuilt from zero (2026-10-13, D-2026-10-13-h): first the theories of Luthier, written in
> Luthier, then the Python that implements them. The interpreter this page describes is at the tag
> `v0.1-final` (`git checkout v0.1-final`); the specification it will follow is `docs/spec/`.

A language that verifies models of theories. A theory is a type with its laws; a model is a value
of it, and defining a model defines its test. The common case is a function type with its laws, a
theory of one symbol over types already modelled with their equality; a function is a model of it
and has sense only in that context.
What runs is decided by a demand from outside, which picks among the models of a theory by cost.
Version 0 tests; it does not prove.

```
import "algebra"

Z7 : U := { k : Int | 0 <= k and k < 7 }

eqZ7 (a b : Z7) : Bool := a == b
addMod7 (a b : Z7) : Z7 := (a + b) mod 7
mulMod7 (a b : Z7) : Z7 := (a * b) mod 7
negMod7 (a : Z7) : Z7 := (7 - a) mod 7

ringZ7 : CommutativeRing Z7 := {
  eq  := eqZ7,
  add := { monoid := { op := addMod7, unit := 0 }, inv := negMod7 },
  mul := { op := mulMod7, unit := 1 } }

test ringZ7 exhaustive
```

```
$ luthier test examples/z7ring.lut
ringZ7: passed
  ok   Associative Z7 Z7 eqZ7 addMod7 addMod7   [exhaustive, 343 cases]
  ok   LeftIdentity Z7 Z7 eqZ7 addMod7 0   [exhaustive, 7 cases]
  ...
  ok   Symmetric Z7 Z7 (eqZ7, ((addMod7, 0), negMod7), mulMod7, 1).eq (eqZ7, ((addMod7, 0), negMod7), mulMod7, 1).mul.op   [exhaustive, 49 cases]
```

`CommutativeRing` is a type in the `algebra` library, built from the structures below it: an
abelian group and a monoid over one equality, joined by distributivity, with a symmetric product.
`CommutativeRing` is the theory and `ringZ7` a model of it over `Z7`. Declaring
`ringZ7 : CommutativeRing Z7` records the obligation; `test` runs it and writes the certificate. A wrong implementation fails with a counterexample:

```
badRing : Ring Bool := {
  eq  := eqB,
  add := { monoid := { op := or, unit := false }, inv := not },
  mul := { op := and, unit := true } }
  FAIL LeftInverse Bool eqB (or, false).op (or, false).unit not   [exhaustive, 1 cases]
       counterexample: x = true
```

## What a program is

A program is a set of declarations (`x : T`), definitions (`x : T := t`) and aliases (`x = t`),
in any order. Everything is a type, and a value is a type with one inhabitant, so `x : T` reads
"x refines T": a later `x := t` makes `x` the inhabitant `t` if `t : T`, or the subtype of `T` that
`t` cuts out if `t` is a predicate over `T`. A type is declared over a labeled base, its laws are
written over it, and it is defined by them:

```
Codec : { parse : String -> Maybe Table, render : Table -> String, eq : Table -> Table -> Bool }
RoundTrip (c : Codec) (t : Table) : Bool := match c.parse (c.render t) { nothing -> false ; just u -> c.eq t u }
Codec := RoundTrip & Canonical & Tolerant & Rejects

csv : Codec := { parse := extern "python:luthier.tables.parse", render := extern "python:luthier.tables.render", eq := sameTable }
test csv with 200
```

The checker reads the whole program and checks it object by object: a declared type, its laws and
its definition form a cycle of the dependency graph, and that cycle is the object. A definition
may use only types that are defined; a lawless product is not a new type and is named with `=`;
the environment (Python) gives values, never types. Products, sums and functions are primitive and
structural; `data` is for recursive types. A vector is a function `Fin n -> Float64`, and a numpy array
is a value of that type as it is.

The specification: `docs/spec/`, twelve chapters with an index, `docs/spec/00-index.md`; each rule
carries its status (implemented, decided, proposed) and its accept and reject programs in `tests/spec/`.

## Install and run

```
pip install -e .
luthier check examples/z7ring.lut              # parse and type-check
luthier check -v examples/z7ring.lut           # and list what is certified, stale, pending, provisional
luthier test  examples/z7ring.lut              # run the file's test directives, write the certificate
luthier test  file.lut --name f --n 500 --seed 1
luthier eval  examples/z7ring.lut "addMod7 3 5"
luthier run   program.lut --set param=value    # evaluate main, record the run in program.run.json
pytest
```

## Layout

- `src/luthier/`: the interpreter. `parser.py`, `graph.py` (the objects of a file), `checker.py`
  (elaboration, obligations, the rules), `evaluator.py` and `machine.py` (reduction; call by need),
  `generators.py`, `testing.py`, `certify.py`, `cli.py`, `api.py` (loading a program from Python).
- `src/luthier/core.lut`: the kernel's own definitions, loaded implicitly: `Unit`, `Empty`, `Bool`,
  `Int`, `Float64`, `String`, `Maybe`, `List`, `Nat`, `Fin`.
- `src/luthier/lib/`: libraries in Luthier, imported on demand (`docs/spec/12-files-and-tools.md`).
- `tests/spec/`: one program the checker must accept and one it must reject per rule of 05, and the
  kernel's type formers. `tests/test_kernel.py`: the mechanisms.
- `examples/`, `docs/guide/`, `docs/spec/`, `docs/rationale/`.
- `record/`: the development record: the voice notes the design comes from (`record/audios/`),
  Luciano's notes, plans, decisions, audits, and what preceded the specification of 2026-10-04
  (`record/archive/`).

## Libraries and certificates

`import "x"` searches next to the importing file, then `LUTHIER_PATH`, then the shipped `lib/`;
`import "x" as m` qualifies the names. A file can declare a value with its laws and another file
give it a body (`sqrt := extern "python:math.sqrt"`), inheriting the laws as obligations.
`luthier test` writes a certificate with a hash of each definition's dependency cone; importing a
file accepts the entries whose hash still matches, so certified libraries are not rerun unless
`--deep`. Every run draws a seed and records it with the generators and the first cases, so
`--seed N` repeats it exactly.

Generators are Luthier values (`Gen A = Nat -> Int -> A * Int`, in `random`) or Python functions
(`gen T := extern "python:mod.fn"`); a function over `Fin n` is generated as its table, a
function of an infinite domain as a constant or an affine map (a thin sample, and the certificate
says so). One
parameter, `--size`, bounds every generated value and grows over a run.
