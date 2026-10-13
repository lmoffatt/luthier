# The inventory of sonolocalización: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec`. Step 1 of
`record/plan/sonolocalizacion/plan-sonolocalizacion-2026-10-13-execution.md`, on D-2026-10-13-ac.

## The prompt

Read `CLAUDE.md` of this repository first. Your task is to read another repository,
`/home/lmoffatt/Projects/sonolocalizacion`, and write one report here. **Do not change anything in
sonolocalización** (read only: no edits, no commits, no scripts run there; its owner runs its
scripts). In this repository write only `record/IA/sonolocalizacion-inventory-2026-10-13/inventory.md`.

Sonolocalización is a scientific project (localizing sound sources from recordings) written partly
in Luthier v0.1 (the retired interpreter, files `*.lut`, tag `v0.1-final` here) and partly in
Python. Luthier is being rebuilt from its theories (`docs/spec/`, `src/luthier/lib/*.lth`); the plan
is to make the new Luthier run one analysis of sonolocalización end to end, and to design the
evidence and certification of laws on that case. Read its `README.md`, `PIPELINE.md`, `CLAUDE.md`,
`docs/`, `sonolik/`, `prototipo-cero/`, `scripts/`, `tests/`, and every `*.lut`; skip `archive/`,
audio and image files, and the folders of the owner's notes (`Lucianos *`).

Write `inventory.md`, in English, with:
1. **The analyses**: each pipeline or analysis the repository runs, in one line each, with its
   entry point; then pick the one that is the smallest end-to-end case (data in, result out) and say
   why.
2. **For that analysis, a table** with one row per thing it needs, columns: item; where in
   sonolocalización (file:line); kind (a v0.1 Luthier library, a Luthier construct, a Python
   package, a data format, an external program); and what of the new Luthier would provide it (a
   spec chapter or item of `docs/spec/`, a theory of `src/luthier/lib/`, or "missing").
3. **The laws**: every law, check or certificate it states (in `.lut` or in Python tests), with
   what kind of evidence it needs: exact (Boolean on finite cases), sampled (random cases), a
   tolerance on floating point, statistical (a p-value or a likelihood), or a citation.
4. **The data**: the formats read and written, their sizes, and how they are read today.
5. **The world**: every action on the outside world (reading or writing files, randomness, clocks,
   calls to programs or to numpy, scipy or other libraries).
6. **What is missing** in the new Luthier for this analysis, ordered by what blocks first.
Quote file paths with line numbers. Say where you were unsure. Do not commit.
