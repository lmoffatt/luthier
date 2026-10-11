# Rewriting the principles from generative ideas: the execution

Draft 0, 2026-10-11. Written for the sessions that carry it out. Status 2026-10-11 (D-2026-10-11-e):
steps 1 to 4 done in one file, `docs/principles.md` draft 2 (cd24137), derivations inline and the
P13 check in its header, on Luciano's instruction; step 5 pending; step 6 is his. The choices it rests on are in
`plan-principles-generative-2026-10-11-decisions.md` (D1 to D8); where a step depends on one it
says which, and what it assumes until Luciano answers. Inputs: `docs/principles.md` draft 1
(d6a4ff5 or later), `record/Lucianos ideas/principios organizadores.txt` (fa3f972, 1c7a284),
`record/Lucianos ideas/el problema de los floating point.txt` (5cc41fa),
`record/organizing-principles-2026-10-11.md` (66d7d48 or later), `record/decisions.md`,
`record/ideas/timeline.jsonl`.

## Rules for every step

- Commit before every change; one step, at least one commit.
- Luciano's notes are never edited; a quote is copied verbatim and checked by eye against its
  source, with the commit of the source named.
- Every derivation, formulation and move is marked *Proposed* until he marks it; his marks are
  committed verbatim before the text that incorporates them.
- No step changes `record/principles.md` (D7) or the spec.

## Step 1. The organizers (D1, D2)

Write `record/principles-generators-2026-10-11.md`: G0 to G4, each with the verbatim quote (note
or timeline id), the model's formulation of at most two lines, what type theory lacks that the
deviation supplies, and the three dependencies of the analysis (D8). Commit. Give it to Luciano:
one screen. Done when he has marked the five formulations and the marks are committed.

## Step 2. The derivations (D3, D4)

In the same file, one row per L1 to L20, W6 and the candidate L21 (identity certificates, D3):
number, organizers it derives from, the
derivation in at most two lines, the extra assumption if any, and one of: derives, needs
assumption, moves to W (D3: decided here, row by row, not in advance; L7, L17 and L14 are
expected to derive, from G0 and G2, from G1 and G3, and from G2). Sources of draft 1 are copied unchanged.

Check that closes the step: every row has a non-empty organizer field or the mark "moves to W";
the grep is

    grep -c -E "^\| L[0-9]+ .*\| (G[0-4]( G[0-4])*|moves to W) \|" record/principles-generators-2026-10-11.md

and the count equals 22. Extra assumptions are collected at the end of the file as candidates
for a further organizer or as free choices (P5).

## Step 3. The P13 check (D5)

For each organizer, list the decisions in `record/decisions.md` whose `Kind:` line names an L or
P that the organizer generates (map from step 2; P10 under G0, P14 under G2, P11 under G4 at W16).
Mechanical: grep `^Kind:` and the lines until the next field, match `L[0-9]+|P[0-9]+`. Write the
counts per organizer in the file. An organizer with zero is marked "candidate". Commit.

## Step 4. Draft 2 of docs/principles.md

Assemble: header with provenance (draft 1 commit, generators file commit, this plan, his marks);
the five organizers with quotes; the dependencies (D8); the consequences grouped by organizer, L
numbers kept with tags (D4), sources unchanged; the way of working with W15 to W17 added (D3) and
W5 restated as bootstrapping (D-2026-10-11-d); two lines on G3's justification pointing to the
rationale (D6). Commit. Check: every L of draft 1 appears exactly once in draft 2, by

    for n in $(seq 1 20); do grep -c "^\*\*L$n\." docs/principles.md; done

each printing 1.

## Step 5. The rationale of cost-valued laws (D6)

Write `docs/rationale/cost-valued-laws.md` draft 0 from analysis §4 and addendum 2, with its
sources: his notes of 2026-05-29 (`note:2026-05-29T14.14.08:matrimonio-hott-bayes`), the critique
(`dialogue:c886516d:critica-hott-bayes-sin-articular`) and its three questions answered one by
one, prior art cluster G (`record/prior-art-2026-10-09/reports/G-cost-valued-laws.md`), the two
notes of today. State the orientation once (0 = true). Mark as open: whether a cost is a −log p
or a distance, and how the uncertainty of a cost is represented in a certificate. Commit.

## Step 6. Luciano marks draft 2

Commit draft 2 before he annotates; commit his annotations verbatim; incorporate; draft 3. Log
in `record/decisions.md` what he decides on D1 to D8 as D-2026-10-11-e onward, one entry per
decision that is not routine.

## What is not done here

No change to `CLAUDE.md` (its principles in force are P1 to P13, unchanged). No change to the
validation experiment of 2026-10-09; its cases cite L numbers, which D4 keeps valid.
