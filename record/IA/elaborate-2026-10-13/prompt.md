# elaborate.py and luthier eval: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec` after kernel bite 1e. Step 2.5, bite 2, of
`record/plan-from-zero-2026-10-13-execution.md` (D-2026-10-13-u, -ab): with it, Luthier runs a
file for the first time.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only the files listed;
a failure from another file is someone else's, report it, do not fix it.

`src/luthier/lib/translation.lth` states the elaboration of the surface tree (`grammar.lth`'s
`Surface`, `SurfaceAct`; in Python `src/luthier/surface.py`, produced by `luthier.parse.parse`) into
the kernel term (`term.lth`'s `Term`, `Act`, `Program`; in Python `src/luthier/term.py`, reduced by
`luthier.kernel.step` and `reduce`) as the theory `Elaboration`, one case law per row of the table
2.S12 of `docs/spec/02-grammar.md`, results compared up to alpha (`luthier.kernel.alpha_equal`).
Write its Python specimen. The theory is stable at 5d7963b; its interface is
`Elaboration (a : Alpha) : { elaborate : SurfaceProgram -> Program, term : SurfaceProgram -> Surface
-> Maybe Term }`: `term` gives `nothing` for a term that does not type; fresh names are free (the
laws compare up to alpha); `true` and `false` are constructor patterns; records go to `Record`,
`RecordValue`, `Proj`; `A + B` to `Sum [("left", A), ("right", B)]`. Left open by the theory on
purpose, to be reported as your choices and not chased as laws: the host call of an applied extern
(spec 10), and the typing beyond what the rules need.

1. `src/luthier/elaborate.py`: `elaborate_program(surface_program) -> Program` and
   `elaborate_term(surface, context) -> Term`, following each law of `translation.lth`; where a row
   needs a type (the operators `*`, `+` by the type of the left operand, numbers, `if` on `Bool` or
   on `Failures`), follow what the theory does without a checker and say in a docstring what is
   approximated until `check.py` exists. Blocks are nested `Let` (D-2026-10-13-aa).
2. `luthier eval FILE NAME [--fuel N]` in `src/luthier/cli.py`: parse, elaborate, reduce the
   definition `NAME` to weak head normal form with fuel `N` (default 10000), print the result with
   a printer of `Term` back to surface syntax good enough to read (write it in `elaborate.py` or a
   small `show.py`); exit 1 with a message on a parse error, an unknown name, or fuel spent.
3. `tests/test_elaborate.py`: one test per law of `translation.lth`, named after the law, on its own
   texts parsed with `luthier.parse.parse`; and end-to-end tests of `luthier eval` on small programs
   you write in `tests/eval/*.lut`: arithmetic on `Int`, a recursive function on `Nat` (factorial),
   a `match` on a `data`, a record and its projection, a block with rebinding, a lambda applied.

Check: `python3 -m pytest tests/test_elaborate.py -q`, then `python3 -m pytest tests/ -q`. Do not
change `src/luthier/lib/`, `parse.py`, `surface.py`, `term.py`, `kernel.py` or their tests; if they
lack something you need, say so in the report. Do not commit. Report in a few lines to
`record/IA/elaborate-2026-10-13/codex.md`: what you wrote, the counts, what `luthier eval` prints
for each program of `tests/eval/`, every law of `translation.lth` not met with its case, and every
place where the theory did not decide.
