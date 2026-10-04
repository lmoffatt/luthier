# Luthier

A language where a type carries the laws its values must satisfy, and defining something defines
its test. Version 0 tests; it does not prove.

```
import "algebra"

Z7 : U := { k : Int | 0 <= k and k < 7 }

eqZ7 (a b : Z7) : Bool := a == b
addMod7 (a b : Z7) : Z7 := (a + b) mod 7
mulMod7 (a b : Z7) : Z7 := (a * b) mod 7
negMod7 (a : Z7) : Z7 := (7 - a) mod 7

ringZ7 : Ring Z7 := (eqZ7, addMod7, mulMod7, 0, 1, negMod7)

test ringZ7 exhaustive
```

```
$ luthier test examples/z7ring.lut
ringZ7: passed
  ok   Associative Z7 eqZ7 addMod7   [exhaustive, 343 cases]
  ok   Commutative Z7 eqZ7 addMod7   [exhaustive, 49 cases]
  ...
  ok   RightDistrib Z7 eqZ7 addMod7 mulMod7   [exhaustive, 343 cases]
```

`Ring` is a type in the `algebra` library: a record of operations, with its own equality, and the
laws they satisfy. Declaring `ringZ7 : Ring Z7` records the obligation; `test` runs it and writes
the certificate. A wrong implementation fails with a counterexample:

```
badRing : Ring Bool := (eqB, or, and, false, true, not)
  FAIL LeftInverse Bool eqB or false not   [exhaustive, 1 cases]
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
structural; `data` is for recursive types. A vector is a function `Fin n -> R`, and a numpy array
is a value of that type as it is.

The specification: `docs/semantica/04-kernel.md` (the kernel: type formers, terms, reduction, the
surface forms and their translation) and `docs/semantica/05-static-semantics.md` (states of a name,
objects, the rules R1 to R8, certification). `00` to `03` are the reading guide, the construction
pattern, the grammar and the libraries.

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
  `Int`, `R`, `String`, `Maybe`, `List`, `Nat`, `Fin`.
- `src/luthier/lib/`: libraries in Luthier, imported on demand (`docs/semantica/03-libraries.md`).
- `tests/spec/`: one program the checker must accept and one it must reject per rule of 05, and the
  kernel's type formers. `tests/test_kernel.py`: the mechanisms.
- `examples/`, `docs/semantica/`, `docs/audios/` (the voice notes the design comes from),
  `archive/` (what preceded the specification of 2026-10-04).

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
