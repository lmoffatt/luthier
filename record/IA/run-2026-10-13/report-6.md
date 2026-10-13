# run.py bite 6: the loader scopes imports by name, an extern's arity from its type (report)

2026-10-14, Claude Opus 5.5, an agent of luthier-1b, on prompt-6.md; saved by the coordinator.
Files: `src/luthier/run.py`, `src/luthier/tester.py`, `tests/test_run.py`, `tests/test_tester.py`,
new `tests/run/extern_arity.lut`, `tests/run/scope/{left,right,main,unlisted,missing_import}.lut`.
Checks: test_run and test_tester 55 passed, 2 skipped; hello prints; validate_graph.lut at the
default fuel prints its line; `luthier test tests/tester/numbers_laws.lut` under LUTHIER_SLOW=1
(2 min): nothing refuted, nothing unsettled, the four log laws settle (`LogOfOne` cases;
`ExpOfLog`, `LogOfExp`, `LogMultiplies` sampled); `LeqAntisymmetric` still not run (7.S6).

## What changed

1. The loader (`run.Loaded`, replacing `load` and `_core_acts`): reads core and the file's import
   graph; each act's defined names and free references are renamed by scope: the file's own
   definition first, then what its imports list (each under its alias), then core. Binders
   followed as check.py's `names` does; a pattern name is a constructor when it resolves to one.
   An unresolved reference is an error naming the file (`unlisted.lut: helper is neither defined
   there, nor imported, nor core's`); so is an import listing a name its file does not define.
   Both raised only when the runtime slice keeps the act (`Loaded.demand`, 12.S21). `run_file`
   and the tester load through it. No library depended on flattening; the one unresolved import
   was `one two` in kernel_models.lut (labels of `Selected`), now allowed (choice 4).
2. tester.py: `Scope`, `_bound`, `_defines` gone; `load_program` uses `Loaded`; the constructors
   of `grade`, `Verdict`, `Coverage` resolved in test.lth then laws.lth; output without `@file`.
3. Arity: `TypedExtern` carries `arity` from the declared type; `inspect.signature` only when no
   type is declared; a builtin without a signature is unary.
4. Tests: the two-library fixture (`3 10 false true`, left.lut's own `not` shadowing core's only
   inside left.lut); both error messages; the seven clashes (`LeqPair`, `LeqChain`, `LeqBoth`,
   `PlusCommutes`, `NonNegative`, `Exhaustive`, `Assumed`); test.lth's `Exhaustive` is laws.lth's
   constructor while generators.lth's is its theory; `grade` gives test.lth's `Assumed`; the
   arity fixture (`math.log` typed and untyped, `math.pi`); the slow test asserts no unsettled
   line and no `@`.

## Choices of the agent (each undone by reverting this bite)

1. A name keeps its plain program name when one file defines it; on a clash the file being run
   wins, then core; the others become `name@stem` (`~k` if two files share a stem).
2. An unresolved reference or a bad import entry is an error only when a demand reaches it.
3. Re-export: an import of a name the target file itself imports resolves through the chain.
4. Sum labels stay global, as the elaborator reads them, and an import may list one.
5. A name a file both defines and imports means its own definition, no warning (generators.lth's
   `Exhaustive`).
6. Arity: a definition `f (x..) : B := extern "r" x..` has as many arguments as binders; a bare
   extern counts the arrows of its declared type up to the first arrow whose domain is `Fin`
   (3.S23); a declared arity of 0 gives the host's value (`math.pi`); host objects that crossed
   back keep their Python signature.
7. Free without definition: `extern`, `primitive`, `axiom`, `quote`, the elaborator's built-in
   constructors, `kernel.BOOTSTRAP_PRIMITIVES`.

## Findings for others

- generators.lth imports `Exhaustive` from laws.lth and defines a theory `Exhaustive`: under
  12.S22 the import is dead; whether a name both imported and defined is an error is for
  library.lth's author.
- check.py's `load_imports` docstring says "as run.py's loader reads them": no longer true.
- `LeqAntisymmetric` still has zero acceptance (numbers.lth's).
