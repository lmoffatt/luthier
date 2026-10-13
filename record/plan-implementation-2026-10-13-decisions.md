# Implementing the specification: the decisions

Draft 0, 2026-10-13, at ee8e9ad. The specification is decided in substance (D-2026-10-13-g) and
the interpreter lags it: most of what was decided since 2026-10-11 is not in `src/`. This document
holds the choices that are yours; `plan-implementation-2026-10-13-execution.md` holds the steps.
One bite per screen. Mark under each: "ok", "no", or a comment.

## D1. The order: five phases, by dependency

1. **The surface and the world.** The keywords of D-2026-10-12-ab and `W` (D-2026-10-13-b): the
   lexer keeps `data`, `match`, `if`, `then`, `else`, `U`, `W` (and `operator`); `extern`,
   `primitive`, `axiom`, `cite`, `provisional` become names of core; `W` gets its rules.
2. **Files and modules.** A file read when a demand needs it (D-2026-10-12-ac, -ad): externs as
   routes, imports lazy, modules as values, `import "x.lut" Name as Alias`, core enclosing every
   file, and the private part by ascription (D-2026-10-13-c).
3. **Tests and generators.** `test` as a function with named arguments, bindings and profiles, the
   functors of chapter 7, `gen` removed.
4. **Certification over costs.** `lib/certification.lut` over `C`, a first library of costs,
   `Certificate` abstract, the library of checks with `Failures E`.
5. **The demand and the memo.** The open demand, the plan as a value, the result store keyed by
   what the cone reads.

Why this order: each phase uses the one before it. `Certificate` abstract needs the private part
(phase 2); `gen` can go only when bindings exist (phase 3); the memo needs files read on demand,
since a file's hash is part of a result's key (phase 2). Recommended as listed.

## D2. Migrating the `.lut` files

Phases 1 to 3 change the syntax of nearly every file: 73 in this repository (19 libraries, the
examples, `tests/spec/`) and 46 in sonolocalización. Two ways:

- **(a) A script per phase, and only the new syntax afterwards.** `scripts/migrate_lut.py` rewrites
  the old forms; the parser stops reading them in the same commit. Git keeps the old files (P6).
- **(b) Both syntaxes for a while**, the old with a warning, removed at a milestone.

Recommended (a): (b) is a period in which every rule has two forms to test, which is the
bureaucracy P8 warns about, and a script is undone by one commit. Its cost: sonolocalización
breaks on the day of each phase until the script runs there too. Since that repository is yours
and its runs are yours to make, the question inside the question is whether I may run the
migration script there (it rewrites code, it processes no data), or you do.

## D3. Recertifying

Every change to the interpreter invalidates every certificate (the interpreter is in the hash,
spec 6.S8). Certifying luthier's libraries takes tens of minutes; sonolocalización took hours.

Recommended: the libraries of this repository are recertified at the end of each phase, by the
session (`luthier certify` is among what the model may run); sonolocalización only at a milestone
(D7), by you. Between milestones its certificates are stale and `run`, strict since
D-2026-10-12-y, refuses its cones: that repository does not run between milestones.

## D4. `W` is used exactly once

D-2026-10-13-b says each value of `W` is used once. "At most once" (Clean's uniqueness, affine)
forbids duplicating the world; "exactly once" (linear) also forbids dropping it. With evaluation
forward on demand (D-2026-10-10-d) the difference matters: an action whose new token nobody uses is
not demanded, so it would never run, silently. Exactly once makes every action lie on the chain
that reaches the output of `main` or of the session.

Recommended: exactly once, checked by the checker per block; the last token of a block is its
output or is passed on.

## D5. What a module shows without ascription

D-2026-10-13-c hides what a theory does not name when the importer gives the module a theory as
its type. Without one (`la := import "x.lut"`), the importer can see either everything the file
defines, as today, or nothing.

Recommended: everything. Ascription is then the way to hide, the migration costs nothing, and a
library that wants a private part says so by the theory it exports. What must never be built
outside its theory (a `Certificate`) is protected by the library that holds it being imported
only through that theory, which phase 4 does for `lib/certification.lut`.

## D6. Who writes it

The checker's new rules (linearity of `W`, lazy files, ascription) touch `checker.py` (2300
lines) where the rules interact; the rest is well fenced by the specification (the migration
script, the programs of `tests/spec/` from each rule, the generators, the libraries of costs and
checks).

Recommended: an Opus session for the checker and the evaluator, phase by phase; Sonnet agents in
worktrees for the fenced parts, in parallel, with a brief each as for the chapters; the session
that integrates reads every diff, runs the suites and flips each item of the specification from
`[decided]` to `[implemented]` only with its accept and reject programs passing.

## D7. Milestones

Push only tagged milestones (working rule). Recommended: `v0.2` after phases 1 and 2 (the new
surface, files and modules), `v0.3` after phases 3 and 4 (tests and certification), `v0.4` after
phase 5. At each, sonolocalización is migrated and recertified (D3), and the tag is pushed.
