# run.py bite 4: arrays, tables and Maybe across the bridge, report

2026-10-14, Claude Opus 5.5 (an agent of luthier-1b), on prompt-4.md, over the slice's theories at
9289aff. Not committed. Files: `src/luthier/run.py`, `src/luthier/arrays.py` (`retained_rank_at`
only), `tests/test_run.py`, `tests/run/{vector_norm,matrix_product,table_cell,record_externs,numbers}.lut`.
`host.py` and `tables.py` are unchanged.

## What crosses and how

The bridge now reads by type. When the Runner is built, every extern a definition gives (`f (x : A)
: B := extern "..." x`, or a field of a record whose declared type is a theory's record, such as
`numpy : Arrays` or `csv : Codec`) becomes a `TypedExtern`, a subclass of `term.Extern` carrying the
declared type. At a call each argument crosses at its domain, a later domain instantiated with the
earlier arguments (`(n : Int) -> Fin n -> Float64`), and the result at the codomain. An extern
without a declared type crosses by value, as before.

- `Vec Float64` `{ n, f }` goes as the 1-d float64 ndarray of `f` over `Fin n`, `Mat Float64`
  `{ m, n, f }` as the 2-d one, each entry evaluated once (3.S23, 3.S25), the shape checked against
  the record (3.S24). From the host an ndarray at `Vec` is `{ n := shape[0], f }` and at `Mat`
  `{ m, n, f }`, the number of dimensions checked (11.S6); `f` is a host object applied by indexing
  with `0 <= i < n` checked by the interpreter (3.S22). `Fin n -> Float64` and `Fin n -> Int` alone
  cross the same way: int64 with the 64-bit range check (11.S8), an int array promoted at
  `Float64`, a float array at `Int` an error, NaN or inf in an array an error (11.S7).
- `Float64` is a Python float, an int with an exact double promoted (both ways, including an Int
  literal passed where a Float64 is declared), NaN or inf an error. `Int` is an int, a bool or a
  float an error. `Fin n` is an int checked in range where `n` is known.
- `Table` goes to the host as the record tables.py's `as_table` reads (a dict with attribute
  access), `cell` a Luthier function giving None or `(label, value)`; a table that came from the
  host goes back as the same `tables.Table` object. From the host a `Table` is `{ nRows, names,
  kinds, cell }`, `cell` the host's method giving `nothing` or `just (int k)`, `just (real x)`,
  `just (text s)`. `Maybe Table` from `parse`: None is `nothing`, a table `just`.
- An extern inside a record value is resolved only when a projection reaches it and it is applied
  (3.S40): `record_externs.lut` projects one field of a record whose other field names a missing
  module.

Tests: a vector's norm through `numpy` (`5.0`), a matrix product's entry and shape (`43.0`, `2`),
a table's text, int and float cells through `csv.parse` on a CSV the test writes, then `csv.render`
of a table built in Luthier; the numbers (promotion, `Fin n -> Float64` both ways); eight crossing
errors with a control; each entry once; `retained_rank_at`. None waits for kernel bite 9: the
arithmetic is numpy's and the entries are literals.

Checks: `tests/test_run.py` 29 passed; `luthier run examples/hello.lut` prints `hello, world`;
`pytest tests` 470 passed, 7 xfailed.

## Choices the spec left open (mine; each undone by reverting this bite)

1. The type at the crossing is the extern's definition's declared type, attached by rewriting the
   program (`TypedExtern`); an extern applied to anything other than its parameters stays untyped.
2. A host object inside the kernel is a `TypedExtern` with a route `host:k` of this run and the
   object; it is applied like an extern and goes back to the host unchanged, never copied.
3. A record is a `Vec`/`Mat` by its labels (`n f`, `m n f`) with `f` a function over `Fin`; one
   whose elements are not numbers goes as the record with `f` a list (11.S9).
4. A record whose fields are one host object's attributes (a function field being that object's
   method) goes back as that object: this is how a host `Table` passes through, with no rule
   specific to tables. A Luthier-built `Table` is recognized by its four labels, so that its `cell`
   gives None or `(label, value)`; any other `Maybe` goes to the host as `host.Just`/`host.NOTHING`.
5. From the host at a declared `Maybe`: None or `NOTHING` is `nothing`, `Just x` or any other value
   is `just`. A declared sum crosses as `(label, value)` both ways (tables.py's cells).
6. Record fields cross in the type's order; a later field's type reads the earlier fields (`Fin
   nRows`, `Fin n`). Other refinements are not checked at the crossing (`Nat` is read as `Int`,
   `RankFloor` as `Float64`); 10.S11's obligation per refinement is still to do.
7. Untyped results: a numpy scalar is an int or a float, a float is checked finite, a bool is
   `true`/`false`, an ndarray a host function over its first index, a callable a host function.
8. `retained_rank_at(floor, a)` counts eigenvalues strictly above `floor * max|w|`, 0 for an empty
   matrix.
