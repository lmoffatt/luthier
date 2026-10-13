# The checker's 18 leftovers on the theory files: report

Written 2026-10-14 by a Claude agent (Claude Opus 5.5) on the brief `prompt.md` in this folder;
saved verbatim by the coordinator (luthier-1b) from the agent's final message, since the harness
refused the agent's write of this file. Inputs: the tree at 9ff7115, check.py md5
f6b802a08768da00b352e64d90a5522d. The groups are those of `record/IA/check-2026-10-13/opus-3b.md`,
part 2. Each run is `PYTHONPATH=src python3 -m luthier.cli check FILE`, one process per file.
"Mirrored" means the scratch script, which patches check.py's 4.R3 with program.lth's new reading
of `fieldsRead`, `lawNames` and the lambda case and then runs the same `check`.

Of the 18 leftovers, 8 pass under today's check.py. 6 more pass once check.py copies the new
program.lth rules. 4 remain: laws.lth `Coverage`, world.lth `agreement`, generators_model.lut
`supportOf` and kernel_laws.lth `Initial`.

## Commits

| commit | file | groups |
| --- | --- | --- |
| 5f33db8 | src/luthier/lib/program.lth | 1, 2 [proposed], 4, 5 |
| 9e677cd | src/luthier/lib/laws.lth | 2 |
| 4c71da3 | src/luthier/lib/grammar.lth | 2 |
| 4940e6d | src/luthier/lib/term_model.lut | 2 |
| 2031c3a | src/luthier/lib/kernel_laws.lth | 3 [proposed], 4 |
| a1a91ef | src/luthier/lib/kernel_models.lut | 4 |

## Per group

**Group 1: a chained projection (4.R3, theory fields).**
- Change: in program.lth, `fieldsRead` now takes the field after the first `.`. So `s.world.read`
  reads the field `world` of `s`, computed as `namePrefix (nameRest s)`. `nameRest` replaces
  `nameSuffix`, and the unused `suffixes` was removed.
- check.py must: in `fields_read`, use `namePrefix(name.split('.', 1)[1])` instead of
  `nameSuffix(name)`.
- Mirrored: world.lth `Persistence` and `Console` pass, kernel_laws.lth `TheBooleans` and `Lists`
  pass, and so does algebra.lth `CompleteOrderedField`.

**Group 2: a `data` no claimed law mentions (4.R3, L2.7).** Decided case by case.
- term_model.lut `HeadStep`, `PatternStep`, `PatternListStep`, `ArmStep`: the model's internal
  step results, no law of role; now aliases of labeled sums, as 4.R3 and D-2026-10-13-aa say. A
  `Unit` alternative is injected by its label alone (3.S4), so no use site changed. The file
  checks clean and elaborates.
- laws.lth `Verdict`: `Supported` was reached only through the helper `forallVerdict`. By 4.S15 a
  law depends on the names in it "without unfolding definitions", so helpers stay unread. The
  helper inlined into `ForallOnPoints` and removed. `Verdict` now passes.
- grammar.lth `Surface`: `name` was reached only through the helper `nm`. `ProjectionTree` now
  writes `name "m.f"` (2.S14). Clean.
- test.lth `Mode`: both constructors appear in the laws' own bodies, but only as match patterns.
  `SampledMode` holds a `Metric`, a record of functions, so `Mode` has no `==` (4.R8): a law can
  only name it in a pattern. So program.lth's `lawNames` now also counts the constructors named
  by the patterns of a claimed law's own matches and clauses, marked [proposed]. Helpers stay
  unread, and an observer that only lists constructors is a helper (D-2026-10-13-p).
  check.py must: do the same in `law_names`. Mirrored: test.lth is clean.
- laws.lth `Coverage`: still refused. `Exhaustive` is now in the body of `ForallOnPoints`;
  `Bounded`, `Listed` and `Drawn` get their roles in test.lth's `GradesAsTerms`, another file.
  4.R3 asks for a role "in some theory", and D-2026-10-13-t puts core's roles in kernel_laws.lth,
  so the spec allows a role in another file, and the refusal comes from checking one file at a
  time (program.lth's rule covers one `SurfaceProgram`). Left; the comment names both places.

**Group 3: `Concrete` where `U` is expected (4.R9).**
- Spec: one universe, `U : U` (3.S8), no sub-universe. The reading that needs nothing new is a
  subtype of `U`, since 3.S6 makes the forgetting implicit.
- Change: kernel_laws.lth declares `hasStructuralEquality : U -> Bool` and defines `Concrete : U
  := { A : U | hasStructuralEquality A }`, marked [proposed]. No new refusal there.
- Still refused: world.lth `agreement` and generators_model.lut `supportOf`: check.py does not
  load imports, so in those files `Concrete` has no body.
- check.py must: read an imported name's definition (12.S22) when it computes `base`. program.lth
  has the same limit, since it also works on one program.

**Group 4: a name not in scope (4.R2).**
- program.lth: `PWild` added to the import from term.lth.
- kernel_laws.lth: the sum `select` returns is named, `Selected (A B : U) = { one : A || two : B }`;
  kernel_models.lut imports `Selected one two`, the way a `data`'s constructors are imported by
  name. The other option, an imported theory's sum labels coming with it, would let an import
  bring in names it does not list. Both files clean; check.py needs nothing.

**Group 5: an unused lambda parameter (4.R3).**
- Spec: 4.R3 is "A predicate defines only what it touches", so the lambda case applies to
  predicates only.
- Change: program.lth's `lambdaIsPredicate` decides when a lambda counts as a predicate: the
  type written on the definition ends in `Bool`, `Law` or `Failures E`; or no type is written and
  the name is declared at a non-function type (4.R6, the `Tagged` example); or no type is written
  and the name is declared at a type that ends in a verdict; or nothing is written or declared.
  Limit: a predicate type reached through an alias is not visible on the surface; check.py
  expands aliases first (4.R7), so it can see it.
- check.py must: apply the same test before its `s.Lambda` case in `violatesR3`.
- Mirrored: generators.lth (`walk`) is clean.

**Group 6: `Initial`'s vacuous law.** Left. `NoValue` is the claim itself and holds vacuously
(7.S12). A law that reads `i.absurd` would need a value of `T` to apply it to, or an equality of
functions, which is not structural (4.R8). The author's call.

## The seven files added after e2590af

Checked at 9ff7115. "Whose" is judged against program.lth as it now stands. None changed.
- numbers_model.lut, tables_model.lut: clean.
- algebra.lth: 4.R3 `CompleteOrderedField` (`c.ordered.leq`) is group 1 and passes once check.py
  mirrors it. 4.R3 `OrderedField` is the file's: its fields are read only through the helper
  `asOrderedRing`, and by 4.S15 helpers don't count; the fix is to inline the record in
  `FieldIsOrdered`.
- tables.lth: 4.R3 `Codec`: `eq` is read only through the helper `sameParse`, the file's. 4.R3
  `Table`: `nRows` is read only in a law's binder (`r : Fin t.nRows`) and in a helper; the binder
  part is program.lth's: `lawReadsIn` reads bodies only, while 1.S7 counts binders. 4.R9
  `sameParse` is the checker's: in `Maybe Table`, check.py takes the theory head's type to be its
  record, not `U`.
- arrays.lth, 4.R3 on `VecOf`, `MatOf`, `MatRows`, `Square`, `Symmetric`, `SymmetricOf`,
  `ClearDiagonal`: each predicate reads its variable only through a projection (`v.n == k`).
  program.lth's as well as check.py's: `untouched` asks `member "v"`, but `namesIn` gives `v.n`;
  by 1.S7 a projection `e.f` counts as touching `e`. The fix is to count `namePrefix` in
  `untouched`. Not made, outside the six groups.
- arrays.lth, 4.R9 on 45 definitions: all the checker's, and not the cause the slice report
  gives. Three causes: (a) most: an unannotated `fn k { ... }` passed where `Fin n -> T` is
  expected; the parameter's type is inferred as a hole, and `refines` compares the hole with `Fin
  n`. (b) A value of a subtype of `Vec Float64` or `Mat Float64` passed where the alias is
  expected: inside the subtype's base, the alias's `Fin n -> A` is elaborated as `implies (Fin n)
  A`; elsewhere it is a Pi. (c) `Orthogonal`: `identity k` is given the type `{ m, n, f : Fin m ->
  Fin k -> Float64 }`; substituting `n := k` captured the record's own dependent field `n`.
- arrays_model.lut and core.lut, 4.R13 on every `operator` target: program.lth's as well as
  check.py's. `rivalModel` compares `declaredSurface`, which is `nothing` whenever the type is
  written on the definition, so any two functions look alike. It should compare `typeOfAct`.
- core.lut, 4.R4 on `Int`, `Real`, `String`: program.lth's `makesAType` and check.py's R4 accept
  `extern` but not `primitive`, which 11.R1 prescribes for these types.
- core.lut, 4.R3 on `Unit`, `Bool`, `Maybe`, `List`: the one-file limit again. Their roles are in
  kernel_laws.lth's theories, through kernel_models.lut's models (for example `point := unit`).

## One question for Luciano

4.R3 asks for each constructor "a law stating its role in some theory", and in practice those
laws sit in other files: core's data in kernel_laws.lth and kernel_models.lut, laws.lth's
`Coverage` in test.lth. Should the rule be read over a library, meaning a file together with the
files that import it? And should a model that binds a constructor to a field, whose role a law
states, count as that law? If yes: program.lth needs a library-level 4.R3 and check.py needs to
load imports; that would also clear group 3's two leftovers. If no: the roles have to be restated
in the file that defines the data.

## Decisions taken on my own

- Group 2: patterns in a claimed law's own body count as naming constructors (program.lth,
  [proposed]). `forallVerdict` inlined into `ForallOnPoints` and removed. The four step types of
  term_model.lut turned into aliases of sums.
- Group 3: `Concrete` defined as a subtype of `U` with a declared predicate (kernel_laws.lth,
  [proposed]).
- Group 4: the sum named `Selected` and its labels imported, the brief's first option.
- Group 5: the surface test for "a lambda is a predicate".
- The new files and the 1.S7 projection fix in `untouched` were left unchanged.
