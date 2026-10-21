# Brief: a document on Luthier's key concepts and the logic that joins them

Luciano asked (2026-10-21): "un documento md y pdf que expliquen los conceptos clave de Luthier y la
lógica que los une". This is its first draft; he will annotate it.

Reader: a scientist who likes mathematics and writes some code (a biologist or physicist), new to
Luthier, who wants to understand what its pieces are and why each follows from the others, before
reading the spec. Not a tutorial on the syntax, not the spec again.

Read first, in this order: `CLAUDE.md`; `docs/principles-for-readers.md`; `docs/guide/00-fundamental-
elements.md`; `record/principles-language.md` (the source of the principles; `docs/principles.md` is
its projection); `docs/spec/00-index.md` and, as needed, the chapters it points to;
`record/plan/core-2026-10-17/execution.md` sections 0 to 4 (the core being rebuilt now: the
structures, names resolved by type, the three planes, the within-bound laws); `record/decisions.md`
from D-2026-10-16 on, and the decisions the other documents cite. Read what `record/Lucianos
observations/` holds on the principles and the guide. Grep before reasoning: when a concept's reason
is in a principle, a decision or a spec clause, cite it there instead of reconstructing it.

Write `docs/concepts.md`. What it must do:
- Name the key concepts (at least: theory, model, law, claim; the core and its structures;
  certification, the store and its cone hash; test programs, grades and controls; demand and the
  planner; the world and actions; numbers and within-bound laws; the three planes; the algebra of
  error, uncertainty, evidence and resources) and say for each what it is, in plain words first and
  then in its mathematical form where one exists.
- Above all show the logic: why a law needs a control, why a certificate is keyed by a cone, why
  demand decides what runs, why names resolve by type, how the three planes keep a claim apart from
  its evidence and its execution. One thread the reader can follow from "I write a theory" to "a run
  I can trust", with each step justified by what came before it.
- One small example carried through the document, in real Luthier that `luthier check` accepts
  (run it with `/home/lmoffatt/miniconda3/bin/luthier`; put the example's files under
  `docs/concepts/` so they can be checked). Prefer an example from the library or
  `examples/sonolocalizacion/` over an invented one.
- Mark what is settled and what is [proposed] or still being built (the core rebuild is in progress:
  say which names may still move). Cite each claim's source as the documents do: a principle by its
  number with its statement ("L10.12 (a store lives beside the file that claims it)"), a decision by
  its id, a spec clause by its number. What you propose yourself, mark as yours.
- Define every symbol and abbreviation at first use. Length: what the logic needs, likely 12 to 25
  pages; no padding.
- Write for a human reader: no em-dashes as punctuation, no "not X but Y" constructions, no inflated
  vocabulary, no closing summaries; contractions are fine.

Then the PDF: `pandoc docs/concepts.md -o docs/concepts.pdf --pdf-engine=xelatex` with whatever
options make it readable (a font with the Unicode the text uses, a table of contents, margins); put
the exact command in a comment at the top of `docs/concepts.md` so the PDF can be regenerated, and
check the PDF renders every symbol (no missing glyphs in xelatex's log).

Don't touch the library, the tests or the plan: bite 11's agent is working in arrays and tables and
runs the suite. Small commits staged by path: a subject, a blank line, one body line, ending with
"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Commit the markdown, the example files
and the PDF.

Accepted when: `luthier check` accepts the example files; the PDF builds with no missing glyph;
`python3 scripts/project_principles.py --check` still passes; every principle, decision and clause
cited exists with the statement given. Report in your final message: the outline, the sources each
section rests on, what you marked [proposed] or yours, the gaps you found (a concept whose reason
you couldn't find written anywhere), and decisions taken on your own. At most one question.
