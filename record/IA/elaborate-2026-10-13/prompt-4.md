# elaborate.py, bite 4: a block item with a pattern on `<-`, brief for a Claude agent

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session, luthier-1b), for an Opus agent launched by it. After bite 3 (codex-3.md) and after the
parser follows D-2026-10-13-ag (the left of `<-` a pattern: `surface.Rebind` takes a
`SurfacePattern`, report `record/IA/sums-2026-10-13/opus-rebind.md`).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only
`src/luthier/elaborate.py`, `tests/test_elaborate.py` and the `LIMITATIONS` table of
`tests/test_spec.py` (removing an entry whose case now passes); a failure from another file is
someone else's, report it, do not fix it.

`src/luthier/lib/translation.lth` (87d6091 or later), law `Blocks`, says what a block item
`rebind q t` elaborates to (read the law and its comment, with spec 2.S12, 2.S17, 4.R12 and
D-2026-10-13-ag in `record/decisions.md`):
1. when `t` is an action (its type is `W * A` for the world `W`), the item is a `match` with one
   arm: `Match t [(pattern, rest)]` where `pattern` is the surface pattern translated as in a
   `match` arm (`(w1, s) <- readFile w0 "f"` gives `PPair (PVar "w1") (PVar "s")`), and `rest` is
   the rest of the block;
2. when `t` is an action of type `W * Unit` and `q` is a bare name, the arm is `PPair (PVar w1)
   PWild`: the token is bound and the unit dropped;
3. when `t` is not an action and `q` is a bare name, the item is a `Let` on a fresh name as
   before (the renaming of `y` to `y0`, `y1`).
A pattern that is not a bare name on a value that is not an action: translation.lth does not say;
refuse with a message naming the item, and report it as a question. Each case with a test in
`tests/test_elaborate.py` mirroring the law's three `gives`, and `examples/hello.lut` plus the
programs of `tests/eval/` and `tests/spec/` still elaborating as before.

Check: `PYTHONPATH=src python3 -m pytest tests/test_elaborate.py tests/test_check.py
tests/test_spec.py tests/test_run.py -q`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not
commit. Report in a few lines to `record/IA/elaborate-2026-10-13/opus-4.md`: what you changed,
where translation.lth did not decide and what you chose, what failed and whose it is.
