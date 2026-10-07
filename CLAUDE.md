# Working rules

- `docs/`, `src/`, `examples/` and `tests/` present Luthier; `record/` holds the record of its
  development: his sources, plans, decisions, audits, what preceded the specification.
- Luciano's notes, transcripts, annotations and observations are never edited. A correction keeps
  the original in git and puts the corrected version in front, with a note at its top.
- His observations on code are in `record/Lucianos observations/` here and in `Lucianos feedbacks/`
  in sonolocalización. Read the ones on a file before changing it.
- In a document you write, mark what comes from a source (cite it) and what you propose.
- Everything derived records its inputs (by commit or hash), the script or prompt with its
  version, every parameter, and the seed.
- Commit before every change. Keep commits small; name the decision in the message when there is
  one.
- A decision is yours when one commit undoes it and nothing depends on it yet. Otherwise it goes
  to Luciano as one question he can answer after reading a screen.
- Before a decision that isn't routine, say in one line which principles it touches, in which
  direction, and what it assumes.
- Raise a latent conflict between principles when what it could cost is worth his attention; don't
  nitpick.
- Log each decision that isn't yours in `record/decisions.md` when it is taken. A reversed decision
  keeps its entry, marked reversed.
- At the end of each task, list the decisions you took on your own.
- Commit a document before Luciano annotates it, then commit his annotations verbatim.
- A plan comes in two documents: the decisions for Luciano, the execution for the sessions.
- In anything Luciano reads, a numbered reference carries its statement: "P6 (every change can be
  undone)". Records (`record/decisions.md`, `record/principles.md`) may be terse.
- A mechanism with a recurring cost (per commit, per session, or on Luciano's attention) is added
  only after a real case it would have caught.
- Push only tagged milestones.
- Written material is in English; chat with Luciano is in Spanish.
- Luciano runs scripts that process data or the record of the project. Lints, luthier check and
  luthier certify you may run.

## Principles in force

- P1 Luciano's part stays discernible.
- P2 Everything derived carries how it was derived.
- P3 Keep the original evidence and its corrections; put the best reading in front.
- P4 Decisions follow guiding principles, found as the work goes, toward the objectives of the
  project.
- P5 A free choice is a legitimate principle, for Luciano and, within margins, for a model.
- P6 Every change can be undone.
- P7 Each repository is self-contained.
- P8 No more bureaucracy than it pays for.
- P9 What Luciano hasn't fully understood may come in, contained.
- P10 The mathematical object that best represents a concept is the invariant of its type.
- P11 Every criterion is a parameter, never a constant in the code.
- P12 Luciano's attention is the scarce resource; what reaches him is synthesized according to the
  objectives of the project.
- P13 A principle is worth the decisions it guides or helps interpret.
