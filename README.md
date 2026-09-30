# Luthier

A language where a type carries the laws its values must satisfy, and defining
something defines its test. Version 0 tests; it does not prove.

```
Z7 : U := { k : Int | 0 <= k and k < 7 }

addMod7 (a b : Z7) : Z7 := (a + b) mod 7
mulMod7 (a b : Z7) : Z7 := (a * b) mod 7
negMod7 (a : Z7)   : Z7 := (7 - a) mod 7

ringZ7 : Ring Z7 := (addMod7, mulMod7, 0, 1, negMod7)

test ringZ7 exhaustive
```

```
$ luthier test examples/z7ring.lut
ringZ7: passed
  ok   Associative Z7 addMod7   [exhaustive, 343 cases]
  ok   Commutative Z7 addMod7   [exhaustive, 49 cases]
  ...
  ok   RightDistrib Z7 addMod7 mulMod7   [exhaustive, 343 cases]
certificate: examples/z7ring.cert.json
```

`Ring` is defined in the base library as a subtype with named components and
the laws they satisfy. Declaring `ringZ7 : Ring Z7` records the obligation;
`test` runs it and writes the certificate. A wrong implementation fails with a
counterexample:

```
badRing : Ring Bool := (or, and, false, true, not)
  FAIL LeftInverse Bool or false not   [exhaustive, 1 cases]
       counterexample: x = true
```

## Install and run

```
pip install -e .
luthier check examples/z7ring.lut
luthier test  examples/z7ring.lut            # runs the file's `test` directives
luthier test  examples/pyext.lut --name sinAll --n 500 --seed 1
luthier eval  examples/z7ring.lut "addMod7 3 5"
pytest
```

## Layout

- `src/luthier/` the interpreter: lexer, parser, checker, evaluator, generators, testing, cli
- `src/luthier/prelude.lut` the base library, written in Luthier
- `examples/` programs with their `test` directives
- `docs/semantica/` the design: core elements, the subtype pattern, the grammar
- `docs/audios/`, `docs/ideas/` the voice notes the design was distilled from

## Libraries

```
import "z7ring.lut" as z7      -- qualified: z7.addMod7, z7.Ring...
import "xor.lut"               -- flat: names enter this file's namespace
```

A file can declare a function with its laws and leave it as a hole; another
file imports it and fills it (`sqrt := extern "python:math.sqrt"`), inheriting
the laws as obligations. `luthier test` writes a certificate with a hash of each
definition's dependency cone; importing a file accepts entries whose hash still
matches, so certified libraries are not rerun unless you pass `--deep`.
`luthier check -v` shows what is certified, stale or pending. Imports are
searched next to the importing file, then in `LUTHIER_PATH`, then in the base
library. See `docs/semantica/03-librerias.md`.

## What is in version 0

Definitions `name : Type := term`, holes (declared without body), `data` with
pattern matching, dependent functions `(x : A) -> B`, pairs `A * B`, subtypes
`{ x : T | p }` with named components, `extern` to Python, and `test` with
sampled or exhaustive generation. No proofs, no `Term` as a value yet.
