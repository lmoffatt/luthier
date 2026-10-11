# Libraries: what a file is, how it is imported, what travels with it

Rewritten on 2026-10-04 from the Spanish draft of 2026-09-30 (`03-librerias.md`, in the history).
Implemented in `src/luthier/cli.py` (the loader), `graph.py` (the objects of a file) and
`certify.py`.

## 1. A file is a structure

A `.lut` file is a set of acts with dependencies among them, and it denotes a value of a dependent
record type: `a : A := ..., b : B a := ...` is a term of `{ a : A, b : B a, ... }`, where the laws
of each definition are the subtypes of its component. A file is the same kind of thing as `Ring`.
This is the reading of ML's modules as dependent records: the signature of a library is its type,
two interchangeable libraries are two values of one type, and a library with holes is a function
whose parameters are its holes.

In version 0 a module is not built as a value; it is implemented by prefixing names. An
implementation of a theory, on the other hand, is a value already (a model, `01 §2`), and is
passed like any other.

## 2. Import

    import "x.lut"            -- flat: the definitions enter the importer's namespace
    import "x.lut" as m       -- qualified: reached as m.f, with no collisions

Search: next to the importing file, then the directories of `LUTHIER_PATH`, then the package's
`lib/`. `.lut` is optional. A `.bib` file imports as a module of `Reference` values
(`lib/reference.lut`), one per entry, named by its key, for `cite` (`05 §7`; 2026-10-11). Importing twice under one prefix does nothing; the same file may be
loaded under two prefixes. A cycle of imports is an error. `core.lut` is imported implicitly.

Name resolution inside a module `m`: `m.x` first (its own), then `x` (core and what the root
imported flat). A module does not see the definitions of the file that imports it. Constructors,
data types and the labels of sums named by an alias are prefixed like functions.

Within a file, order does not matter: the file is read whole and checked object by object
(`05 §2`). Between files it does, in the only sense imports allow: a file sees what it imports.

## 3. Declaration in one file, definition in another

A file may declare a value with its laws in its type, `sqrt : SquareRoot`, and another file give it
a body, `sqrt := extern "python:math.sqrt"`. The type of the definition, if written, must agree with
the declaration; if omitted, it is inherited. The laws of the declared type become obligations of
the definition, so a specification has as many implementations as files that fill it, all
compared against the same laws. This is C++'s separation of declaration and definition, and ML's
functor with the hole as parameter.

A declared type may likewise be defined by its laws in another file. What may not happen is a
definition that uses a type no file has defined (`05` R2), or an extern that gives a type (`05`
R5): the pattern of an opaque carrier declared in one file and filled by a Python class in another
is gone. In its place the libraries follow one pattern:

- the pure file (`array.lut`, `table.lut`) defines the types natively, writes a native definition of
  each operation, declares the operations the environment computes faster as holes, and states the
  laws;
- the `_python` file (`array_python.lut`, `table_python.lut`) fills those holes with externs, gives
  the generators, and certifies each extern against its native definition or the laws of its
  theory.

## 4. What travels: the certificate with its hash

`luthier test x.lut` writes `x.cert.json`. For each definition it records the laws run, each with
its grade (`05 §7`): the mode, the cases, the result, the generators used for each variable, the
seed and the first cases. And a hash of the definition's **dependency cone**: the definition and
everything it refers to, transitively, written with the module prefix removed and the bound
variables renamed canonically. Changing a definition changes the hash of everything that uses it.

When a file is imported its certificate is read. An entry is accepted if it passed and its hash
matches the current cone; the definition is then **certified**, and `test` does not run it again
unless `--deep`. If the hash does not match, the entry is **stale** and the obligation is pending
again. `luthier check -v` shows the state of each, and lists the provisional externs.

Laws of the importer that mention imported functions are obligations of the importer and always
run. `--name m.f --deep` runs an imported definition and writes into the certificate of its own
file; it is how an obligation whose generator lives in another file (a table generator in
`table_python.lut` for a law of `table.lut`) is certified.

## 5. The libraries

`src/luthier/lib/`, rewritten on 2026-10-04 under 04 and 05:

| file | what it holds |
|---|---|
| `real`, `real_python` | functions on `Float64` (declared, bound to Python's math), `approx` (the equality of `Float64` within a relative tolerance), `NonNegative`, the tolerances of laws |
| `random` | `Gen A = Nat -> Int -> A * Int`, a congruential generator, generators for `Int`, `Nat`, `Bool`, `Float64`, lists |
| `array`, `array_python` | `Vec`, `Mat`, their shapes, native definitions of every operation including the determinant and Jacobi's spectrum, numpy leaves certified against them |
| `algebra`, `algebra_python` | setoids, rings, fields, vector and inner product spaces, linear maps; instances on `Int`, `Float64`, vectors |
| `probability` | samplers and likelihoods, the kernel with its three presentations (sampler, likelihood, transform), the Gaussian and profile constructions, the ensemble diagnostics |
| `belief` | belief families, discrete and Gaussian (Laplace) beliefs, their laws |
| `optimization` | Levenberg-Marquardt in pieces, each with its law |
| `table`, `table_python` | native tables, the CSV codec as a theory and its model |

## 6. Open

- Modules as values (`fft : FFTLib := import "fft.lut"`) and explicit functors.
- Visibility: everything is public in version 0.
- The Python packages a file's externs depend on are declared nowhere.
- Whether a file that imports a provisional definition may itself be certified.
- Whether an importer may require a minimum grade of a certificate it accepts.
