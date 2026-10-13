# check.py bite 3b: partial, written by the coordinator

The Opus agent on `prompt-3b.md` was stopped by Luciano at about 23:50 on 2026-10-13 before it
wrote its report. What it left in the tree, read from the diff by the coordinator (luthier-1b) at
03:25 on 2026-10-14 and committed as it was:

- Part 1 of the brief done: the two 4.R9 refusals of library.lth were the checker's. `base` now
  reads a theory head `T` (or `T a b`) as its record, as `elaborate.theory_domains` reads a domain,
  so `(l : Loader)` passes where `Loader` is expected; `arrows` reads `implies A B` in type
  position as the arrow `A -> B` (elaborate.py takes an arrow over a name brought in by an import
  for the Bool implication). A test each in `tests/test_check.py`. Suite: 443 passed, 7 xfailed.
- Part 2 (every leftover failure on the theory files named by cause) not done; its last words were
  that it was rerunning files to add "named in / read in" detail. Relaunched with check.py bite 4.

## Part 2

Written 2026-10-14 by an Opus agent (Claude Opus 5.5), relaunched with check.py bite 4. Runs of
`luthier check` on the 18 theory files of `src/luthier/lib/` at e2590af and `examples/hello.lut`,
one process per file, on the working tree at 5fa3d84, rerun after the two fixes below; term.lth
and term_model.lut changed since (681742e, b328aa4) and were rerun at 79f6f7e with the same
result. Details from a scratch script that recomputes each failing predicate and prints what it
compared (not kept in the repository).

Clean: checks.lth, ebnf.lth, ebnf_model.lut, library.lth, term.lth, test_model.lut,
translation.lth, world_model.lut, examples/hello.lut.

### Fixed in check.py (14 refusals, two causes, a test each)

- 4.R9, an `Int` where core's `Nat` or `Fin n` is expected (12 cases: term_model.lut
  `canonicalTerm`, `canonTerm ... nil 0`; grammar.lth `OpenForms`, `DefinitionTree`, `DefaultTree`,
  `LiteralTree`, `SubtypeTree`, `BlockOrRecordValue`, `ListTree`, `PatternTree`, `ScrutineeTree`,
  `NamedArgTree`, `NegationTree`, each through `numeral (n : Nat)`). Spec 11.R1 makes `Nat`
  `{ k : Int | 0 <= k }` and `Fin n` a subtype of `Int`, so the bases are `Int` and the refinement
  an obligation; `base` did not know them because core is not in the elaborated program. Now
  `CORE_SUBTYPE_BASES` in check.py, read only when the program does not define the name.
  Test `test_R9_core_Nat_and_Fin_are_subtypes_of_Int`. (A `Nat` argument to an `Int` parameter
  was refused too.)
- 4.R9, an applied subtype definition (grammar.lth `LexesWhatDerives` and
  `LexFailsWhatDerivesNot`, `tokenize d s` with `s : LexedText d g`, argument base `LexedText d g`,
  domain base `String`). `LexedText (d) (g) : U := { s : String | lexes d g s }`; `base` looked
  through a name defined as a subtype only when bare. Now it unfolds the application when the
  definition's body under its parameters is a subtype. Test
  `test_R9_applied_subtype_definition_is_looked_through`.

Both go beyond program.lth's `base` read literally (`Var x` defined as a subtype, nothing else),
as part 1's theory-head case did: program.lth's `base` wants the same two cases (an applied
definition; core's subtypes, which need core in the elaborated program).

### Left, by cause (18 failures)

1. **A chained projection `m.f.g` counts only `g` as read** (4.R3, theory fields). program.lth's
   `fieldsRead` takes `nameSuffix`, the part after the last `.`; the field of the model is the
   part after the first. check.py mirrors it. For program.lth.
   - world.lth `Persistence`: field `world`, read as `s.world.read` in WriteThenRead, WriteChangesOnlyItsPlace.
   - world.lth `Console`: field `world`, read as `c.world.read` in the console laws.
   - kernel_laws.lth `TheBooleans`: field `algebra`, read as `b.algebra.top`, `b.algebra.bottom`.
   - kernel_laws.lth `Lists`: field `free`, read as `l.free.neutral`, `l.free.combine`, `l.free.inject`.
2. **A `data` whose constructors no claimed law mentions** (4.R3, L2.7, D-2026-10-13-aa). The
   checker follows the spec; a constructor matched in a pattern is not a mention (`armsNames`),
   and a mention inside a helper the law calls is not one either (`lawNames` reads the law's
   body only). For the theories, unless program.lth should follow helpers or count patterns.
   - laws.lth `Coverage`: Exhaustive, Bounded, Listed, Drawn (Exhaustive only in a pattern of the
     helper `forallVerdict`; the others in test.lth's laws, another file).
   - laws.lth `Verdict`: Supported (in the helper `forallVerdict`, called by ForallOnPoints).
   - grammar.lth `Surface`: name (through the helper `nm` in every tree law).
   - test.lth `Mode`: ExhaustiveMode, SampledMode (no law reaches them; the comment names
     CoverageIsTheWeakest).
   - term_model.lut `HeadStep` (Done, Next), `PatternStep` (Hit, Miss, Blocked, Demand),
     `PatternListStep` (ListHit, ListMiss, ListBlocked, ListDemand), `ArmStep` (Selected,
     ScrutineeNext, NoArm): the model's internal step results, no law reaches them. By 4.R3 these
     are sums to be written as aliases.
3. **`Concrete` passed where `U` is expected** (4.R9). kernel_laws.lth declares `Concrete : U`
   (a type) and uses it as a universe of types (`(S : Concrete)`, then `S` as a type); nothing
   says `Concrete` refines `U`. For kernel_laws.lth or program.lth (how a sub-universe is said).
   - generators_model.lut `supportOf`: `List (T * Float64)`, argument base `Concrete`, domain base `U`.
   - world.lth `agreement`: `Described S A`, `A : Concrete`, argument base `Concrete`, domain base `U`.
4. **A name not in scope** (4.R2).
   - program.lth `TypeOfIntroductions`: `PWild`, read in its body; term.lth's constructor, missing
     from the import list at program.lth line 45. For the theory (one word).
   - kernel_models.lut `recordXY`: `one`, `two`, read in its body (`select`); labels of the sum
     `{ one : A || two : B }` inside kernel_laws.lth's `NamedProduct` declaration, which no import
     can name today. For program.lth (do an imported theory's sum labels come with it?) or the
     theory (name the sum and import it).
5. **An unused lambda parameter in a function definition** (4.R3). program.lth's
   `predicateUntouched` applies its lambda case to any definition whose body is a lambda; spec
   4.R3 speaks of predicates. generators.lth `walk`, `fn n s { ... }` of type `Gen (Maybe T)`:
   `n` untouched. The grammar has no `_` parameter for `fn`, so the author cannot opt out. For
   program.lth.
6. **A vacuous law** (4.R3). kernel_laws.lth `Initial`: field `absurd`, the only law `NoValue := false`
   reads nothing. The author's call (the comment says the law holds vacuously).

### Files added after e2590af, not checked here

algebra.lth, arrays.lth, arrays_model.lut, core.lut, numbers.lth (checked once at 79f6f7e: clean),
numbers_model.lut, tables.lth, tables_model.lut.

Check: `tests/test_check.py tests/test_spec.py` 104 passed, 7 xfailed; `tests` 450 passed,
7 xfailed.
