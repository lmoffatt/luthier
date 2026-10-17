# Bite 4b, the tester splits a conjunction of laws: report

2026-10-18, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-bite-4b.md` of this
folder (D-2026-10-18-f, D-2026-10-18-a; report-bite-2.md's question; report-budgets.md's question).
Started at 61f9523.

## Commits

- 3b18771 generators.lth §6, test.lth, tester.py: the region classifier's bounds are fields of
  `Budgets`, `regionNumbers` (4000) and `regionEntries` (400), positive like the counts, defaults in
  `defaultBudgets`, carried by `withFuel`; `Classifier.numbers` reads both from the line's budgets
  and `_MOST_ENTRIES` is gone. Its test, `tests/test_tester_conjunction.py`.
- 6f21bd5 tester.py, certify.py and three tests: the split (below).
- b46cb9b spec 7.S22 `[implemented]` (new, §12), 7.S8 names the two bounds.
- afa31b4 the stores after the wave.
- 717b212 execution.md's Status.
- this commit, the report.

## What was built

A law whose body is a `&` of partially applied laws, or unfolds to one through definitions applied
to all their parameters (`IntEquivalence r := BareEquivalence Int r`), is split by the tester
(`conjunction_parts`); a conjunct that is itself such a law is split in turn. `load_program` adds
one definition per conjunct, `L%conjunct<k>`, whose parameters are the law's and then the
variables the conjunct leaves missing, read from the type of the law at its head (`x : Int` of
`Reflexive Int r`, `p : Related Int r` of `Symmetric Int r`). It runs through `run_spec` unchanged,
so each missing variable is drawn by the generators of its type and bound by name or type as any
parameter (7.R1). The definitions are in no cone but their own: no other hash moved, and
`drawing_revision` is the same as at 61f9523 (checked), so no sampled line got a new fingerprint
from this bite.

A law line gives each conjunct its entry in the store of the law's claim: the law's name and the
hash of its cone, `conjunct` (part of the identity and of the pruning group) and `conjuncts` (the
list, not in the identity). Its outcome is refuted when a conjunct is; otherwise its grade is the
demand's combination of the conjuncts' grades (`certify.COMBINATION`, the weakest by default), and
none while one has none. `certify`'s `certificate_grade_and_empty` reads a conjunction's grade the
same way over the stores, none while a listed conjunct has no grade, and `refuse` serves a run's
demand of the law only when every conjunct is served (`served`). A control line passes when it
refutes one conjunct: the conjuncts run in order until one is refuted, and the line writes one
control entry, the law's, whose binding is every conjunct's and whose outcome names the conjunct
(`Symmetric Int r: r = leq, p = { x := -1, y := 1 }`). `luthier test` prints the conjunction's line
and one indented line per conjunct.

The elaborator did not need to change (elaborate.py untouched). Bite 2's `Equivalence` written bare
in a test program is split, graded and controlled (the tests below).

## The checks

- `tests/test_tester_conjunction.py`, 4 tests: the bare `Equivalence` at `Int` split into its three
  conjuncts with parameters (r, x), (r, p), (r, c), each with its entry, 300 cases, sampled; the same
  law on `<=` refuted at its `Symmetric` conjunct; its control refuting it, one entry; the
  certificate's grade the weakest of two conjuncts graded exhaustive and cases (cases; with
  `strongest`, exhaustive); stored, known on a second run, and no grade when a conjunct's entry is
  missing; the classifier's bounds read from a line's budgets (a 3 x 3 matrix written as a function
  gives 9 numbers at `regionEntries` 400 and none at 8; a list of 8 doubles gives 4 at
  `regionNumbers` 3).
- `python -m pytest -q tests` at b46cb9b, in the background: `6 failed, 833 passed, 6 skipped, 9
  xfailed in 1337.62s`. 833 is the brief's 829 plus my 4. The six failures are
  `tests/test_spec.py::test_spec_program_syntax` on `r13_structure_ambiguous.reject.lut`,
  `r13_structure_name.accept.lut` and four `r9_*.reject.lut`: untracked programs of the agent
  working in tests/spec and the elaborator (bite 4), which its work has not yet made pass. Nothing
  of this bite reads them.
- `python3 scripts/check_spec.py`: its known finding only, `docs/spec/03-kernel.md:190`; "187
  implemented, 79 decided (of which 33 suspended), 8 proposed" (7.S22 new).
- `luthier check src/luthier/lib/generators.lth src/luthier/lib/test.lth`: nothing, exit 0.
- `python3 scripts/core_metrics.py`: homonyms 96, executive names shadowing 112, list helpers 427,
  unclaimed 137, loose 1974 (real 1341, the rest 633), as before. The counts are in this report's
  commit message, not in 6f21bd5's (the last code commit): I did not rewrite history while another
  agent commits in the repository.

## The wave

`luthier certify tests/tester/*.test.lut --jobs 4`, at b46cb9b, 8 min 49 s, no `--deep`. Lines that
ran outside the fixtures, 44: certification_controls 7, certification_laws 8, cutoff_controls 1,
demand_controls 2, demand_laws 2, pooling_controls 2, pooling_laws 2, regions_controls 10,
regions_laws 10; every other program `0 lines ran`. They are the lines whose cone holds `Budgets`
(certification's `Entry`, demand.lth) or certification_model.lut's `hash`, an extern into
certify.py (`host_hash` of `python:luthier.certify`, which this bite changed). No law refuted,
every non-fixture law graded and controlled, every control refuted; the fixtures printed what they
are built to print (laws.test.lut: AndIsOr and Small refuted; cases.test.lut: Partial and
RootIsNotNegative not run), exit 1 for them alone. A second wave, 47 s: `0 lines ran` in every
non-fixture program. The fixtures' stores beside them were removed after each wave.
`tests/tester/core_instances.cert.json` (untracked, not mine) is byte-identical before and after.

## Findings

1. The elaborator types a bare conjunction's definition with a `Hole('type')` codomain: `infer`
   gives a `&` of two `Pi`s with different domains no type (elaborate.py, the `&` case). The split
   reads the law's lambdas, so it does not care; but bite 4's criterion "zero `Hole('type')` from
   `infer` on a definition's body" will meet every bare structure of bite 6. Bite 4 should give such
   a `&` the type of a conjunction of laws (a law over the shared parameters, 5.S6) or exempt it.
2. A binding by name binds every conjunct's variable of that name. `x : Bool` of one conjunct and
   `x : Int` of another are bound together, and the wrong one is then out of its type and the line
   not run. A binding by type keeps them apart; 7.S22 says so. Bite 6 will meet it where the
   structures' properties share `x`.
3. Within one line every conjunct is weakened alike by the line's bindings (test.lth's
   `specCoverage`), so the combination of grades rarely differs from each conjunct's there; it
   bites across bindings and in a demand. The test gives two conjuncts different grades by hand.
4. certification.lth's `Entry` states no `conjunct` field, and `identity` there does not read one;
   the stores now carry it. I left the theory alone (question).

## Decisions taken on my own (one commit undoes each)

- The names `regionNumbers` and `regionEntries`, positive in `positiveBudgets`.
- The conjuncts as definitions `L%conjunct<k>` added by `load_program` for every law a test line
  names, the split unfolding definitions applied to all their parameters, nested to any depth.
- A conjunct's entry under the conjunction's law name and cone, with `conjunct` in the identity and
  the pruning group and `conjuncts` beside, so that a missing conjunct leaves the law ungraded.
- A control of a conjunction writes one entry, the conjuncts run in order until one is refuted, its
  binding the union of theirs.
- A missing variable whose name clashes with the law's parameters gets a prime; `_` becomes `x`.
- The line's combination is `certify.COMBINATION`; a run's demand of the law is served only when
  every conjunct is (`served`).
- The output format of a conjunction's line and its conjuncts' lines.
- 7.S22, a new clause in §12, rather than a sentence in 7.S9.

## Question

Should certification.lth's `Entry` and `identity` state the `conjunct` field now, which changes
the cone of certification's laws and re-runs about fifteen lines once, or wait until bite 6 writes
the first structure bare?
