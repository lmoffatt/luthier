# Internal review of the layer 2 and 3 theories: brief for an Opus subagent

Written 2026-10-13 by Claude Fable 5.1 (the coordinating session) for a Claude Opus 5.5 subagent.
Read only: you write exactly one file, `record/IA/opus-2026-10-13/review-layers-2-3-report.md`, and
commit it alone (`git add` that path; never `-A` or `.`; message ending with
"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"). Other agents edit the tree meanwhile.

Read `CLAUDE.md`, `docs/principles.md` (Terms, L2, L9, L10, L11, L14), then the chapters and the
theories: `docs/spec/07-tests.md` with `src/luthier/lib/generators.lth`, `generators_model.lut`,
`test.lth`; `docs/spec/10-world.md` with `world.lth`, `world_model.lut`, `examples/hello.lut`;
`docs/spec/12-files-and-tools.md` with `library.lth`. These were not reviewed externally (layers 0
and 1 were: see `record/IA/layers-0-1-review-2026-10-13/A-prompt.md` for the questions asked, and
`summary.md` for what such a review finds). Review them the same way, per file, numbered, quoting
the line: (1) laws false of the intended model or unsatisfiable together; (2) laws that do not
determine what they claim, with the wrong model that passes; (3) constructors of a `data` with no
law of their role (L2.7), or role laws that only list constructors; (4) the models against their
theories, with the case; (5) where a file says other than its chapter or a cited decision
(`record/decisions.md`); (6) laws stated over a type with an implication a random case rarely
meets instead of the subtype (7.S12, L9.6); (7) what you would change first, one thing. Verify
each finding against the file before writing it; a claim you cannot verify goes in a "not sure"
list. Do not rewrite the files; do not reopen cited decisions.
