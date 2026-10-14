# The theories' two pending laws: Coverage's roles in laws.lth, the callback crossing (D-2026-10-14-a)

Written 2026-10-14 by the coordinating session (luthier-3e, formerly luthier-1b), for a Fable
agent. luthier-03, the theories' session, closed at 11:20 leaving these two
(`record/handoff-2026-10-14.md`, "Closed at 11:10").

## The prompt

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-14-a and -b (the end of the file),
`record/plan/questions-2026-10-14.md`, then the files named below at their latest commits. Other
agents edit `src/luthier/*.py` and `tests/` meanwhile: touch none. You may change
`src/luthier/lib/laws.lth`, `test.lth`, `world.lth`, `world_model.lut`, `term.lth` only, one commit
per file (`git add` its path; never `-A` or `.`; no `git stash` or `git checkout`), messages naming
the decision and the spec items, ending with "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>".

1. D-2026-10-14-b, second half: the law that gives `Coverage`'s constructors (`Bounded`, `Listed`,
   `Drawn`; `Exhaustive` is already read in `ForallOnPoints`) their roles lives in test.lth
   (`GradesAsTerms` or the ordering of coverages: find it) and moves to laws.lth, which defines
   `Coverage`, without repeating a law: if the law needs test.lth's names (`Grade`), split it so
   that the part about coverages alone (their order, the weakest) is in laws.lth and test.lth's
   part reads it. `luthier check src/luthier/lib/laws.lth` and `test.lth` must come clean
   (`PYTHONPATH=src python3 -m luthier.cli check FILE`); both must parse.
2. D-2026-10-14-a, the theory side: a Luthier function passed to a host function and called back
   from the host. State it where it belongs: in world.lth (an action of the host that calls a
   Luthier function is still one action of the world, its calls counted, so that the run's record
   carries the count, 12.S18; the token used once, D4) or in term.lth beside `ExternIsValue` (an
   extern applied to a lambda over an infinite domain is a value until the host demands it; what
   the host gives back is a value). Read 3.S23 as it now stands (1e38cb4) and 10.S8 to 10.S10
   (an extern validated at its first action), and `world_model.lut` for the shape of a host
   action; also state the two other forms of D-a (a record of functions crosses as the record
   with each function a callback; a host function crossing in is an opaque value applicable only
   through the bridge, never reduced: a law that `step` leaves it as it is, beside `ExternIsValue`).
   Mark [proposed] every reading the decision does not spell out, with the item cited above it.
   Every file must parse and `luthier check` clean (report what it refuses if not yours).
Report to `record/IA/theories-2026-10-14/report.md` (commit it): what you wrote, every
[proposed], and what the specimens (run.py) must do for each law, in one line each.
