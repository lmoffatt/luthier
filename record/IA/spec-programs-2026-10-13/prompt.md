# The specification's programs in the new syntax: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 for Luciano, who gives it
to Codex working in this repository once the parser (`src/luthier/parse.py`, step 1.2) is in the
tree. Step 4.2 of `record/plan-from-zero-2026-10-13-execution.md`, brought forward because it needs
only the parser; Z9, D-2026-10-13-r.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `tests/spec/v0.1/` holds 50 programs, about
240 lines, written for the retired interpreter (tag `v0.1-final`): one accept and one reject program
per rule of the checker, a rejected one carrying the fragment of its error in `-- expect: ...`. The
specification in `docs/spec/` names them on its `Files:` lines. Rewrite them into the language as
now specified, in `tests/spec/`, so that the new checker (not written yet) has its cases.

For each program `tests/spec/v0.1/<name>`:

1. Write `tests/spec/<name>`, same file name, so that the `Files:` lines of the specification still
   resolve. Keep what the program tests: its rule, its accept or reject verdict, its `-- expect:`
   fragment.
2. Its header comment cites the rule by its current item (`spec 4.R4`, `spec 3.S7`), found by the
   `Files:` line that names the file; the old section numbers (`05 §7`, `R4`) go.
3. The syntax is chapter 2's as `luthierSyntax` in `src/luthier/lib/grammar.lth` gives it (its
   generated form is in 2.S9). In particular: `let` is gone (blocks, 2.S17); `test` and `cite` are
   functions (2.S21); an import names what enters, `import "x.lth" Theory` or
   `import "x.lut" Model : Theory` (12.S22); `eval` is a name of core. A program no other file
   imports may hold theory and model together (12.S23, Z8). A program that imported a library of
   v0.1 that no longer exists (`reference`, ...) becomes self-contained: state in it the little it
   needs.
4. Where the rule itself changed since v0.1, the program follows the specification as it reads
   now, and its verdict may flip. The changes you will meet: a `data` need not be recursive, but
   each constructor needs a law of its role, else it is a collection to be written as an alias
   (3.R3, 4.R3, 4.R4, L2.7 in `docs/principles.md`); laws are claimed by a theory's definition
   (4.S14); `W` and the world (spec 10); numbers (spec 11). Read the items the `Files:` line sits
   under before rewriting.
5. Where the specification states the error message, the `-- expect:` fragment is taken from it;
   where it does not, keep the old fragment as `-- expect (v0.1): ...`.

Then rewrite `tests/spec/README.md` for the new suite, and copy `cite_sources.bib` if a program
still uses it.

Check: `luthier parse tests/spec/*.lut tests/spec/*.lth` (or `python3 -m luthier.cli parse ...`)
parses every file; `python3 scripts/check_spec.py` passes. Do not touch `tests/spec/v0.1/`,
`docs/`, `src/`, `scripts/`, or `record/` except your report. Do not commit: leave the changes in
the working tree. Write your report to `record/IA/spec-programs-2026-10-13/codex.md`, in English:
a table of the 50 files with one column saying kept, rewritten, or verdict flipped (and by which
item), then every place where the specification did not tell you what the program should be, as
one question each. If the parser rejects a program you believe is right by chapter 2, do not change
the parser: list the text and the error.
