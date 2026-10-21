# Bite 10: Luthier's self-description over the core

Claude Sonnet 5.5, 2026-10-21, on `prompt-bite-10.md`. Input: `24b63e9`. Commits: `9e2857d` (ebnf,
ebnf_model, grammar), `010d17c` (term, term_model), `4e36e5f` (the two renames and run.py's
collisions), `c58ec5c` (program, library), and this report's.

## What changed

Files: ebnf.lth, ebnf_model.lut, grammar.lth, term.lth, term_model.lut, program.lth, library.lth,
translation.lth (rename only). The local `append`, `memberString`, `termMember`, `programMember`,
`concatNames`, `concatTermNames`, `concatTerms`, `appendApps`, `appendTerms`, `appendText`, `appendEnv`,
`appendBindings`, `lookupField`, `lookupContext`, the `all...` and `any...` families, `nonEmpty`,
`atLeastTwo`, `ebnfEmpty`, `countProductions`, `tokenCount`, `namesLength`, `distinctNames` are gone, written
with `<>`, `member`, `remove`, `removeAll`, `distinct`, `all`, `any`, `filter`, `map`, `concat`, `lookup`,
`isEmpty`, `size`. The generic functions take their type arguments explicitly (`all List Rhs p rs`); the
structure parameters are filled by the elaborator.
Kept on purpose: `removeName`/`removeNames` in program.lth (they also remove dotted names a binder
prefixes, not the core's `remove`), `anySplit`, `anyTerm`, `leftCallsSeq`, `telescopeFree`, `substTelescope`,
`longestPrefix`, `tokenizeWithin`, `lastIsNewline`, `pairsAgree`, `armsAgree`, `renameAll`, `definition`,
`lookupBody`, `allNames` of term_model (a collector): searches or recursions that are not folds.
`CanonIdempotent` and `UnqualifyIdempotent` are gone; `CanonicalForm` states them with the core's
`Pointwise` of `compose f f` against `f`, bare (D-2026-10-18-f, not wrappers). run.py's CORE_COLLISIONS
lost `Beta` and `Lists`: term.lth's `Beta` is `BetaReduces`, translation.lth's `Lists` is `ListLiterals`.
grammar.lth gained `wfField`, `wfPair`, `wfItem`, `wfParam`, `wfArm`, `wfClause`, `wfImportName` (predicates
for `all`, no recursion). library.lth's `sameNames` is `sameVisible` (homonym with term.lth's) and its
`pairValues`, `itemValues`, `armBodies` are imported from program.lth (homonyms gone).
No test program for these files exists; none added.

## Evidence

`luthier check` is clean on the eight files. Differential evaluation, old against new, of 70 well-formedness
terms of grammar.lth's `wf` and `wfProgram` and of ebnf's `litsOf`, `catsOf` and `backtrack` gave the same
values. For term.lth and term_model.lut the differential ran but `luthier eval` leaves a top-level term over
core's `foldList` unreduced (`all List String p ["a"]` prints as `foldList ...` in any file), so the new
side could not be compared there; correctness of those rests on `check` and the pytest selection below.
Metrics (`scripts/core_metrics.py`, shared tree, other bites running): at the start 74 homonyms, 107 shadows,
426 list helpers, 45 unclaimed, 2087 loose; at the end 59, 107, 226, 32, 1973 (real 1325). The share of
bite 10 is not separable.

## Decisions taken on my own

1. `memberChars` is an `any` over the words (the brief's row wrote `all`; its meaning is membership).
2. `Beta` to `BetaReduces`, `Lists` to `ListLiterals`, `sameNames` (library) to `sameVisible`.
3. New `wf...` predicates in grammar.lth instead of inlining each lambda.
4. `removeName`/`removeNames` kept (different semantics).
5. Commit bodies hold one line plus the co-author line, in two `-m` blocks.

Follow-up (refusal-holes fix a37136b): term_model.lut's sum label `Selected` collided with the core alias `Selected`; it is `ArmSelected` (three uses). `check` clean on term_model.lut and certification_model.lut, `luthier test tests/tester/certification_laws.test.lut` exits 0.
