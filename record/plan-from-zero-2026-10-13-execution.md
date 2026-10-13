# Luthier from zero: the execution

Draft 0, 2026-10-13, at 23792d3. Written for the sessions that carry it out, including one with no
memory of the chat: everything it needs is in files, and the status lines below are updated at each
step. It rests on D-2026-10-13-h and on Z1 to Z7 of `plan-from-zero-2026-10-13-decisions.md`;
until Luciano marks them, every step assumes them as recommended and says so in its commit.

## Status

- 2026-10-13: plan written; Z1 to Z7 with Luciano; nothing started.

## Rules for every step

- Commit before every change; one theory or one specimen, at least one commit; the message names the
  specification items it states or implements.
- A theory states what its chapters say, item by item, citing them (`-- spec 4.R3`) above each law;
  it adds nothing the specification does not say, and where the specification is silent or wrong it
  stops and asks one question (W15).
- A theory is in the syntax of chapter 2 as decided, including D-2026-10-12-ab (keywords),
  D-2026-10-13-b (`W`), Z5 (import with its theory) and D9 (top-level `test` lines as data).
- From step 1 on, every theory passes the parser; from step 4 on, the checker.
- An item of `docs/spec/` moves to `[implemented]` only when its Python specimen runs it and its
  programs in `tests/spec/` pass.
- Agents: Sonnet, in a worktree, with a brief from `record/spec-brief-template.md` adapted (goal,
  the chapters and items to state, the theories it may cite, what not to touch, the parser or
  checker that closes it, the report). The worktree starts at an older commit; the agent
  fast-forwards to the brief's commit. The session reads every file whole, runs the checks,
  commits, removes the worktree and its branch.
- The lints stay: `scripts/check_spec.py`, `scripts/project_principles.py --check --strict`,
  `scripts/check_quotes.py`; their tests stay in `tests/`.

## Step 0. Retire the old code (Z4)

1. Tag `v0.1-final` at the commit before this step.
2. Remove from the tree: `src/luthier/*.py` except `arrays.py`, `tables.py`, `rational.py` and
   `__init__.py`; `src/luthier/core.lut` and `src/luthier/lib/` with their certificates;
   `examples/`; the interpreter's tests (`tests/test_bridge.py`, `test_certificates.py`,
   `test_checker_rules.py`, `test_evaluators.py`, `test_kernel.py`, `test_spec.py`,
   `test_sugar.py`, `bridge_externs.py`) and `luthier.lock`. List what was removed, with the tag, in
   the commit message and in `record/spec-drafts.md`.
3. Move `tests/spec/*.lut` to `tests/spec/v0.1/`, read only: the cases to rewrite in step 4.
4. `pyproject.toml` (or the package setup) keeps the `luthier` package with the three host modules;
   the `luthier` command is removed until step 4 brings it back.

## Step 1. The grammar and the parser (Z3; layer 0)

1. `src/luthier/lib/grammar.lut`: chapter 2 as a theory, the surface syntax as `data` (L14),
   with the keywords of 2.S21 and `W`, the import of Z5, blocks (2.S17), the translations of §4.
   By the session.
2. *Agent.* `src/luthier/parse.py`: a parser for that grammar, syntax only, producing the surface
   tree; `luthier parse files` prints errors with lines; tests with the examples of chapter 2.
   It is the specimen of `grammar.lut`, certified against it once the checker exists.

## Step 2. The kernel's theories (layer 0, by the session)

1. `src/luthier/lib/kernel_laws.lut`: the laws every structure satisfies by construction (3.S36),
   with the laws of structural `==` (reflexive, symmetric, transitive, substitutive;
   D-2026-10-12-ak).
2. `src/luthier/lib/term.lut`: `Term`, `Pattern`, `Act`, `Program` as `data` (3.S29),
   alpha-equivalence (3.S31), the canonical form (3.S34), substitution, `reduce` with beta, delta,
   iota, prim, extern (3.S33, §4 of chapter 3), `quote` and `eval` (3.S32).
3. Both pass the parser.

## Step 3. The checker's theories (layer 1, agents in parallel)

1. `src/luthier/lib/program.lut`: `WellFormed : Program -> Failures E` with one law per rule of
   chapter 4 (4.R1 to 4.R13, 4.R14 for `W` with D4 and D8, 4.R11, 4.S17, 4.S23, 4.S24), each law
   citing its rule (4.S21).
2. `src/luthier/lib/laws.lut`: `LawValue` and `verdict` (5.S3), the relations moved from algebra
   (D-2026-10-11-l), lift and exact (5.S5). A law as a theory (D-2026-10-13-l): `Law`, `forall`, `exists` and the
   connectives, `then` material; the evidence of each form.
3. `src/luthier/lib/checks.lut`: `Failures E`, the projections, composition (5.S9 to 5.S11).
4. `src/luthier/lib/library.lut`: a file as a record type (12.S1), modules, the import of Z5, core
   enclosing every file, laziness (12.S21), ascription (L6.12).
5. All pass the parser; the session reads each whole and reconciles names across them.

## Step 4. The Python checker and evaluator (layers 0 and 1)

1. `src/luthier/kernel.py` (terms and reduction, the specimen of `term.lut`) and
   `src/luthier/check.py` (the specimen of `program.lut`), by the session; `luthier check files`.
2. *Agent.* Rewrite the 50 programs of `tests/spec/v0.1/` into the new syntax in `tests/spec/`,
   each keeping its rule and its `-- expect:` line; `tests/test_spec.py` anew.
3. The theories of steps 1 to 3 pass the checker; the programs pass; the items of chapters 2 to 4
   flip to `[implemented]` as their programs pass.
4. Milestone `v0.2` (Z7).

## Step 5. Evidence (layer 2)

1. *Agents.* Two cost types, `Distance` for the values of laws and `Evidence` for what samples
   give (D-2026-10-13-m), with the interface of 6.S5 split between them and refined here.
   `src/luthier/lib/certification.lut` (6.S16: `CostAlgebra C` with its six laws,
   `Certificate C`, `grade`, `transport`, `compose`, `serves`); `src/luthier/lib/cost.lut`, a first
   model (`⊕` the sum over [0, ∞]); `src/luthier/lib/test.lut` (7.S20, `TestSpec` of D9) and
   `src/luthier/lib/generators.lut` (7.S1 to 7.S8).
2. Their Python specimens: the certifier (certificates by hash of the canonical cone, 6.S8, with the
   chain kept), the tester, the generators; `luthier test`, `luthier certify`; the statistical laws
   (7.S17 to 7.S19).
3. Milestone `v0.3`.

## Step 6. Execution (layer 3)

1. *Agents.* `src/luthier/lib/demand.lut` (8.S1, 8.S2), `src/luthier/lib/plan.lut` (8.S4, 8.S8,
   8.S11), `src/luthier/lib/world.lut` with `print` (10.S5, 10.S13, D8),
   `src/luthier/lib/number_model.lut` and `src/luthier/lib/rational.lut` (11).
2. Their Python specimens: `run` (strict, 12.S17), `eval`, `session`, the result store keyed by what
   the cone reads; externs read when a demand reaches them, validated at the first action (10.S8 to
   10.S10), calling the host modules kept in step 0.
3. Milestone `v0.4`.

## After

The domain libraries rewritten over the new language (Z1); `planner.lut` and the planner (chapter
9); the decorated demand of 8.S1 (ask Luciano how the generic form is obtained); sonolocalización
redone by Luciano.

## If the session that reads this has no memory of the chat

The specification in `docs/spec/` is the authority; `record/decisions.md` holds why, the latest of
2026-10-13 (-a to -h). The old interpreter is at the tag `v0.1-final` and is not a source: read it
only to learn what a host function did. Luciano reads Spanish in chat; written material is in
English. He runs the scripts that process data; the model may run the lints, the parser, `luthier
check` and `luthier certify` here.
