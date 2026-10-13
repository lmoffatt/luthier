# Luthier in sonolocalización: the execution

Draft 0, 2026-10-13, for the session of the next quota cycle. Rests on S1 to S5 of
`plan-sonolocalizacion-2026-10-13-decisions.md`; until Luciano marks them, assume them as
recommended and say so. Rules as in `plan-from-zero-2026-10-13-execution.md` (Z9: the session
writes theories; Codex what must run and iterate; a web model small bites).

## Status

- 2026-10-13: written; nothing started.
- 2026-10-13, night: S1 accepted (D-2026-10-13-ac); step 1, the inventory, running (Codex, read
  only; brief record/IA/sonolocalizacion-inventory-2026-10-13/).
- 2026-10-13, night: S5's minimal VS Code extension done by Codex (`tools/vscode-luthier/`): colours
  from `luthierSyntax`, parse errors as diagnostics; run from source, see its README. Luciano has
  not marked S5; one commit undoes it. The plan from zero is at step 2.2 (`term.lth`, another
  session) with `kernel.py` next (D-2026-10-13-u).

- 2026-10-14, 05:40 (the night, record/plan/night-2026-10-13.md): step 1 done by an Opus agent
  (inventory at 5cce858; the sonolocalización session's answers at c49b34b). Step 2 taken as the
  inventory's §6, items 1 to 5. Step 3 begun: the theories (core.lut, numbers, arrays, tables;
  3c43822 to d63cee7), the kernel's primitives (c2a63d0), the bridge (2821823), the port of
  validate_graph.lut with session A's graph copied (2b9a2c5 to 9ea7d8f, examples/sonolocalizacion/);
  the run reads the graph and stops in run.py (bite 5 running). Codex is gone: specimens by Claude
  agents.

- 2026-10-14, 07:00: step 3's first stage done: `validate_graph.lut` (port at
  examples/sonolocalizacion/, run.py bite 5 and kernel bite 10) runs end to end on session A's old
  graph and prints its summary line (21 distinct pairs, 14 unseen directions) in about five
  minutes, uncertified. Step 4 waits for Luciano: a v0.1 run of validate_graph.lut on the same
  graph as the reference, and the corrected graph (prepare_experiment_zero.py). The second stage,
  `experiment_zero.lut`, needs functions across the bridge (inventory §6 item 6), unstated in the
  spec: his question.

## Steps

1. Inventory, read only (Luciano runs any script there): in `~/Projects/sonolocalizacion`, which
   v0.1 Luthier libraries and which Python packages the analysis uses, which data formats it
   reads, which laws or checks it already states. Output: one table, item against the layer or
   library of the plan from zero that provides it. A Codex task with a brief, or the session if
   short.
2. The slice: from the table, the minimal set of theories and specimens to run one analysis end to
   end, in order; marked against the plan from zero (which steps it pulls forward, which it
   shrinks). To Luciano as one screen before starting.
3. Execute the slice, theories by the session, specimens by Codex; one external review round for
   the slice's theories.
4. Run the analysis; compare with the current results of sonolocalización.
5. The same for macroir (S4).

Beside it, at the start of the cycle: the minimal VS Code extension (S5), a brief for Codex.
