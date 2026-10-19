# Naive review of core bite 5 (fd7b9ee..bd59354, report 8ac13f7)

2026-10-19, Claude Sonnet 5.5, on prompt-review-bite-5.md. Nothing in the repository was changed
but this file. Probes are small files in /tmp/rv, run with `luthier check` (and `eval` for one).

## Findings

1. The refusal has a hole for the names in CORE_COLLISIONS: they are exempt for every file, not only
   for the listed one. `redefinitions` (src/luthier/run.py:209) skips a name when ANY core file that
   defines it is a known collision (`any(known_collision(p, n) for p in others)`). So a user file that
   writes `Idempotent : Bool := true`, `Symmetric`, `Reflexive` or `Associative` passes check with no
   refusal (probed; `Both`, `flip`, `Beta`, `Lists`, `PlusCommutes` are refused as intended). The
   exemption was meant for the two files of each pair (equality.lth/relations.lth, functions.lth/
   operations.lth, algebraic.lth/properties). Fix: exempt only (file, name) pairs listed, and for a
   non-core file only its own entry.
2. A data constructor is covered (`unit`, `cons`, `true` refused, run.py:_defines 226), as are
   definitions, declarations, aliases and models. Four paths are not covered, all silent:
   a. An `operator` act: `operator + := intMinus` passes check; `eval` of `5 + 2` still gives 7
      (the core's meaning wins silently), so the file believes something that is false.
   b. A label of a sum alias: `S = { unit : Int || compose : Int }` passes check and `r : S := unit 3`
      too (`_defines` reads only DataBody constructors, not sum labels).
   c. An import alias: `import "core/structures/algebraic.lth" Monoid as compose` passes check
      (`_defines` ignores ImportAct names).
   d. A record field (`R : { compose : Int }`) and a parameter or pattern variable (`f (compose : Int)`,
      `match x { compose -> compose }`) pass. Fields and local binders are probably meant to stay
      free (they are not top-level names; D-2026-10-18-b is about names of the core), but neither
      the spec 12.S22 text nor the report says so. A field named as a core structure's field
      (`eq`, `map`) is the case that will matter at bite 6.
3. CORE_COLLISIONS is the only list of exceptions in the code (run.py:153; check.py:core_refusals
   and Loaded both call `redefinitions`, no other bypass; `--no-core` is a separate switch,
   check.py:60). Each of the nine entries names its bite in the second element of its tuple
   (8, 9, 11, 10, 10, 6, 6, 6). No entry is stale: each name is still defined in its file and in
   another core file (checked by parsing). But it is exactly the "only a few remain" the decision
   forbids in the end state: 26 names in non-core files plus 7 inside the core (report Question).
4. A name two core files define is not part of the prelude: check excludes it (check.py:core_names,
   `len(files) == 1`) and the loader says it is defined by both. D-2026-10-18-b says the whole core is
   visible without an import; for those 7 names a file must import from one core file. Declared in
   the report; the same list (item 3) removes it at bite 6. Not a contradiction while the list lives.
5. Qualified access works, but bite 5 did not add it: `git diff ff7fe35 HEAD -- src` has no qualified
   code, and the report's title names it without a line on it. It is bite 4's (tests/test_check.py:564,
   tests/test_elaborate.py:471). Probed: `Object.eq 1 2` and `Monoid.combine` resolve the structure
   with no import (core structures reachable unqualified-prefix, good) and fail with "no model of
   Object at Int; the models claimed: none" because the core claims no models until bite 6;
   `Object.nosuch` is "Object has no field nosuch"; `Bogus.eq` is 4.R2. `Function.compose` is 4.R2:
   `compose` is not a structure's field, so `Struct.name` is only for fields of a structure
   (consistent with execution.md section 3.3). Qualified access to a core name that is not a field
   does not exist, and the decision's phrase "qualified access disambiguates where needed" is met
   only for fields.
6. Contradictions with D-2026-10-18-b: (a) items 1 and 2 (a core name can be redefined without
   refusal); (b) item 4. The rest holds: the core directory is the prelude (run.py:142, Loaded 460),
   a redefinition names the core file, the redundant import is a notice, not a refusal (the plan's
   [proposed], consistent with the decision, which says nothing of imports).

## What was checked

Refused as intended (def, decl, alias, data constructor, model value, uppercase theory name,
`--no-core` off): def.lut, decl.lut, alias.lut, data*.lut, model.lut, upper.lut, c_Both, c_flip,
c_Beta, c_Lists, c_PlusCommutes. Not read: the test files' bodies beyond the names in the report, and
the suite (not run; the report says 862 passed).

## Question for the coordinator

Close items 1 and 2a to 2c in a small commit before bite 6 (they make the refusal false for
three kinds of name), or let bite 6 do it with the list?
