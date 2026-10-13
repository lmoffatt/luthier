# Implementing the specification: the decisions

> Superseded on 2026-10-13 by D-2026-10-13-h (start from zero) and `record/plan-from-zero-2026-10-13-decisions.md`; kept for its D4, D8 and D9 and for Luciano's annotations below, unedited.

Draft 1, 2026-10-13, at a563fd2 (draft 0 reviewed the same day: D8 and D9 added, D3 and D6
corrected). The specification is decided in substance (D-2026-10-13-g) and
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


a

## D3. Recertifying

Every change to the interpreter invalidates every certificate (the interpreter is in the hash,
spec 6.S8). Certifying luthier's libraries takes tens of minutes; sonolocalización took hours.

Recommended: the libraries of this repository are recertified at the end of each phase, by the
session (`luthier certify` is among what the model may run); sonolocalización only at a milestone
(D7), by you. `run` becomes strict in phase 1 (spec 12.S17, your "empecemos siendo estrictos"):
from then on, between milestones, sonolocalización's certificates are stale and `run` refuses its
cones, so that repository does not run between milestones. If you need it to run meanwhile, the
alternative is to make `run` strict only at `v0.3`, when certificates mean what the specification
says.

OK, first finish luthier transformation, then I will apply it. I have to redo everything anyway.


## D4. `W` is used exactly once

D-2026-10-13-b says each value of `W` is used once. "At most once" (Clean's uniqueness, affine)
forbids duplicating the world; "exactly once" (linear) also forbids dropping it. With evaluation
forward on demand (D-2026-10-10-d) the difference matters: an action whose new token nobody uses is
not demanded, so it would never run, silently. Exactly once makes every action lie on the chain
that reaches the output of `main` or of the session.

Recommended: exactly once, checked by the checker per block; the last token of a block is its
output or is passed on.

esto es raro. Porque solo una vez? 
vos podes alterar el mundo secuencialmente, de hecho eso es lo normal, aclarame de que estamos hablando aqui



## D5. What a module shows without ascription

D-2026-10-13-c hides what a theory does not name when the importer gives the module a theory as
its type. Without one (`la := import "x.lut"`), the importer can see either everything the file
defines, as today, or nothing.

Recommended: everything. Ascription is then the way to hide, the migration costs nothing, and a
library that wants a private part says so by the theory it exports. What must never be built
outside its theory (a `Certificate`) is protected by the library that holds it being imported
only through that theory, which phase 4 does for `lib/certification.lut`.


Explicame cuidadosamente ascription. 
Yo desarrolle una logica para no leer los files a menos que haga falta, por lo cual los nombres que estan en el file deben estar accesibles sin leerlo, eso se logra con   import "x.lut" myModel. 
Si vos haces import "x.lut", no se sabe lo que hay en x.lut hasta que no se leyo y eso genera dudas de que carajo hay en x.lut hasta no verlo, es decir que no tenemos garantias de que hay en cada lado. en este caso vos podes verificar si en x.lut esta MyModel y si esta lo importas cuando te lo pidan y si no esta tiras un error. 



## D6. Who writes it

The checker's new rules (linearity of `W`, lazy files, ascription) touch `checker.py` (2300
lines) where the rules interact; the rest is well fenced by the specification (the migration
script, the programs of `tests/spec/` from each rule, the generators, the libraries of costs and
checks).

Recommended: the session you run, whatever its model, for the checker and the evaluator, phase by
phase; Sonnet agents in worktrees for the fenced parts (the migration script, the lexer and parser
change of phase 1, the generators, the libraries of costs and checks, the matrix families), in
parallel, with a brief each as for the chapters; the session that integrates reads every diff,
runs the suites and flips each item of the specification from `[decided]` to `[implemented]` only
with its accept and reject programs passing.




## D7. Milestones

Push only tagged milestones (working rule). Recommended: `v0.2` after phases 1 and 2 (the new
surface, files and modules), `v0.3` after phases 3 and 4 (tests and certification), `v0.4` after
phase 5. At each, sonolocalización is migrated and recertified (D3), and the tag is pushed.

## D8. `main` without actions, and what a `main` with `W` returns

Nearly every `main` today is pure: it computes a value and acts on nothing. If `W` always enters
`main` and must be used exactly once (D4), a pure `main` would have to pass the token through
untouched, which is what "exactly once" is meant to forbid.

Recommended: `W` is optional in `main`. A `main` that takes no `W` is a pure script, evaluated and
printed as today, and no action may occur in it. A `main` that takes `w : W` returns the final
token with its result, `W * A`; the session is the same with its implicit `w`. Until a library
defines an action, a `main` with `W` has nothing to call, so phase 1 adds one action, `print`, to
core, so that the rule of `W` has a real case.

## D9. Where tests live

`test` is a function (7.S20) and an action on Luthier's own state (D-2026-10-12-m), so it takes
`W`. But an action may not occur at a file's top level (10.S2), and today 116 lines of the form
`test f with 100` sit at the top level of the files of sonolocalización, and more in the
libraries. Two readings:

- **(a) The top-level `test` lines are data.** `test f with 100` declares what to test and how,
  a value of a record type `TestSpec`, kept in the module; the action is `test "x.lut"`
  (D-2026-10-12-ad), which runs every declared test of the module, and `luthier test` is that
  action from the command line. The lines keep their place; only their meaning changes.
- **(b) Tests move into a block**, `tests := { w <- test w f (n := 100) ; ... }`, and the top level
  holds no `test` line.

Recommended (a): it keeps the files as they are, it fits D-2026-10-12-ad (the module's `test` is
the total demand), and it separates what a module says about itself (data, declarative face) from
running it (an action). (b) puts an action chain in every library for no gain.
