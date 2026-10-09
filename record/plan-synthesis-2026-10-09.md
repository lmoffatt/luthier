# Synthesis of Luthier's ideas, rules and principles: the night's plan

2026-10-09. Written for the session that carries it out (any model, after a loss of context) and for
Luciano to read in the morning. Approved by Luciano: "SI apruebo todo el plan escribilo por si te
quedas sin memoria e implementalo durante toda la noche, te doy libertad de correr scripts."
(chat:8c2cb06b:2902; D-2026-10-09-e). That authorization covers running the scripts that process the
record, which the working rules otherwise leave to him, for this plan only.

## What it produces

One document for Luciano, `record/synthesis/<date>_synthesis.md`, in three parts:

1. **The map of ideas.** The 725 lineages of `record/ideas/lineages_link_ideas_v1_claude-code_opus.json`
   grouped into themes, each idea with its state (seedling: developed; latent seed: powerful, not
   developed; open tension: a fork left unresolved; the classes of `consolidate_ideas_v1`, May), who
   said it first and when.
2. **The candidate principles.** What `find_principles_v2` (blind) proposes from the lineages, set
   against P1 to P14 by `match_principles_v1`, each with a `Mark:` line for him.
3. **The rules.** The normative statements of the specification (`docs/spec/`) and the entries of
   `record/decisions.md`, each traced, where the trace exists, to the lineages it comes from.

Then, second, the validation with a cutoff (section "Part B").

## Rules for the night

- Commit before every change; small commits; results and infrastructure in separate commits.
- Every model call isolated (no tools, no session), at effort low unless said otherwise; every
  output pinned by sha256 of inputs and prompt, with the raw answers kept.
- Tests pass before any commit of code; never chain a commit after `tail`, `tee` or another command
  that hides an exit code; `scripts/check_private.py` on every output before it is committed.
- Nothing is pushed. Nothing of Luciano's is edited. No case is approved; nothing is marked for him.
- A step that fails twice the same way is stopped and written down in the progress log below, and
  the night moves to the next independent step.

## Part A. The synthesis

**A0. Pin and mine.** `iachat ingest claude-code` and `iachat ingest claude-code --from
~/.claude-databaum/projects`; `scripts/mine_decisions.py`; commit `record/validation/decision_units.*`
after the private-words lint.

**A1. Themes and states.** New prompt `prompts/consolidate_lineages_v1.md` and script
`scripts/consolidate_lineages.py`. Input: every lineage (id label, scope, statement, origin, first
seen, up to two quotes). The model groups them into themes (ecology, not taxonomy: ideas that are
understood together) and gives each its state. It sees no principle and no description of Luthier
beyond its name and designer. Checks: every lineage once, themes named, states in the three classes.
Output `record/synthesis/<date>_themes_*.json/.md`. Done when the tests pass on a stub and the run's
answer passes the checks.

**A2. Candidate principles.** `scripts/find_principles.py --var language=Luthier --var
"designers=Luciano Moffatt" --max-candidates 10`, then `scripts/match_principles.py --found <that>`.
Ten, not seven: a synthesis lists more than a sitting's marking; the number is a parameter and is
recorded (the model's choice, logged).

**A3. Rules and their sources.** New prompt `prompts/trace_rules_v1.md` and script
`scripts/trace_rules.py`. Mechanical part: the rules of the specification (the bold identifiers of
`docs/spec/*.md`, R1 to R11 in 05, G and C in 08; where a document has no identifiers, its numbered
headings) and the entries of `record/decisions.md`. Model part, one call: for each rule, the lineages
that state or motivate it, by label, or none. Checks: ids exist. Output
`record/synthesis/<date>_rules_*.json/.md`.

**A4. The document.** `scripts/assemble_synthesis.py`, mechanical: the three parts in one Markdown
document, a one-screen summary first (themes and their sizes, states, candidates, rules without a
source in the ideas), then the parts. Commit it before Luciano reads it.

## Part B. Validation with a cutoff (after A)

Luciano: a principle is "una idea organizadora que ayude a tomar decisiones". The candidates found
from his ideas up to a cutoff T are tested on his decisions after T, with the machinery of
`record/plan-principles-validation-2026-10-09-execution.md`.

**B1.** T = 2026-09-30T00:00Z (the start of Luthier version 0; 193 mined decisions after it, 76 on
the language). Lineages of the rows up to T only, in a separate state:
`scripts/link_ideas.py --timeline <rows up to T> --output-dir record/validation/cutoff`.
**B2.** `find_principles` on those lineages, blind, 10 candidates; `match_principles` against P1 to
P14, so that a candidate that restates a principle in force inherits its operative dates.
**B3.** Eligibility for the candidates: explicit = the time of the candidate's quote row; operative =
that of the principle in force it is covered by or extends, else never. Extension of
`scripts/eligible_cases.py` (`--candidates <find output> --match <match output>`), with tests.
**B4.** `scripts/draft_cases.py` on the candidates of B3 (decisions after T only).
**B5.** `scripts/review_cases.py draw`, then `exposure`, then `write`. The review document is
committed for Luciano. The night stops here: the review, and the scoring after it, are his.

## Progress log

Each step, when done, gets a line: step, commit, what came out, anything that went wrong.
- A0 done: transcripts pinned (both accounts, one new file); the units were already committed by Luciano at 656a754 (337 units, 100 with a commit, 29 reversals, 22 withheld). He is marking principle_dates.md: not touched.
- A3 done, e3ecacd: 100 rules (58 of the specification, 42 decisions), 87 traced to at least one idea. A lineage named with a private word by the linking model was scrubbed (170b25e; scripts/scrub_private.py, 64d0a5f). Part B prepared (9ea1806). A1 and A2 running; their first calls lost the connection and were retried.
- A1 done, 57958e3: 725 ideas in 33 themes; 226 seedlings, 486 latent seeds, 13 open tensions.
- A2 done, b2bdc62 and 4b88aab: 10 candidates found blind; against P1 to P14, 9 new, 1 extends P10 (the mathematical object as invariant).
- A4 done, eb7984e: record/synthesis/2026-10-09_synthesis.md (557 lines, summary first). Part A complete.
- B1 running: lineages of the 1,020 rows before 2026-09-30 with link_ideas_v2 (the prompt that does not describe Luthier; v1 states one of the candidates as a fact), in record/validation/cutoff.
- B1 done, daacc9a: 404 lineages of the 1,020 rows before the cutoff.
- B2 done, 9eba77d: 10 candidates (7 first said by Luciano); 8 new, C1 extends P14, C6 extends P10.
- B3 done: eligibility with --after the cutoff (c5fcd8e): 175 units to draft.
- B4 running: draft_cases on the 175 units, output in record/validation/cutoff.
