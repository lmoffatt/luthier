# Brief for a chapter of the specification

The template every agent that writes a chapter receives, filled for its chapter. Written
2026-10-12 (step 0 of `record/plan-spec-2026-10-12-execution.md`). An agent has nothing but this
brief and the files it names.

## Goal

Write chapter N of the specification of Luthier, `docs/spec/NN-<name>.md`, from the sources named
below, in the shape given below, so that `scripts/check_spec.py` passes on it. The chapter
describes the language designed, not only what runs: every rule carries its status.

## What the specification is

Luthier is a language in which a type is a theory (structure with laws), a value of it is a model,
and the language verifies models of theories. The specification is one document in twelve
chapters; this chapter is one of them. The principles are `docs/principles.md` (read its Terms,
its organizers G0 to G2, and the entries this brief names); a chapter realizes principles and
never contradicts them. If you find a contradiction between a source and the principles, do not
resolve it: write the rule as the principles say, and name the contradiction in your report.

## The shape of a chapter

- First line: `# N. <Title>`. Then one paragraph: chapter N of the specification, draft 0,
  date, sources by path and commit, who wrote it (your model name), the principles it realizes.
- Sections `## §k <Title>`, numbered from 1. The last section is `## Open`, which cites the open
  questions of `docs/principles.md` by their ids (O1 to O12) and adds nothing of its own.
- Two kinds of item, each a paragraph:
  - a rule, `**N.Rk. <Title>.** [status] <text>` followed on its last line by
    `Files: <name>.accept.lut, <name>.reject.lut.` naming programs in `tests/spec/`; a rule is
    what a program can be accepted or rejected by;
  - a statement, `**N.Sk. <Title>.** [status] <text>`, for a behaviour no single program decides
    (a reduction rule, a grammar production, what a command does).
- The status is one of `[implemented]`, `[decided D-YYYY-MM-DD-x]` (decided by that entry of
  `record/decisions.md`, not yet in the interpreter), `[proposed]` (yours or your source's, awaiting
  Luciano's mark). A rule `[implemented]` names both files and they exist; take the names from
  `tests/spec/` and do not invent files.
- Citations: another chapter as `spec M §k` or `spec M.Rk`; a principle as `L5`, a clause as
  `L5.3`, an organizer `G1`, an open question `O3`, a decision `D-2026-10-11-c`, the way of working
  `W5`, the method `P11`. Every citation must resolve; the check verifies it.
- Terms: use the words of `docs/principles.md` Terms (structure, theory, model, specimen, law,
  certifier, certificate, cost, resources, demand, planner, action, world, object) and define
  nothing twice; chapter 1 holds the notation, cite it as `spec 1`.
- Where the kernel can express a rule as a theory in Luthier (L14), name the `.lut` file that
  states it or would state it, and mark `[proposed]` what is not written yet.
- No sentence of eight words or more copied from another chapter or from `docs/principles.md`:
  cite instead. Keep the words of your source where the source is decided or implemented; what
  you add is `[proposed]`.
- English; no em-dashes; every symbol defined or cited before use.

## Sources

<filled per chapter: paths with commits; which parts to take; which to leave to another chapter>

## Decisions in force

<filled per chapter: the D ids and their one-line statements that bind this chapter>

## What not to touch

The principles, the interpreter (`src/`), `tests/spec/` (you read it, you do not write it), the
other chapters, the record. You write exactly one file, `docs/spec/NN-<name>.md`.

## Check

Run `python3 scripts/check_spec.py docs/spec/NN-<name>.md` and make it pass. Then run
`python3 -m pytest tests/test_spec.py -q` to confirm the suite is untouched.

## Report

Return, in this order: what of the source you dropped and why; what you marked `[proposed]`; any
contradiction between the sources and the principles, as one question each; the `.lut` theories
the chapter names and whether they exist. Nothing else.
