# The reading guide rewritten for the current language: brief for an Opus subagent

Written 2026-10-13 by Claude Fable 5.1 (the coordinating session) for a Claude Opus 5.5 subagent.
You may change exactly one file, `docs/guide/00-fundamental-elements.md`, and commit it alone
(`git add` that path; never `-A` or `.`; small commits, messages naming what changed, ending with
"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"). Other agents edit the tree meanwhile.

Read `CLAUDE.md`, `docs/principles.md` whole, `docs/spec/00-index.md`, `01-terms.md`, `02-grammar.md`,
`03-kernel.md`, `04-static-semantics.md`, `05-laws.md`, `10-world.md`, `12-files-and-tools.md`, the
theories `src/luthier/lib/ebnf.lth`, `grammar.lth`, `kernel_laws.lth`, `term.lth`, `world.lth` and
the models beside them, `examples/hello.lut`, `tests/eval/*.lut`, and the guide as it is. The guide
dates from 2026-10-04, before the specification: it cites chapters by numbers that changed, uses
syntax that changed since (lambdas are `fn`, labeled sums are `{ a : A || b : B }`, `let` is gone,
a block is nested `Let` in the kernel, records are named products with `Record`/`RecordValue`/`Proj`,
theories are `.lth` files and models `.lut`, a definition is a concept and every constructor has a
law of its role, L2.7), and some of its content predates decisions in `record/decisions.md`.
Rewrite it as the reading guide for someone meeting Luthier now: the few ideas a program is made
of, in the order to think them (a type is a theory, a value is a model, laws, certification by
testing, the world token, the theory/model pattern of the first files), with one program executed
by hand (take `tests/eval/factorial.lut` or `examples/hello.lut`), every term defined before use,
citing spec items (`spec 3.S14`) and principles (`L2.7 (a definition is a concept)`) by number with
their statement at first use. Keep what in the old guide is still right and his (sentences marked
as his, or citing his notes in `record/audios/`), and say at the top what the rewrite is and from
what. English, no em-dashes, no sentence of eight words copied from the spec or the principles
(cite instead; `python3 scripts/check_spec.py` must pass, run it before each commit). Report, as
your final message: what you dropped from the old guide and why, and what you were unsure of.
