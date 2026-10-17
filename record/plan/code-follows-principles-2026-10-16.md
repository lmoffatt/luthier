# The code follows the principles: execution, 2026-10-16

Why (chat of 2026-10-16): L10.5 (a certificate serves every demand it meets) is settled and 6.S15 is
`[decided]`, yet the code matches the tolerance exactly. Not a lack of emphasis: D-2026-10-14-c
(Boolean first) postponed the cost part, the coordinator's brief told the theory's agent to leave it
as a hole, and the postponement was written only in a comment (certification.lth 267). The spec kept
saying `[decided]`; nothing lists what is decided and not implemented (114 clauses of the spec).

Rules adopted (coordinator's, each undone by one commit):
- A postponement is written in the clause it postpones (spec status, principles clause), not only in
  a comment of the code.
- Before reasoning a design question, search the principles record, the spec and the decisions.

Status: 2026-10-16, step 0 done (e6eb343, b27dae8, 805daff); step 1 done (b9705b0: 131 clauses, 60 implemented, 44 postponed, 27 pending); step 3a done (5f2b87d..812bc15; v0.4 criterion c met, verified by the coordinator); step 2 done (6c08c32..97ff0dd: check_spec counts 181 implemented, 81 decided of which 33 suspended, 8 proposed; 42 raised to implemented with evidence, 33 suspended, 11 postponements in text); step 3b running. For the next spec-touching bite: 12.S17's last sentence ("refuses only under --require-certified") and 10.S7's "until a world library exists nothing checks it" are stale.

## Step 0. His decisions of 2026-10-15/16 into the principles (agent, Sonnet)
D-2026-10-16-b: L2.8, L2.7's sentence, L13.5, L11.8, O1's note, L10.5 marked suspended in the Boolean
slice, L5.6's citation; P11's reading (item 22) as a sentence in L5.18. Brief:
`record/IA/code-follows-2026-10-16/prompt-principles.md`.
Accepted when: `scripts/project_principles.py --check` prints ok after `--write`; each clause cites
its decision; the record and the projection are committed apart.

## Step 1. The debt made visible (agent, Sonnet, read only but for its report)
Every `[decided]` and `[proposed]` clause of `docs/spec/` classified: implemented in fact (where),
postponed (by which decision, to when), or pending; the holes the theories mark (comments naming a
spec clause left as a hole). Brief: `record/IA/code-follows-2026-10-16/prompt-debt.md`.
Accepted when: every such clause has one class with its evidence (a file and line, or a decision id);
the report is committed.

## Step 2. The spec says what the code does
From step 1: the clauses implemented in fact get `[implemented]`; the postponed ones get their
postponement in the status (a format for `check_spec.py`, e.g. `[decided D-x; suspended by D-y]`);
`check_spec.py` prints the count of decided-not-implemented as information.
Accepted when: `check_spec.py` exits 0 and its information line gives the debt.

## Step 3. Code bites from the decisions of 2026-10-15/16 (agent, Opus, one at a time)
a. D-2026-10-15-d (item 1): each run records the hash of every store it read; the hole marked in
   certification.lth; only pure results served (v0.4's criterion c at its smallest).
b. D-2026-10-16-b (item 7): `certify` writes an entry only in the store of the claiming file; the
   copies beside test programs dropped.
c. D-2026-10-15-f, -g (items 3, 4): an agreeing replay absorbed, a disagreeing one kept and the law
   refused; a not-run for lack of fuel never memoized.
d. D-2026-10-15-h (item 5): `x.run.json` carries the hash of the whole key (seed included); the law
   relating record and key in demand.lth / plan.lth.
e. D-2026-10-15-e (item 2): the cone's hash erases binder annotations, with the law that erasure
   leaves the term's behavior unchanged; one re-certification wave; then the elaborator's fix at the
   source (a projection typed everywhere).
Each accepted when: the suite is green, the named law or test exists and a control refutes a wrong
version (L9.14), and the stores touched are committed with the code.

f. D-2026-10-16-c and -d (one agent, run.py and cli.py): a provisional extern refused by default in
   world.lth as in run, run as assumed only when the demand names it (`--accept assumed:NAME`), a
   warning on stderr per application, `provisional` with its reason, `check -v` lists them; the
   modes of running as fields of `Demand` with declared defaults: strategy (forward on demand the
   default, call by need the specimen under `TheDefaultsAgree`), fuel unbounded by default for run
   with an optional bound in steps or time, `fresh`. Brief: prompt-modes.md.
f'. 3f landed (cc883f1..749e0e4; 755 passed). The coordinator's choices: the 90 s past-the-bound
   test behind LUTHIER_SLOW with a cheap one in its place (asked of the same agent); 6.S14's sentence
   given to the 3i agent, which holds chapter 6.
g. D-2026-10-16-e (after f; renames many files): executive files `.run.lut` and `.test.lut`; the
   checker's refusals; run and certify take only their kind; the migration of tests/tester and the
   two mixed sonolocalización files. Principles text (L2.6, L5.1) by a separate agent, launched.
Order: 3b's follow-up (done, 741 passed, verified), then f and 3c together (launched), then g, then 3e.

h. D-2026-10-16-h: tables.py returns the host's `Just` or nothing at a `Maybe` (item 14), the
   table cones re-certified; no cutoff accepts a failure, running past one names it
   (`--accept assumed:LAW`, item 16); records of `.run.lut` under examples/ tracked, under tests/
   ignored (item 8, after g).
c'. 3c landed (af07d24..3a364a2). Its question answered by the coordinator (one commit undoes it):
   a failure in a disagreement keeps refusing until resolved by hand with its reason recorded (P2),
   two later passes do not erase a counterexample (D-2026-10-15-f); a resolving command later.
   `luthier certify` of certification_laws.lut and certification_controls.lut waits for 3f.
i. D-2026-10-16-g: (launched after 3c) a law's samples pooled across seeds, each stretch keeping its seed; a statistical
   law continues one sequential test (certify.py, tester.py; after 3c).
i'. 3i landed (edaeb6f..5c58dad; budget bounds the whole test, ec3574c; 759 passed). The store and
   pooling laws certified by the coordinator (4c0549e); three store laws uncontrolled
   (ANewIdentityGoesInFront, AnAgreeingReplayAddsNothing, AnAgreeingPairSettles): a control each is
   debt under L9.14, a small bite after 3g. Gap left by 3i: certification.lth's `Entry` does not name
   its cutoffs parameter (marked at `pooledCases`). 3g launched, alone in the repository.
j. D-2026-10-16-i: evidence kept per binding and per labelled region with its n and bound; the
   demand combines grades, weakest by default (5.S8); special values and atoms in the generators,
   `classify`/`cover` (7.S14); certification.lth's grade rules rewritten (a theory: Fable); a
   principles clause on null sets [proposed], its sentence written by the coordinator in the brief.
   Refined by D-2026-10-16-j: the regions that enter a grade come only from three finite sources,
   the type (its theory declares its degenerate cases once), the law (each cutoff's two sides, each
   premise's boundary) and the code (each branch of the cone: branch coverage); an author's label is
   informative and enters no grade.
v0.4: D-2026-10-16-f, tag when (c) is met with (e) as debt. (c) verified by the coordinator at
1922758 (741 passed); 3470c54 adds only record files. The tag is his.

g'. 3g landed (6c9be06..bf25747; 781 passed, verified by the coordinator). Its question answered by
   the coordinator (P2, one commit undoes it): a run cut by its time limit or fuel is recorded as a
   run that did not finish (its demand, the step reached, the reason), never served; in 3h.
Queue after 3g:
- 3h (Opus): D-2026-10-16-h (tables `Just`, table cones re-certified, `CellsOfTheirKind` refuted at
  baseline to be read in that light; no cutoff accepts a failure, `--accept assumed:LAW`; records of
  `.run.lut` under examples/ tracked, under tests/ ignored) and the cut run recorded. Brief:
  prompt-tables-cut.md.
- controls (Sonnet): a control for each of the three uncontrolled store laws and the others `certify`
  lists uncontrolled. Brief: prompt-controls.md.
- controls landed (b55445f, 10d09e8): three store laws controlled. Findings under L9.14:
  plan.lth's `KeyReadsOnlyTheCone` and `KeyReadsTheType` follow from `demandKey`'s definition for
  every planner, so no model fails them; restate them so the planner enters, or drop them (a theory
  bite, with 3j).
- 3h landed (227065a..c1ca37d; 798 passed). The coordinator's answer: CellsOfTheirKind's 2026-10-14
  failure, written by a control line misfiled among the laws, moved to the archive with its reason
  (P3), not deleted. examples/ run records tracked. Findings for later: tester.py's `_list_members`
  fingerprints only a census's named members, not those built by an expression (`parsed ...`), so a
  change to tables.py left three lines known (replayed with --deep, they agree); its fix restales
  fingerprints, so it goes with 3e's re-certification wave. A pure run past an assumed law is served
  from the result store (`assumes` not in the key; certification is read before serving, so the
  warning stays).
- 3j: j1 the theory (Fable, record/IA/regions-2026-10-17/prompt-theory.md, launched 2026-10-17) with
  plan.lth's two laws; L9.16 by Sonnet (prompt-principle.md); j2 the code after j1 (Fable for the theory, after the controls): regions from the type, the law and the code.
- j1 landed (1b4ea60..a1c994b; 799 passed): degeneracies in generators.lth and arrays.lth, regions
  in certification.lth (`Regioning`, `Deriving`), plan.lth's KeyReadsOnlyTheCone restated and
  controlled, KeyReadsTheType removed. Its question answered by the coordinator ([proposed], one
  commit undoes it): an empty region caps a binding at Sampled (L9.16), a stricter demand chooses
  another combination. L9.16 landed (dd69450, bdc88d3). j2a launched (prompt-code.md: items 1-4,
  6, 7, 9, 10 of report-theory.md section 5); j2b later (branch coverage, `cover`). The suite wrote
  examples/hello.run.json, now tracked: a Sonnet bite makes the suite write no tracked file.
- 3e: the hash erases binder annotations; one re-certification wave.
- print and stdout (after his item 12): a failed write is recorded as a success today (the
  decision-assistant fork's finding of 2026-10-16: `print` appends to a Python buffer, `observe`
  reads the same buffer, the real write happens at exit outside W, so `HostAgreesPrint` is
  tautological). Direction: write at once, check what the OS accepted, fail the action otherwise;
  stdout observed according to what fd 1 is.

Priority from 2026-10-17 (D-2026-10-17-i, his words "Primero tenemos que rehacer todo el core"):
the core first. Its design is launched beside j2a (record/plan/core-2026-10-17/prompt-design.md,
Fable); its bites run before the rest of the queue below, which joins only where files are
disjoint. Slice work waits: item 34 (session A with and without A2, both kept, compared on the
corrected graph he regenerates with src/prepare_experiment_zero.py) after the core; 35 to 37 wait.

Documentation (luthier-8c's review of 2026-10-17): the spec clauses each bite touches are its own;
three principles clauses written now (L3: equivalences between types as named values; L8: the
subtype by a law as an equalizer; L11: roots of trust), brief prompt-principles-three.md in
record/plan/core-2026-10-17/; docs/guide, README, principles-for-readers.md and rationale in one
pass after the core, so they are not rewritten twice.

Queue added 2026-10-17 (decisions D-2026-10-16-k to -n and D-2026-10-17-a to -d, relayed by the
decision-assistant fork, now luthier-8c), in this order after j2a:
- print and stdout, now decided (D-2026-10-16-n, item 12): `print` writes at once and checks what
  `write()` returns, failing the action when the system rejects bytes; a file checked by re-reading
  it; stdout observed according to what it is connected to (file re-read, pipe with an own tee,
  terminal the bytes accepted); the roots of trust declared once per project and listed in every
  run's record. Later: each place's kind of feedback grades its actions.
- convergence and vacuity (D-2026-10-16-m): a law whose cases are all vacuous is not run, its premise
  count the reason; `MaximizerStationary`'s `else true` and `QuadraticConverges`'s
  `if s.maxIter < budget then true` go; convergence as a domain plus a step bound derived from the
  theory (Newton 1, LM a handful, gradient about kappa log(1/tol)), never a constant; a `Reason` why
  an algorithm stopped; the step count recorded.
- the rest of D-2026-10-16-k and -l: a host action validated once per hash of the model's cone, its
  arguments kept as evidence (item 9); `Bounded n` a domain, exhaustive on its box `Exhaustive`,
  `ForallOnPoints` following (item 17); per-law cutoffs a typed field of `Demand` (item 20); the most
  specific binding wins (G6); a law quantified over `U` a static error, `Settling`'s laws on concrete
  instances (L5); 3.R1 and 3.R2 reworded (D-2026-10-17-a).
- D-2026-10-17-h: the checker refuses a refutable pattern on `<-` (item 27); the agents' [proposed]
  readings ratified in bulk for their meaning, their markers removed (item 28), except: a theory file
  importing a model by name (L2.6); the fit's items 5 and 9 (D-2026-10-16-b); demand/plan items 5,
  7, 9, 10; all of plot.lth (waits for G1 to G5); 4.S13's borrowed [decided D-2026-10-12-z] becomes
  [proposed] (P1). A Sonnet bite after j2a lands (it touches theory comments and spec statuses), from
  item 28's list in record/plan/decisions-pending-2026-10-15.md.
- 3e (hash erases binder annotations; census fingerprint fix; one re-certification wave).
- The typing bite (item 39, recommended after the next tag; the tag now follows the core): after the
  core, before the tag. Bite 2 of the core found `luthier check` passes a predicate typed wrong, a
  missing field and `x + "a"` (check.py runs program.lth's predicates, it is no type checker); until
  then the core's signatures are verified by its test programs (instances and controls), and
  "check clean" in an acceptance criterion means only that.
- No version tag until after the core's step (D-2026-10-17-e): the names change at large with it.
- The core (D-2026-10-17-b, -c, -d), before more theories, then the tag (D-2026-10-17-e); 3e's
  hash change goes in its first bite so the library is re-certified once: the
  algebraic properties as generic laws over an operation and its equality, adjectives without "is";
  properties.lth and structures.lth replace kernel_laws.lth, in five groups (relations, operations,
  functions, containers, the structure of types); the equality of functions derived pointwise from
  the codomain's, with the combinators (id, compose, flip, zipWith, map) and the few non-equational
  properties (order, injective/cancellative, LandsIn); a generic list library in the core replacing
  about 110 per-type helpers. Survey findings to fold in: 25 names defined in more than one file;
  models re-exporting their fields as top-level names; 38 unclaimed Bool laws; `check`'s "loose"
  notice firing 1675 times; the 11 theories of Luthier itself without tests or stores. Plan: a
  design brief for Fable (the two files and the migration map), then mechanical migration by Opus in
  bites by group, each re-certifying what it touches.
  Extended by D-2026-10-17-f (Metric in the core beside Object: d over the type's equality, M1 to
  M3, variants by their exact names; KL, relative error and squared Euclidean as controls; a Float64
  realization a separate claim within a bound of an exact metric; every equational property with a
  within-bound version, Doubles associative within gamma_2(|x|+|y|+|z|); the approx families as a
  ball of a named metric) and D-2026-10-17-g (universal constructions with their universal
  properties, by priority: equalizer, pullback, pushforward in probability.lth, coequalizer,
  pushout; product, coproduct, free). Layout proposed by the fork: lib/core/ with core.lut,
  lists.lut, properties/{relations, operations, functions}.lth, structures/{equality, order,
  algebraic, containers, universal}.lth; to confirm in the design brief.

## Step 4. The first cost (v0.5)
`PinvProjects` returns its distance; the certificate records it; a demand is served by
`distance <= tolerance` (L10.5, 6.S15 for that law); the pattern written for the other laws.
Accepted when: one certificate serves demands at 1e-6 and 1e-8 without re-testing, and refuses one
below the recorded distance.

Waiting on him: item 41 (a law's evidence pooled across seeds) and the rest of the pending list.
