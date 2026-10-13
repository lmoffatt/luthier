# kernel.py, bite 9: the primitives of the numbers and strings, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). After bite 8 (323b402) and the
slice's theories (report `record/IA/slice-theories-2026-10-14/report.md`, section "What the
kernel and the bridge must do": read it first, "Kernel" part).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (on run.py, host.py, arrays.py,
and on theory files): change only `src/luthier/kernel.py`, `src/luthier/cli.py`,
`tests/test_kernel.py`, and write your report; a failure from another file is someone else's.

term.lth §5 at 681742e (`git show 681742e`) states `PrimInt`, `PrimFloat`, `PrimString`,
`PrimConvert` beside `Prim`; `src/luthier/lib/core.lut` (3c43822) names the primitives. Mirror
them in kernel.py: Int `/` and `mod` by floor (a zero divisor never steps), Int `<=`, `>`, `>=`,
`/=`; Float64 `-`, `*`, `/` and the comparisons `<`, `<=`, `>`, `>=`, `/=` (a NaN or infinite
result is an error, 11.S7); String `+`; `toFloat64` on an Int. A body `primitive "<name>"` is the
kernel's `Primitive "<name>"` (3.S39). For the infix forms the elaborator emits (`Var "+"`, `Var
"<"`, ...): extend cli.py's bootstrap (`Define(op, Universe, Primitive(op))`, line ~56) to the new
symbols and to `toFloat64`, as the reversible choice tonight (the alternative, resolving through
core.lut's `operator` acts, is for a later bite; say so in the report). `and`/`or`: if the kernel
has no reduction for them, add one on `Var "true"`/`Var "false"` operands and say so. Tests for
each clause, including the stuck and error cases; `tests/eval/`, `tests/test_run.py` still pass.

Check: `PYTHONPATH=src python3 -m pytest tests/test_kernel.py tests/test_run.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in a few lines to
`record/IA/kernel-2026-10-13/report-9.md`.
