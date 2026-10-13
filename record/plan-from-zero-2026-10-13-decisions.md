# Luthier from zero: the decisions

Draft 0, 2026-10-13, at 23792d3. D-2026-10-13-h: Luthier starts again from zero; first its
theories, written in Luthier, then the Python files that implement them, then Luthier
implementations where the kernel can say them. The specification (`docs/spec/`) is the authority
for both. This document holds what is yours to choose; `plan-from-zero-2026-10-13-execution.md`
holds the steps. One bite per screen; mark "ok", "no" or a comment under each.

From the superseded plan (`plan-implementation-2026-10-13-decisions.md`), still in force: D4 (each
token of `W` is consumed exactly once; the world changes as often as one likes, one token after
another), D8 (`W` optional in `main`; `print` as the first action), D9 (top-level `test` lines are
data; `test "x.lut"` is the action). Your marks there: D2 (a), D3 ok, to apply in sonolocalización
once Luthier is done.

## Z1. Two groups of theories, Luthier's own first

The theories of Luthier itself, the files the specification names: the grammar, the kernel and its
laws, terms and programs as data, the checker's rules as the laws of `WellFormed`, laws and checks,
modules, certification over costs, tests and generators, the demand and the plan, the world, the
number models. About thirteen files. Then the domain libraries (`algebra`, `array`,
`probability`, `table`, `belief`, `optimization`), which use Luthier and do not define it.

Recommended: Luthier's own first, the domain libraries after, written with the language running. 

Yes, Luthiers own first, specially the ones that allow bootstrapping

## Z2. Layers, so that each theory rests on written ones

- Layer 0, the surface and the kernel: `grammar.lut` (chapter 2), `kernel_laws.lut` with the laws of
  `==` (3.S36, D-2026-10-12-ak), `term.lut` (3.S29 to 3.S38).
- Layer 1, the checker: `program.lut`, the rules as the laws of `WellFormed` (4.S21, with `W`'s
  rule); `laws.lut` with `verdict` (5.S3); `checks.lut` (5.S10); `library.lut`, modules and import
  (12.S1, 12.S22).
- Layer 2, evidence: `certification.lut` (6.S16) with a first cost model; `test.lut` and
  `generators.lut` (7).
- Layer 3, execution: `demand.lut`, `plan.lut` (8); `world.lut` with `print` (10); `number_model.lut`
  and `rational.lut` (11).
- After: `planner.lut` (9).

Recommended as listed. Each layer's Python specimen is written once its theories are, and before the
next layer's theories, so that a layer's theories are checked by the checker the layer below built.

## Z3. A parser first, to check syntax while the theories are written

Without an interpreter a theory in the new syntax is checked by nobody. Chapter 2 fixes the grammar,
so a parser is a fenced task. Recommended: `grammar.lut` first, then its Python specimen, a parser
that only reads (no types, no evaluation), run on every theory as it is written. Errors of syntax
then appear one file at a time; errors of meaning wait for the checker of layer 1.

OK

## Z4. Retiring the old code

Recommended: tag the present state `v0.1-final`; remove from the tree the old interpreter
(`src/luthier/*.py` except the three below), the old libraries and examples in the old syntax, and
their certificates; git keeps all of it. Kept: the host functions the externs call, `arrays.py`,
`tables.py`, `rational.py`, which depend on nothing of the interpreter (numpy, csv, the standard
library) and are specimens of the world (L11), not interpreter; and the 50 programs of
`tests/spec/`, which encode the rules of the specification and are rewritten into the new syntax
as the cases of the new checker. Sonolocalización keeps using `v0.1-final` until you redo it.

OK

## Z5. Import names what enters, with its theory

Your annotation on D5: a file is not read unless needed, so what enters must be known without
reading it, which `import "x.lut" MyModel` gives, and `import "x.lut"` alone does not. To check the
importer without reading `x.lut`, the checker needs the type of `MyModel` too, so the import line
carries it:

    import "x.lut" MyModel : LinearAlgebra
    import "x.lut" MyModel : LinearAlgebra as LA

The importer is checked against `LinearAlgebra` alone; when a demand first needs `MyModel`, the
file is read and the checker verifies that it defines `MyModel` as a model of `LinearAlgebra`, an
error otherwise; and the importer sees only what `LinearAlgebra` names, which is the private part
(ascription, D-2026-10-13-c). There is no import without names, and `la := import "x.lut"`
(D-2026-10-12-ad) goes. Core is the exception: it encloses every file (D-2026-10-12-af).

Recommended: this form, amending D-2026-10-12-ad, -af and D-2026-10-13-c; spec 12.S3, 12.S22 and
L6.12 follow.

OK, of course LinearAlgebra had to be imported from a .lth first

## Z6. Who writes the theories

The theories are the specification said in Luthier; each layer has its chapters as source.
Recommended: layer 0 by the session you run, since it fixes the style every other theory follows;
layers 1 to 3 by Sonnet agents in worktrees, one per theory or per small group, in parallel within a
layer, with a brief each; the session integrates, runs the parser and, from layer 1 on, the checker.
The Python specimens: the checker and the evaluator by the session, the rest (parser, certifier,
generators, the cost model) by agents.

Ok

## Z7. Milestones

Recommended: `v0.2` when layers 0 and 1 have their theories and their Python checker, and the 50
programs of `tests/spec/`, rewritten, pass; `v0.3` with layer 2 (certification and tests);
`v0.4` with layer 3 (run, session, world). Push only tags.

ok

## Z8. Theory files and model files

Your proposal (D-2026-10-13-i, refined by D-2026-10-13-j): theories and models in separate files,
as C++ headers and implementations, so that different models of one theory live in different files.
A theory file holds types, declarations and laws. A model file holds one value of a theory, native
or extern, or a functor: an algorithm written against a theory without naming a model
(`gramSchmidt (M : LinearAlgebra) : Orthonormalizer M`), instantiated with any model and certified
per instance. There is no duplication between the two files, since laws and implementation are
different things, except where something is defined by its implementation. Every type has laws,
at the least those of its equality (D-2026-10-12-ak); data enters from the world as a `String` and
a check refines it into its lawful type once (spec 5.S9, 5.S12). What another file imports has its
theory in a `.lth`; what no file imports (a `main`, a local helper) may live whole in a `.lut`. The checker reads theory files; a
model file is read only when a demand needs its model, and is certified against its theory. This
is where the theory named in an import line (Z5) comes from:

    import "linear_algebra.lth" LinearAlgebra
    import "linear_algebra_numpy.lut" Numpy : LinearAlgebra

Each model brings its own dependencies (numpy, Python) and its own certificate; the planner sees
them as specimens of one theory (L6). Today's `array.lut` mixes the theory with its native model;
`array_python.lut` is a second model; this makes the pattern of 12.S9 a rule.

Recommended: enforced, not a convention. A theory file has its own extension, `.lth`, and the
checker rejects an `extern`, an action or a model value inside it, because laziness rests on a
theory file never touching the world. In the plan, step 3's `library.lut` states the two kinds,
and every theory of Luthier is written as a `.lth`.

Yes, enforced
