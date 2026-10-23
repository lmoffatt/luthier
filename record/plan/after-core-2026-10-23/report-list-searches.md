# Report: `foldLeft`, `takeWhile`, `dropWhile` and `find` in the core

Agent: Claude Sonnet 5.5, 2026-10-23, brief `prompt-list-searches.md`. Commits: ba7d02c (the functions),
d18e118, 8901dff, 49337e2 (the helpers moved), and the stores' commit after them. Scratch and logs
(not versioned): `~/.cache/luthier-searches/` (`diff/` has the old copies, the driver and the eval
terms; `pass*.log`, `suite/`, `metrics-*.txt`).

## Functions and laws added (lib/core/lists.lut)

`foldLeft A B step e xs` (Haskell's `foldl`; named as the brief's title does), `takeWhile A p xs`,
`dropWhile A p xs`, `find A p xs : Maybe A`. No other function was needed by the helpers. Five laws,
each a claim in `ListLibrary` with a replaceable candidate, a profile in `lists_laws.test.lut` and a
broken candidate in `lists_controls.test.lut` (all refuted):

- `FoldLeftIsFoldRightOfReverse`: `foldLeft step e xs` equals the right fold into `B -> B` over
  `reverse xs`, applied to `e`. Control: the step with its arguments flipped. The test step is
  `2 * acc + x`, which does not commute (subtraction would not tell order from its reverse).
- `FoldLeftAppends`: folding `xs <> ys` equals folding `ys` from the result of folding `xs`.
  Control: a fold over the reversed list.
- `TakeWhileDropWhileSplit`: `takeWhile p xs <> dropWhile p xs == xs`. Control: `filter p` as takeWhile.
- `TakeWhileStopsAtFailure`: every element of `takeWhile p xs` satisfies `p`, and the head of
  `dropWhile p xs`, if any, does not. Control: a dropWhile that drops nothing.
- `FindIsHeadOfFilter`: `find p xs == nth (filter p xs) 0`. Control: the last match instead.

The lists tested are `searchValues`, with the failing element first, middle and last. `lists_laws`:
20 laws, `lists_controls`: 20 controls, both 0 lines ran on the second pass.

## Helpers moved (14) and kept

Moved: plan.lth `addNew`, `runFrom`, `demandAll`; certification.lth `behind` (`drop 1 (dropWhile ..)`),
`along` (a `foldLeft` into `Maybe`); generators.lth `before` (`total` of a `takeWhile`); ebnf.lth
`leftCallsSeq`; ebnf_model.lut `remaindersSeq` (`remaindersFrom` is gone); grammar.lth `longestPrefix`
(`find` over the reversed splits); term_model.lut `lastComponent`, `applyArguments`, `finishBindings`,
`demandFields`, `demandTerms` (`dropWhile` for the part to step, `takeWhile` for the front rebuilt).

Kept, with the reason (comments of the kept ones are unchanged, "kept as a recursion (bite 13b)"):
- State and a result both threaded, which a `foldLeft` would carry only in a pair that reads worse than
  the recursion: `placedBefore`, `byLevels`, `sumOfLargest`, `bindingsFrom`, `unusedRebinding`,
  `itemsFault`, `disputes`, `substTelescope`-family counters (`canon*`, `freshArm`, `stageBindings`).
  This is my judgement, not a limit of the core; the review counted several of these among the ~20.
- A search whose result is computed on the way, which `find` on a Boolean would compute twice:
  `chooseArm`, `pick` (with its fallback to the last positive weight), `determined` (pairwise over tails),
  `tokenizeWithin` (fuel).
- Telescopes, `renameAll`, `swapAt`, `allNames`, `badCitation`, `anyTerm`, and the two broken controls in
  lists_controls: as review-close.md item 2 says.

## Differential (luthier eval, old copy against new, same terms)

194 terms over the 14 helpers (empty lists, first element matching, none matching, state carried in,
a stuck element): 190 equal, 4 stuck in both with the same message (`longestPrefix` over the
`lexeme` rule, which needs the primitive `characters`), 0 differ. By helper: addNew 6, runFrom 20,
demandAll 24, before 7, lastComponent 8, applyArguments 4, finishBindings 4, demandTerms 9,
demandFields 7, behind 24, along 10 (with a refusing transport), leftCallsSeq 9, remaindersSeq 30,
longestPrefix 32. Driver and terms: `~/.cache/luthier-searches/diff/drive.py`, `drive2.py`.

## Checks

- Certification: tests/tester, 44 files. First pass 40 rc 0, one timed out (probability_laws, 3000 s,
  my session was cut); second pass left probability_laws at 6 lines; a third pass 7, a fourth 0. A final
  pass over all 44 (`xargs -P6`): 0 lines ran in 44 files. rc 1 on belief_laws, cases and laws, as before
  my change (known refutations and uncontrolled notices). Stores committed.
- Suite: every tests/test_*.py by itself under `timeout 1800` (42 files); see the last section.
- `scripts/core_metrics.py`: before (c44d0e5 tree, 45 helpers) homonyms 0, shadows 113, list helpers 45,
  unclaimed 7, loose 1407 (real 1330, rest 77). After: homonyms 0, shadows 113, list helpers 33,
  unclaimed 7, loose 1415 (real 1338, rest 77).

## Two things the numbers hide

1. List helpers fall by 12, not 14: `demandFields` and `demandTerms` still count, because their body
   now matches `nil`/`cons` on the result of `dropWhile`; they no longer recurse. The metric looks at the
   shape of the match, not at the recursion. The honest count is 31.
2. Loose rises by 8 (nine new definitions, `remaindersFrom` gone). The four functions and five laws are
   loose in the same sense as `filter` and `FilterKeeps` and every other core list definition. "Nothing
   up" is true of helpers, unclaimed and homonyms, not of loose.

## Decisions I took on my own

The name `foldLeft` (the brief's title) over Haskell's `foldl`; no law for the helpers kept; the pair-state
helpers kept; fixing the count in tests/test_lists.py myself; not touching `core_metrics.py`.
One commit message said "seven" helpers and was amended to "eight" before anything else. None for
`record/decisions.md`.

## Question

Should the helper count in `core_metrics.py` look for recursion (a body that calls itself) instead of the
`nil`/`cons` shape, so `demandFields` and `demandTerms` leave it, and should loose exclude Bool-typed laws
and functions with a law (review-close.md item 4)?

## Suite

42 files: 37 pass, test_check_private collects nothing (rc 5, as before). Failures, and what they are:
- test_lists (2): it asserted 15 laws in lists_laws and lists_controls; there are 20 now. Mine, fixed in
  tests/test_lists.py (15 to 20); 17 passed afterwards.
- test_run (18), test_plots (1): stderr carries "tests/run/luthier.lock pins interpreter v0.2, this is v0.3
  (12.S13)". The lock is an untracked file left by earlier runs, so this is the tag, not my change.
  Not touched; deleting or re-locking it is Luciano's or the tag's.
- test_render_grammar (1): docs/spec/02-grammar.md is stale against scripts/render_grammar.py (last
  touched in 09182bb). Not mine; I did not run `--write`.
I did not re-run the three against the tree before my first commit, so "not mine" for them rests on the
messages, which name neither lists nor the helpers moved.
