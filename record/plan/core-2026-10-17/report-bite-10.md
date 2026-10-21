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

## Differential after a182ed5

Run 2026-10-22 on HEAD (02c70e1) against 010d17c^ in a `git worktree` (386a5f0, "Bite 9"), both with
`/home/lmoffatt/miniconda3/bin/luthier eval FILE TERM` (the same installed core, so only the library
files differ). The old copy of term.lth and term_model.lut carried the three renames that bite 10 made
after its main commit (`Beta` to `BetaReduces`, `ArmStep`'s `Selected` to `ArmSelected`; `Lists`
does not occur in them) so the old files load; no other edit. 208 terms, each evaluated on both sides,
first output line compared as text (list: /tmp/difft/terms.txt, results: /tmp/difft/out.tsv, script
/tmp/difft/run.sh; scratch, not kept in the repo).

Terms, by rewritten function (edge cases: empty lists, duplicate names, a binder that shadows or
prefixes a name such as "y" and "y'", "x" and "x0"): term.lth `freeVars` (every constructor: Lam, Pi,
Sigma, Subtype, Let, Match with empty and repeated pattern variables, Data with its own name among the
constructors, Sum, Record, RecordValue, Proj, Inj), `patternVars`, `patternsVars`, `swap` (Match,
Data, Record, Sum, Let, x = y), `swapPatterns`, `sameNames` (7 terms: empty, permutation,
duplicates both ways, strict inclusion), `free` (7 programs); term_model.lut `textAppend`,
`unqualified`, `freshName`, `allNames` (all constructors), `armNames`, `pairNames`, `recordNames`,
`substTerm`, `substArms`, `substPairs`, `substTelescope`, `swapLocalPairs`, `canonicalTerm`,
`nextBinder`, `canonBindings`, `linearBindings`, `bindingNames`, `bindingTermNames`,
`applyBindings`, `stepPattern`, `stepTerm` (Match, Proj through RecordValue and through a definition,
beta, equality), `constructorType`, `equalValues`.

Result: 192 equal, 16 differ. The 16 are all the same print difference and not a disagreement:
`textAppend`, `canonicalTerm`, `nextBinder` and `canonBindings` leave `textJoin (...)` of the two
text lists unreduced on both sides (`textParts` is stuck, so `textJoin` never fires), and the old
side prints `appendText (textParts "x") (textParts (natDecimal 0))` where the new one prints
`{ neutral := nil, combine := combineList String }.combine (textParts "x") (textParts (natDecimal 0))`,
which is the same call by `<>`'s definition. Of the 192 equal, 28 are equal only as the same
`stuck match` or the same unreduced `textJoin`; these are the terms that need `freshName`,
`unqualified` or `canonName` to reduce (freshName with a collision, substTerm and canonicalTerm that
rename a binder, nextBinder and canonBindings with an `avoid` list that hits, applyBindings with two
or more bindings). Neither side evaluates them, so for the `<>` in `lastComponent`, the `member` in
`freshName` and `nextBinder`, and the `allNames`-fed `avoid` lists of the renaming paths the
differential says nothing. The other 164 are values (lists of names, Bools, terms, Maybe, pairs)
and agree; that covers every use of `remove`, `removeAll`, `<>` on names and bindings, `concat`,
`map`, `all`, `distinct` and `lookup` outside those paths.

Verdict: no disagreement found, no fix made. The open part is the stuck terms (28), which wait for
`textParts` and `textJoin` to reduce in `luthier eval`; until then their correctness rests on `check`
and the pytest selection, as before. The `foldList` obstacle of the first differential is gone: `all`,
`distinct`, `removeAll` and `remove` reduce to values at a182ed5.

## Differential after the text fix

Run 2026-10-22 by Claude Sonnet 5.5 on `prompt-eval-text.md`. No fix was made: `textParts`, `textJoin` and
`natDecimal` are declared holes of term_model.lut with no body, and a term with a hole where the reduction
needs a value does not reduce (spec 3.S19); the kernel has string `+` and `==` but no decomposition of a
string (spec 11 gives none, as term_model.lut's comment says). Details in `report-eval-text.md`.
To compare the renaming paths anyway, both sides ran with a scratch model of the three holes, the same text
on each side (a table for the dotted strings used, `[s]` for any other, `<>` for join, a table for `natDecimal`
0 to 3), in two `git worktree`s under `~/.cache/luthier-sdk/difft/` (old: 010d17c^ with `Beta` to `BetaReduces`
in term.lth and `Selected` to `ArmSelected` in term_model.lut; new: HEAD 43f6d3d), each run with the installed
`luthier eval FILE TERM` from its own lib directory (script `run.sh`, terms `terms.txt`, results `out.tsv`,
overlay `overlay.py`, all there; scratch, not kept in the repo).

Terms: the 208 of the earlier run plus 33 that exercise `freshName` (collision, chain, dotted name),
`unqualified`, `canonName`, `textParts`, `textJoin`, `canonicalTerm` (renaming binders, a free `x1`),
`substTerm` (Lam, Pi, Sigma, Let, Match, Subtype with a capturing binder), `applyBindings` (swap, chain, three
bindings, Match), `nextBinder`, `canonBindings`. 241 terms: 241 equal, 0 differ, and every one reduces to a
value (no `stuck match`, no unreduced `textJoin`). That includes the 28 that were stuck before and the
16 that differed only in print.
Verdict: no disagreement found over the renaming paths, under the scratch model of the text holes; the
real holes stay unfilled, so this checks the rewrite of `member`, `<>` and `allNames`, not the model of text.
