# Implementing the specification: the execution

Draft 1, 2026-10-13, at a563fd2 (draft 0 reviewed the same day). Written for the sessions that carry it out, including one with no
memory of the chat: everything it needs is in files, and the status lines below are updated at
each step. The choices it rests on are D1 to D9 of `plan-implementation-2026-10-13-decisions.md`;
until Luciano marks them, every step assumes them as recommended and says so in its commit.

## Status

- 2026-10-13: plan written; D1 to D7 with Luciano; nothing started.
- 2026-10-13, reviewed: D8 (`main` and `W`) and D9 (where tests live) added, 12.S17 and the
  omitted items scheduled, `print` as the first action; D1 to D9 with Luciano.

## Rules for every step

- Commit before every change; one step, at least one commit; the message names the specification
  items it implements and the decisions it rests on.
- An item of `docs/spec/` moves from `[decided ...]` to `[implemented]` only in the commit where
  its accept and reject programs exist in `tests/spec/` and pass (`python3 -m pytest
  tests/test_spec.py -q`); a statement with no program says in its text what runs.
- The specification is not changed by implementing it. A step that finds the specification wrong
  or silent stops and asks one question (W15); a typo or a citation is fixed in passing.
- Before closing a step: `python3 scripts/check_spec.py`, `python3 scripts/project_principles.py
  --check --strict`, and the whole suite, `python3 -m pytest tests -q`.
- At the end of each phase: `luthier certify` on the libraries of `src/luthier/lib/` and on
  `examples/` (D3), certificates committed. Sonolocalización is migrated and certified only at a
  milestone, by Luciano or with his leave (D2, D3).
- Agents: Sonnet, in a worktree, for the parts marked *fenced* below, with a brief written from
  `record/spec-brief-template.md` adapted to code (goal, the specification items quoted, files it
  may touch, the tests that close it, the report). The worktree starts at an older commit; the
  agent fast-forwards to the brief's commit. The integrating session (Opus) reads the whole diff,
  runs the checks, commits, removes the worktree and its branch.

## Phase 1. The surface and the world

Realizes 2.S21, 3.S39, 4.S23, 12.S17, 12.S18, 12.S19 and D-2026-10-13-b (spec 10.S5, L4.11), with
D8.

1. *Fenced.* `scripts/migrate_lut.py`: rewrites `extern "..."` to the application of core's
   `extern` (spec 3.S39), `extern provisional "..."` to its named argument, and the bodies
   `primitive` and `axiom` likewise; `--check` lists what it would change; tests in
   `tests/test_migrate_lut.py`. Not yet `test`, `gen`, `cite` (phase 3).
2. *Fenced.* Lexer (`src/luthier/lexer.py`, KEYWORDS) and parser: the keywords of 2.S21 plus
   `W`; the names that leave the keywords are parsed as names; core (`src/luthier/core.lut`)
   declares `extern`, `primitive`, `axiom`, recognized by the checker as before. 4.S23 is kept to
   what these three need: their type is the declaration's, which the checker already holds;
   bidirectional inference in general is not this step.
3. `W` in the checker: a primitive type with no introduction and no `==` (spec 4.R8), entering
   only as an optional parameter of `main` and as the session's implicit `w` (D8); a `main` with
   `w : W` returns `W * A`; each value of type `W` used exactly once in a block (D4), the last one
   being the block's output or passed on. One action in core, `print : W -> String -> W * Unit`,
   so that the rule has a case. A new rule in chapter 4, `4.R14`, written in the same commit, with
   `w_threaded.accept.lut`, `w_used_twice.reject.lut`, `w_dropped.reject.lut`,
   `w_constructed.reject.lut` in `tests/spec/`; 10.S2 updated to name `print`.
4. `run` strict (12.S17): the refusal of an uncertified or provisional cone becomes the default,
   `--require-certified` retired; `--no-record` retired (12.S18); `eval` prints the states of the
   cone of its term (12.S19). Tests in `tests/test_certificates.py`.
5. Run the migration on this repository; suites green; certify the libraries; commit.

## Phase 2. Files and modules

Realizes 3.S40, 4.S24, 10.S8, 10.S9, 10.S10, 12.S21, 12.S22, L6.12, L11.7, D5.

1. Externs as routes: the checker records target and type without importing the module
   (`checker.py`, the `importlib.import_module` of the extern registration, today at line 877);
   the module is imported when evaluation reaches the node; its file hash enters the identity of
   the result and of the certificate (`certify.py`). Programs: an extern whose file does not exist
   and that no demand reaches is accepted (`r5_extern_absent.accept.lut`).
2. Modules as values: `import "x.lut"` gives a value of the record type of the file (12.S1);
   `la := import "x.lut"`, `la.f`; `import "x.lut" Name as Alias` as the alias of a projection
   (12.S22); no flat import; core encloses the top-level scope of every file. Lazy: the file is
   read when a name of it is first needed (the `Loader` of `cli.py`). `test "x.lut"` demands
   every name (D-2026-10-12-ad).
3. Ascription: `m : T := import "x.lut"` checks the module against the theory `T` and the importer
   sees only the fields of `T` (D5: without ascription, everything). Programs:
   `ascription_hides.reject.lut` (a name outside the theory), `ascription.accept.lut`.
4. The validation of an extern the first time an action asks for it (10.S10, L11.2): with the
   module imported at evaluation (step 1), the laws of its type are checked at that moment unless
   a certificate by hash serves; a failure refuses the extern.
5. *Fenced.* The migration script gains the import forms; run it; suites green; certify.
6. Milestone `v0.2` (D7): sonolocalización migrated and certified; tag; push.

## Phase 3. Tests and generators

Realizes 7.S20, 7.R1 to 7.R4, 7.S1 to 7.S9, 7.S12 to 7.S19, 2.S19 replaced, D-2026-10-06-ab, -ac,
with D9.

1. `test` and `cite` as functions of core with named arguments (spec 7.S20, 2.S21): `n`, `mode`,
   `size`, `bindings`, `profile`, every budget of 7.S8; a profile is a record value. Under D9 a
   top-level `test f (n := 100)` is a value of `TestSpec` kept by the module, and the action
   `test "x.lut"` (D-2026-10-12-ad), which `luthier test` runs, executes every `TestSpec` of the
   module and writes the certificate; 7.S20 and 10.S2 gain a sentence each saying so.
2. *Fenced.* `lib/generators.lut`: the functors `value`, `census`, `exhaustive`, `sampled` with the
   metrics `linear`, `log` and a weight (7.S2, 7.S3), special values (7.S4), in Luthier, with the
   host's `generators.py` as their specimen.
3. Bindings by parameter and by type, the static errors of 7.R2 to 7.R4, `gen` removed with its
   keyword; budgets as arguments recorded in the entry; `n` counts evaluated cases (7.S12); a
   known outcome not recomputed (7.S13).
4. *Fenced.* Matrix families in `lib/array.lut` (7.S5).
5. The binding in the hash of an entry (7.S9); `run` compares the values it receives with the
   reach of the certificates in its cone (7.S15); labels and coverage (7.S14).
6. Statistical laws: level declared and estimated (7.S17), a failure repeated with an independent
   seed (7.S18), power measured on controls (7.S19); the tolerances of the libraries as laws into
   the cost type wait for phase 4 (11.S18). Luciano's "Esto hay que solucionarlo" of 2026-10-06.
7. Migration of `test`, `gen`, `cite` in every file; suites green; certify.

## Phase 4. Certification over costs

Realizes 5.S3, 5.S9 to 5.S11, 6.S5 to 6.S16, 11.S13, 11.S18, 4.R11, 4.S20, L10.10,
D-2026-10-12-al, -am.

1. `lib/certification.lut`: `CostAlgebra C` with its six laws (6.S5), `Certificate C` (6.S6),
   `grade` with the correspondence of the old names (6.S7), `transport`, `compose`, `serves`;
   imported by the rest only through its theory, so `Certificate` is built only there (D5, L10.10).
2. *Fenced.* A first library of costs, a model of `CostAlgebra` with `⊕` the sum over [0, ∞]
   (spec 6.S5; the choice of model is the library's, D-2026-10-12-al); certified against the six
   laws.
3. *Fenced.* `lib/checks.lut`: `Failures E`, its projections and composition (5.S9 to 5.S11);
   the checker accepts a law into a check type through `verdict` (5.S3).
4. The host's `certify.py` records the bound and the evidence cost (6.S6) and keeps the chain of
   entries (6.S8); laws valued in `C` (5.S2); the `...Agrees` laws and `roundingSlack` return the
   measured cost (11.S18) and the range of the rounding law moves to the demand (11.S13).
5. The checker: a condition refines its variable inside its branch (4.R11, `refine` typable by
   it; replaces the textual discharge of today), with `r11_branch_refines.accept.lut` and
   `r11_other_predicate.reject.lut`; `check -v` reports consistent-not-characterized (4.S20).
6. Certify; milestone `v0.3` (D7).

## Phase 5. The demand and the memo

Realizes 8.S1 to 8.S11, 11.S3, 3.S29, O12.

1. The demand as a value (`lib/demand.lut`, 8.S2), built by `run`, `test`, `eval` and the session
   from their options; `--set` as the values of holes.
2. The plan as a value of `lib/plan.lut` (8.S4, 8.S11): the backward pass from a demand.
3. The result store keyed as 8.S8 says, by what the cone reads; a hit compared with the demand
   (8.S9); the session served from it (8.S13, once marked).
4. `lib/number_model.lut` (11.S3): the theory `NumberModel`, `float64` its first model, and
   `array.lut` generic over a hole `num : NumberModel`; this is what step 5 reinterprets.
5. The decorated type demanded (8.S1): one decoration, dual numbers, as a second model of
   `NumberModel`, demanded as `P T`; how the generic form is obtained for code not written over
   `NumberModel` is the question 8.S1 leaves open, to ask Luciano before this step.
6. `Term`, `Pattern`, `Act` and `Program` as `data` in core (3.S29), with `quote` and `eval`
   (3.S32) as the first use; `lib/term.lut` (3.S38) may wait.
7. Certify; milestone `v0.4`.

Chapters 9 (the planner) and 10 beyond the token (the library of the world) come after `v0.4`,
in a plan of their own.

## If the session that reads this has no memory of the chat

The specification in `docs/spec/` is the authority, chapter by chapter, with a status per item;
`record/spec-drafts.md` says how each chapter was written. The decisions behind it are in
`record/decisions.md`, the latest of 2026-10-13 (-a to -g).
Of the decided items of the specification not named in a phase, the planner (chapter 9) and the
library of the world (10.S13) wait for a plan of their own, and the rest are statements with
nothing to run. Luciano reads Spanish in chat; written
material is in English. He runs the scripts that process data and the certification of
sonolocalización; the model may run the lints, `luthier check` and `luthier certify` here.
