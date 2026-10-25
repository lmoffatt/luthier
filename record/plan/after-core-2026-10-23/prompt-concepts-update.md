# Brief: docs/concepts.md brought up to the closed core, the derivation and the algebras

`docs/concepts.md` (draft 0, 632aa27 and after, with its PDF) was written on 2026-10-21, while the
core was being rebuilt. Since then: the core closed (tag v0.3, record/plan/core-2026-10-17/
execution.md's Status); certification's routing, witness and vetoes (report-bite-13c.md, D-2026-10-
22-a and -d: a pass and a failure are about their model, a control about the law); the derivation
of a value (L5.22, L5.23, L10.13, L11.10, L11.11, O13; D-2026-10-22-b and -c, his reading of the
exponential); the algebra audit and his answers (record/plan/audit-algebras-2026-10-22/, D-2026-
10-25-a), the evidence and error bases (report-B2.md), vacuity (report-wave-a-3.md, -3b.md).

Read `CLAUDE.md`, the current docs/concepts.md whole, and the sources above; grep before writing.
Revise the document so it says nothing false and carries the new concepts in its thread: the
names that moved since 2026-10-21; section 8 (certificate and cone) with what a pass, a failure and
a control serve; the derivation (where the Fable agent's consequences list in the derivation report
points: §8.1, §8.4, §12.4, §14, §15; record/plan/principles/derivation-2026-10-22-decisions.md and
D-2026-10-22-b's report); sections 9 and 10 with the bound transformer and the evidence and error
bases as decided; vacuity in section 6 or 7; section 15's open list (O13 in, what D-2026-10-25-a
settled out). Keep the tape example; re-check it with `/home/lmoffatt/miniconda3/bin/luthier check`
(its test program changed in A3b). Mark settled, proposed, building and yours as the document does;
cite each claim's source with its statement. Rebuild the PDF with the command at the top of the
file; no missing glyph. Touch only docs/concepts.md, docs/concepts.pdf, docs/concepts/ (another
agent writes the principles; another changes code and certifies). Never git stash, checkout or
reset files that are not yours. Small commits staged by path: subject, blank line, one body line,
ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". In your final message: what
changed by section, the gaps found, decisions taken on your own.
