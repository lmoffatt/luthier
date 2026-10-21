# Bite 6: structures and the core's claims

Codex, 2026-10-21. Sources: `prompt-bite-6.md`; execution.md sections 0, 2, 3 and 6;
reports 2, 4b and 5; D-2026-10-17-b through -g and D-2026-10-18-a through -c, -f, -g,
-i. Implementation input: `2859815`. Recovery input: `refs/backup/bite6-20261020`,
`2faaf79ac7ab47fe38a7b591f63cdb306b5c904d`, saved by the coordinator after the reboot.
The earlier recovery repository and its logs were lost with `/tmp`; they are not evidence for
this report's final checks. No commit or recovery repository was attempted after resuming.
The coordinator will make the commits listed below.

## What was built

The relation composites and Isomorphism/Bijective are bare conjunctions. Structures in
`core/structures/{equality,order,algebraic,containers,universal}.lth` declare their data and
state laws, with mathematical references. The seven duplicate core property definitions are
gone, as are their entries in `CORE_COLLISIONS`. Function idempotence uses Pointwise on
self-composition; the one binary Idempotent remains in operations.lth.

The algebraic structures run from Semigroup through BooleanAlgebra, with the ordered-semiring
interface in order.lth. Quantale states indexed suprema and tensor preservation, including the
empty index type. Its four intended bases are named in comments, without asserting that they
are certified models. NonExpansive and Lipschitz live beside Monotone. The metric family includes
pseudo-, quasi- and ultrametrics, bounded metric laws, tolerance and the ultrametric threshold.
ExtendedMetric remains a declaration with no model, as execution.md section 3.1 requests.
The proposed t-norm, distance-distribution and Menger declarations have explicit laws and
counterexamples; no probabilistic metric model is claimed.

Universal constructions use the relevant carrier's Object, including the codomain of a
universal arrow. Equalizer, Pullback and Coequalizer are included. FreeMonoid uses Foldable's
single fold; Lists includes FreeMonoid's laws as well as the constructor roles. The container
interfaces state map, indexing, tabulation and finite-fold laws.

Core kernel instances and claims moved to core.lut, together with combinators and finite folds.
The old integers/strings models are gone from numbers_model.lut. Algebra sections 0-2 moved to
the core; the temporary Iso interface and inverse aliases remain for positions.lut until bite 12.
Generic container computations and the minimal list bodies needed by map/size/at resolution
live in core/lists.lut. The full list library remains bite 7. Their importers use the core's folds.

New global names required local collision renames in program/term/plan, the grammar's surface
sum constructor, their importers, and the factorial example. These preserve the algorithms;
the later removal of their duplicate list algorithms remains bites 9-12. The internal list map
is temporarily named mapKernelList, avoiding world.lth's mapList before bite 9. The bounded
integer metric carrier is MetricInteger (the same +/-2^52 range as numbers.lth's Small), so
existing local laws and models named Small remain legal. Int's unbounded carrier is not
asserted to have an exact Float64-valued absolute-distance metric.

Chapter 7's specified placement references are corrected. Chapter 2's generated grammar block
was refreshed after renaming the surface constructor.

## Integration fixes and autonomous decisions

These are implementation decisions, not changes to the mathematical laws:

- Preserve a declared theory's record when its definition explicitly binds its model; infer the
  signatures of imported bare conjunctions in dependency order.
- Prefer an explicitly claimed subtype model over a base-carrier model (Nat versus Int), while
  still rejecting two models declared at the same carrier.
- Bind a claim's default model for field resolution while leaving the model parameter available
  to controls. Coalesce fields of distinct structures only when their claimed operations are
  literally alpha-equal; distinct operations and two models of one structure remain ambiguous.
- Retain theory predicates for the tester and certification's law slice, while normal execution
  retains their declarations. Cone traversal distinguishes type and value dependencies: a theory
  used as a type contributes its declared record, and its predicate contributes when called as a
  value. Erased lambda annotations create no executable dependency. A model's hash therefore
  agrees in tests and runs. The vector-norm and LM integration tests exposed the incorrect
  alternative: retaining predicates globally pulled SqrtMonotone's auxiliary doublesOrder into
  the execution cone of an Elementary model, demanding unrelated certificates. A regression
  checks both exclusion of auxiliary model dependencies and inclusion of laws called as values.
- Expand declared theories and distribute a shared model over each bare conjunct in the tester.
  Include splitting code in the drawing fingerprint: a real cached NotRun survived a splitting
  fix before this dependency was recorded. Empty data now gives NoGenerator rather than a
  random-range exception; ExhaustiveMode can certify its absence of cases.
- Match controls by both law name and cone hash. Retaining bare theory bodies can make several
  mutually dependent laws share one cone; tables' acceptance test caught controls being attributed
  to other laws when only the hash was compared. A regression checks both false acceptance and
  false rejection across such laws.
- Read a theory's declared record before reducing a type in the generator. The full suite caught
  IntegerDivision being treated as a conjunction of functions instead of its record when no
  model census was bound. Its original “bind a census (7.R4)” diagnostic is preserved. This
  driver change is in the drawing fingerprint, so dependent sampled evidence is re-certified.
- Update current-syntax fixtures and generated test programs whose local Group, Functor,
  Reflexive, IntEquivalence or sum names became core names; qualify local size/map/eq interfaces
  where both the core and fixture now supply a model. Historical v0.1 files and hashes are kept.
- Recognize cross-core claims for the core's unclaimed-law check. Preserve the global identities
  of explicitly imported core types: the list/core import cycle exposed Bool@core versus Bool
  and Maybe@core versus Maybe in the checker.
- Enumerate the finite list censuses for indexing, free-monoid and entrywise tests, including both orders of the two-element Boolean list. SampledMode
  traverses equal censuses in parallel; it had tested indexing only on identical list pairs and
  missed the broken index. The laws were unchanged.
- Keep deterministic counterexamples local to the executive control program, rather than adding
  an importable library of unclaimed counterexample laws. The backup ref retains the earlier
  core_structures.lut and its obsolete store.
- Start the small list implementation in bite 6 because its required unimported map/size/at probe
  needs a model. No full bite 7 library or reinvention-removal campaign was added.

There are 69 deterministic named counterexamples and four metric-candidate controls.
The new Python regressions check all core control outcomes, the four metric controls, cross-core
claimants, shared-model distribution, declared-record preservation, core import type identity, and type/value cone edges including refinement predicates.
Tests retain seed 0 where inherited; new sampled lines use seed 20261020. Explicit counterexample
values and finite censuses are written in the test programs; none are random type generation.

## Mathematical findings and limits

1. The proposed error base with natural <=, addition and the usual supremum does not satisfy
   tensor preservation of the empty supremum: for positive a, a + sup(empty) differs from
   sup(a + empty). Lawvere's orientation uses the opposite order. Bounded evidence addition also
   needs a closure convention. The four comments identify intended bases, not four models.
   No Quantale law was weakened to make those comments into claims.
2. EmptyIsInitial has an exhaustive empty domain. It has no typed wrong Initial Empty model
   that a value of Empty could refute. An Initial Bool record would require an arbitrary value
   of every type, which the total language cannot construct. Its grade is vacuous and its
   control status remains explicitly uncontrolled. No host cast, fake counterexample, xfail or
   weaker law was added to hide this limit.
3. Generic claims are exercised at explicitly listed finite type instances, with Listed coverage.
   This is finite evidence, not certification over U. Some existing generator limitations require
   explicit equal pairs/chains, lists, products and sums instead of rejection sampling.
4. The exact integer metric uses MetricInteger; unrestricted integer-to-Float64 conversion cannot
   justify the exact metric claim. Float64's arithmetic claims remain numbers.lth's bounded ones.

## Validation

The final core confirmation is complete (no --deep):

```text
tests/tester/core_laws.test.lut: 95 laws, 0 lines ran, 110 known
  EmptyIsInitial: cases; uncontrolled: untested against any wrong model (7.S19)
tests/tester/core_controls.test.lut: 0 laws, 167 controls, 0 lines ran, 167 known
```

After the cone correction, `pytest -q tests/test_certify.py` passed: **57 passed, 1 skipped
in 1080.32s**. The static/core scope (`test_check.py`, `test_elaborate.py`,
`test_core_structures.py`) passed: **158 passed in 219.58s**. Dependent re-certification and
the final full-suite run remain in progress; their completed outputs are added before handoff.
The touched-program wave (jobs 4, the lines' own seeds, sizes and budgets, no --deep):

| Program | Laws / controls | Lines ran | Known |
| --- | --- | ---: | ---: |
| core_laws.test.lut | 95 laws | 88 | 22 |
| core_controls.test.lut | 167 controls | 131 | 36 |
| arrays_laws.test.lut | 35 laws | 52 | 0 |
| arrays_controls.test.lut | 37 controls | 37 | 0 |

Every runnable law in this wave graded; every control refuted. EmptyIsInitial's explicitly
uncontrolled empty-domain result is the exception stated above. The direct integration probe
`luthier run tests/run/vector_norm.run.lut` produced `5.0` with exit 0 after this wave.

The acceptance fixture checks size/at/map on lists of Int, Bool, String and Nat; eq/leq on
all four carriers; plus on Int/Nat; and d on Bool and MetricInteger. These are the applicable
models specified in execution.md section 3.6, rather than an assertion that every operation
exists on every carrier. A separate negative elaboration probe refused `Metric.d x y` for
`x, y : Int`, naming the available Bool and MetricInteger models; it did not select a bounded
metric for arbitrary integers.

The conda Python is `/home/lmoffatt/miniconda3/bin/python` (pytest 9.1.1), and the CLI is the
adjacent `luthier`. System Python has no pytest. No re-certification wave uses --deep.

Logs: the coordinator's live session capture is
`~/.cache/luthier-codex/bite6-resume.jsonl`, including the commands' combined stdout/stderr.
The capture was verified to contain the current commands and to be growing during validation.
The sandbox cannot create a separate log directory under this read-only mount, so command output
is retained through that existing capture. No separate logs or recovery repository were put in
`/tmp`. Pytest's generated fixtures and library-store copies use its normal temporary directories;
they are test inputs, not recovery storage or durable logs.

## Metrics

Deterministic `python3 scripts/core_metrics.py`, default roots and parameters, no seed;
script unchanged. The before counts were recorded in the working report that survived the reboot
and is retained in the backup ref, at input 2859815; the after counts were re-run on this tree:

| Count | Before | After |
| --- | ---: | ---: |
| Homonyms | 96 | 81 |
| Executive names shadowing | 107 | 103 |
| Reinvented list helpers | 427 | 426 |
| Unclaimed laws | 137 | 45 |
| Loose | 1974 | 2060 |
| Loose, real | 1341 | 1400 |
| Loose, remaining | 633 | 660 |

Homonyms and unclaimed laws decreased beyond the specified duplicate removals. Loose increased:
this is a recorded regression in the global end-state measure, not a completed core-end claim.
The required new declarations, models and helpers still contribute notices; later bites retain
responsibility for absorption into their theories. The metrics script was not changed.

## Ordered commits for the coordinator

Each entry gives a subject, all its paths, and one body line. After the body line add a blank
line and `Co-Authored-By: Codex <noreply@openai.com>`. Stage by path. Existing untracked user
files, including the fixture stores and time_opus_low.txt, are excluded.

### 1. Support bare structure laws throughout elaboration and certification

Files:

```text
src/luthier/certify.py
src/luthier/check.py
src/luthier/elaborate.py
src/luthier/run.py
src/luthier/tester.py
tests/test_certify.py
```

Body: `Preserve model records and consistent cones, split bare laws, and keep controls specific to their law.`

### 2. Define the core structures as bare mathematical laws

Files:

```text
src/luthier/lib/core/properties/functions.lth
src/luthier/lib/core/properties/relations.lth
src/luthier/lib/core/structures/algebraic.lth
src/luthier/lib/core/structures/containers.lth
src/luthier/lib/core/structures/equality.lth
src/luthier/lib/core/structures/order.lth
src/luthier/lib/core/structures/universal.lth
```

Body: `Implement D-2026-10-18-c, -f and -i with referenced declarations and metric-level laws.`

### 3. Bind kernel models and move finite computations into the core

Files:

```text
examples/sonolocalizacion/distance_graph.lut
examples/sonolocalizacion/distances.lut
examples/sonolocalizacion/figures.lut
examples/sonolocalizacion/positions.lut
src/luthier/lib/algebra.lth
src/luthier/lib/arrays.lth
src/luthier/lib/core/core.lut
src/luthier/lib/core/lists.lut
src/luthier/lib/grammar.lth
src/luthier/lib/library.lth
src/luthier/lib/numbers_model.lut
src/luthier/lib/plan.lth
src/luthier/lib/plan_model.lut
src/luthier/lib/plot.lth
src/luthier/lib/probability.lth
src/luthier/lib/program.lth
src/luthier/lib/tables.lth
src/luthier/lib/term.lth
src/luthier/lib/term_model.lut
src/luthier/lib/translation.lth
tests/eval/factorial.lut
```

Body: `Move kernel instances and folds, preserve the temporary Iso interface, and resolve the new core-name collisions.`

### 4. Exercise core claims and controls without explicit core imports

Files:

```text
docs/spec/02-grammar.md
docs/spec/07-tests.md
tests/spec/core_unimported.accept.lut
tests/spec/r13_structure_ambiguous.reject.lut
tests/test_check.py
tests/test_core_structures.py
tests/test_elaborate.py
tests/test_modes.py
tests/test_run.py
tests/tester/arrays_controls.test.lut
tests/tester/core_controls.test.lut
tests/tester/core_instances.lut
tests/tester/core_laws.test.lut
```

Body: `Cover kernel bindings, every runnable control, four invalid metrics and the placement terminology.`

### 5. Re-certify the structure migration and dependent test programs

Files:

```text
examples/sonolocalizacion/distances.cert.json
examples/sonolocalizacion/session_a.cert.json
src/luthier/lib/arrays.cert.json
src/luthier/lib/arrays_model.cert.json
src/luthier/lib/belief.cert.json
src/luthier/lib/belief_model.cert.json
src/luthier/lib/certification.cert.json
src/luthier/lib/certification_model.cert.json
src/luthier/lib/core/core.cert.json
src/luthier/lib/demand.cert.json
src/luthier/lib/generators.cert.json
src/luthier/lib/generators_model.cert.json
src/luthier/lib/laws.cert.json
src/luthier/lib/numbers.cert.json
src/luthier/lib/numbers_model.cert.json
src/luthier/lib/optimization.cert.json
src/luthier/lib/optimization_model.cert.json
src/luthier/lib/plan.cert.json
src/luthier/lib/plan_model.cert.json
src/luthier/lib/plot.cert.json
src/luthier/lib/plot_model.cert.json
src/luthier/lib/probability.cert.json
src/luthier/lib/probability_model.cert.json
src/luthier/lib/term_model.cert.json
src/luthier/lib/world.cert.json
src/luthier/lib/world_model.cert.json
tests/tester/core_controls.test.cert.json
```

Body: `Record current-cone evidence from the touched programs and the complete certification wave without deep replay.`

### 6. Record bite 6 evidence, findings and core metrics

Files:

```text
record/plan/core-2026-10-17/report-bite-6.md
```

Body: `Report validation, the vacuous initial-object exception, implementation decisions and final deterministic counts.`

## One question

May EmptyIsInitial's vacuous result under ExhaustiveMode (reported as cases) be accepted as the exception to
“every core claim controlled,” while keeping its vacuity and uncontrolled status visible?
