# Brief: chapter 7, Tests and generators

Read `record/spec-briefs/common.md` and `record/spec-brief-template.md` first.

## Goal

Write `docs/spec/07-tests.md`, chapter 7 of the specification: how `luthier test` draws the cases
of a law, how a test names its generators, the budgets, the statistical laws with their level and
power, and what a certificate entry records of the test, with the grades of Terms. The old file
`docs/spec/08-tests.md` is your main source and stays in place; the integrator deletes it.

## Sources

- `docs/spec/08-tests.md` at d12b554, whole. Its items G1 to G12, C1 to C10 become `7.Sk` or
  `7.Rk` in the same order (a rule where a program can be accepted or rejected, a statement
  otherwise); keep its decisions list at the top as the chapter's header paragraph (they were
  Luciano's of 2026-10-06; they have no decision ids: the items that rest on them are `[proposed]`
  unless implemented, and your report lists them under "decided without an id"). §12 (changes to
  other parts) is not part of the chapter: chapter 2 applies the grammar changes; say so in one
  line. §13 (order of work) is not part of the chapter: drop it and say so in the report.
- `docs/principles.md`: L10 (the certificate), in particular L10.3 (the conversion of a sample's
  statistics to an evidence cost, D-2026-10-12-r), L5.18 (no unrecorded policy constants: every
  budget an argument), L9 (a certifier produces the evidence), Terms (the five grades).
- `src/luthier/generators.py`, `testing.py`, `certify.py` (read only) to decide what is
  `[implemented]`; `src/luthier/lib/random.lut` for `Gen`.

## What changes against the source

- Grades (D-2026-10-12-y): C2's list (point, census of k, sampled n, bounded, exhaustive,
  witnessed, assumed) becomes the five of Terms with the domain and the evidence cost carrying the
  rest: point is cases with one case; census of k is cases; bounded is exhaustive on the box the
  domain names; witnessed is cases with a witness; sampled n carries its evidence cost. Say this
  in C2's statement and cite `spec 6` for the certificate's fields.
- C2's bound 3/n at 95% (Hanley and Lippman-Hand) is the first instance of the conversion of
  D-2026-10-12-r: write it as `[decided D-2026-10-12-r]`: the evidence cost of a sampled law is
  −log(1 − ε̂(n, δ)) in nats, with ε̂ the bound on the failure fraction (3/n at δ = 0.05 with no
  failure seen), δ the demand's parameter; the conversion is a function with a declared shape,
  the sample's statistics and δ in, a cost out, filled per theory; name `lib/evidence.lut` as the
  file that would state it, `[proposed]`.
- Budgets (G12): every budget is an argument of the test, recorded in the entry; cite L5.18.
- Statistical laws (C8 to C10): keep; their level α and power β are parameters of the demand
  (L5.18); the verdict with its level is the form `spec 5` gives (cite).
- Certificates of definitions and of results (C1, C6, C7): keep what is about the test (what the
  entry records of the generators, the reach, the known outcome); the identity of a certificate,
  its transport and certification by default are `spec 6` (cite L10.4 to L10.7 and `spec 6`).
- L14: generators are values of Luthier (G1) already; state that the generic generators (G2, G3)
  and the families (G8) are to be written in `lib/generators.lut` and `lib/array.lut`, naming
  what exists today in `lib/random.lut`, `[proposed]` for the rest.
- `## Open`: O1 (the conversion and the algebra), O5 (decorated outputs, for the error), and the
  source's §11 items as citations of O ids where one exists, otherwise as "decided without an id"
  or dropped with a line in the report.

## Length

The source is about 4400 words; the chapter should be about 4000. Keep the words of the items.
