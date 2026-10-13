# generators.lth, to continue if the session stops: brief for Codex

Written 2026-10-13 by Claude Opus 5.5 for Luciano, beside the first commit of
`src/luthier/lib/generators.lth`; give it to Codex only if the session stops before every section
of the file's index is done.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/generators.lth` is a
theory file of Luthier being written section by section; its header has an index with each
section's status, sources and what it needs. Continue it: take the first section marked `todo`,
write it in the pattern of the sections marked `done` (and of `src/luthier/lib/ebnf.lth`: a record
type of the structure's operations, its laws as Bool-valued definitions over a model `(m : T)`,
then `T := Law1 & ...`), cite the spec items above each law, check it with
`python3 -m luthier.cli parse src/luthier/lib/generators.lth` (with `PYTHONPATH=src`), set its
status to `done` in the index, and go on to the next. Rules: state only what the cited sources say
(docs/spec/07-tests.md, record/decisions.md for the D ids; src/luthier/lib/program.lth, whose Violating and Clean domains §7 generates, and kernel_laws.lth and laws.lth, whose pattern it follows);
where they are silent, write the law the structure's textbook definition gives and mark it
`-- proposed` in its comment; a law whose premise random cases would rarely meet quantifies over a
subtype (as `WrittenProgram` in grammar.lth), not over an implication. Do not write model values in
this file (a checker is a Python specimen, step 4). Do not touch other files except your report. Do not
commit. Report in a few lines to `record/IA/generators-2026-10-13/codex.md`: the sections written,
and every place where you had to choose.
