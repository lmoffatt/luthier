# Brief: chapter 12, Files and tools

Read `record/spec-briefs/common.md` and `record/spec-brief-template.md` first.

## Goal

Write `docs/spec/12-files-and-tools.md`, chapter 12 of the specification: what a file is, how it
is imported, what travels with it, and the commands of the interpreter with what each one
requires. The old file `docs/spec/03-libraries.md` is your main source and stays in place; the
integrator deletes it.

## Sources

- `docs/spec/03-libraries.md` at d12b554: §1 (a file is a structure), §2 (import), §3
  (declaration in one file, definition in another), §4 (what travels: the certificate with its
  hash, at the level of import; the certificate's own fields are `spec 6`, cite). §5 (the
  libraries' table) is not part of the chapter (D-2026-10-12-y: the libraries' content is the
  manual's); drop it and say so in the report. §6 (open) becomes O ids or "decided without an id".
- `docs/spec/05-static-semantics.md` §7 at d12b554, the paragraphs "As implemented" and "Added
  2026-10-06", for what `test`, `run`, `certify` and `check -v` do today; and `02-grammar.md` §8
  for `luthier session` as implemented.
- `docs/principles.md`: L5 (the demand), L10 (the certificate, in particular L10.6:
  certification is the default, no opt-out at the start), L14 (the theory of libraries written in
  Luthier), L11 (extern, provisional), Terms.
- `src/luthier/cli.py` (read only) for the commands and their options as implemented.

## What changes against the source

- §1 as a statement: a `.lut` file denotes a value of a dependent record type; this is the theory
  of libraries, to be written in Luthier as `lib/library.lut` (L14), `[proposed]`; what is
  implemented (prefixing of names) `[implemented]`.
- §2, §3 as rules and statements with status and, where `tests/spec/` has programs for them
  (look; there may be none), their files.
- §4: what an importer reads and accepts (by hash, unchanged), stale entries, `--deep`; cite
  `spec 6` for the identity of an entry (L10.4) and for what a certificate records.
- The commands, one statement each: `check` (and `-v`: provisional externs, holes the entry
  depends on, axioms, loose functions), `test` (with the directive's options, cite `spec 7`),
  `certify`, `run`, `eval`, `session` (cite `spec 8` for its semantics). For `run`:
  D-2026-10-12-y, strict from the start: `run` refuses a cone with an uncertified or provisional
  name; `--require-certified` becomes the default and is retired; there is no opt-out flag (O3,
  if a real case asks). Mark this `[decided D-2026-10-12-y]`; what `run` records in `.run.json`
  `[implemented]` as the source says.
- `luthier run --set name=value` for holes (from 06 §6) belongs here: state it.
- `## Open`: O3 (the opt-out, none at the start), O8 (the session's memo), and the source's §6
  items (modules as values, visibility, Python dependencies declared nowhere, a provisional import,
  a minimum grade required by an importer) as "decided without an id" or `[proposed]` statements,
  noting that the last one is answered by the demand's cutoff (L10.5).

## Length

About 1500 words.
