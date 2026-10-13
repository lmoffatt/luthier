# Specification programs in the current syntax

This directory contains the 48 programs migrated from `v0.1/`, with the same filenames,
plus this README and the unchanged `cite_sources.bib`: 50 files in total. The retired suite
is preserved in `v0.1/`. Sources are the current items cited in each program, the original
program at the commit and SHA-256 in its header, and the migration brief
`record/IA/spec-programs-2026-10-13/prompt.md`. Migration version: spec-programs v1;
deterministic, no seed or other generation parameters. The migration report and its
questions are in `record/IA/spec-programs-2026-10-13/codex.md`.

These are cases for the future checker, not evidence that semantic checking passes today.
An `.accept.lut` program is intended to pass; a `.reject.lut` program is intended to fail
its cited rule. `r4_data_nonrecursive.reject.lut` still rejects, for a new reason: its constructors have
no law of their role (spec 4.R3, L2.7), not that it lacks recursion.

`-- expect:` carries a diagnostic fragment explicitly specified by the current text
(the repeated-definition case, spec 4.R12). Where the specification gives no literal
diagnostic, `-- expect (v0.1):` preserves the old fragment without prescribing the new
checker's wording. Headers replace the old chapter references with current items.
For programs named in prose rather than a `Files:` line, the header cites that item;
spec 4.S18's additional cases also cite the rule that explains their verdict.

The recursive `Tree` and `N` programs now state fold equations in theories that claim
them (spec 4.R3, spec 4.S14). The array program states the minimal `Vec` alias of
spec 11.S9 locally. Citation programs state the former reference library's native
identifier record and resolvability law locally, citing `v0.1-final` in the comments.
These programs import no retired library. Unimported programs may hold theories and
models together under spec 12.S23.

The citation programs contain explicitly marked proposals where spec 6.R1 leaves
O10 open: `cite w value reference (checked <- "human")`, returning `W * Unit`, and
`"ai+human"` as the other checker value used here. They put certificate-writing actions
inside `main` and thread the world token (spec 10.S2 to spec 10.S5). The named, typed
`.bib` import applies spec 12.S22 to spec 12.R1; the missing current `Reference` interface
and the import's interpretation remain questions in the report. Parser acceptance does
not settle those interfaces. There are no retired `let`, `test`, or `eval` forms to
migrate in these 48 programs. Provisional externs use `(provisional <- true)`.

Syntax checks, run from the repository root with the package available:

```sh
python3 -m luthier.cli parse tests/spec/*.lut
python3 scripts/check_spec.py
```

The first command intentionally exits 1 on `r12_toplevel_arrow.reject.lut`: its whole
case is `x <- 1`, which spec 2.R5 forbids and `luthierSyntax` excludes. The other 47
programs parse. Keeping this negative case conflicts with requiring every fixture to
parse; the report records the exact error. This is a syntax rejection, not a parser defect.
A future runner must treat that case as an expected syntax failure, use the explicit
verdict override, and distinguish current diagnostic fragments from historical ones.
No suite runner or semantic checker for these programs is present yet.
