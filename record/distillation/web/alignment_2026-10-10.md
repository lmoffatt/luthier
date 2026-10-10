# Alignment of the five web answers, 2026-10-10

Written by the session's model (Claude, Fable) for Luciano, from the five answers in this folder
(committed at 25a62c0 and later; manifest in `README.md`). The grouping of the AIs' lines into one
idea, and the match to a pipeline candidate or a principle in force, are this model's reading; the
counts and the line ids are checkable against the files. One of the five answers is also Claude's,
so the reader of this document and one contestant share a family.

References: S1 to S10 are the pipeline's candidates (found blind by find_principles_v2 on the
lineages, 2026-10-09; statements in `record/distillation/naive/reference.md`). P and F are the
principles in force and the features (`record/principles.md`; `docs/rationale/10`, section 0).

## 1. The language

Ideas found by all five:

| idea | claude | chatGPT | gemini | deepseek | grok | matches |
|---|---|---|---|---|---|---|
| Types are propositions; membership is a guarantee | L1 | L1 | L2 | L1 | L1 | S1 |
| Defining a function defines its test (pre/postconditions) | L2 | L2 | L5 | L2 | L2 | F2; cutoff C1 |
| Code is data; meta-recursion native; self-extensible | L8 | L8 | L1 | L3 | L5 | S2 |
| Many implementations (paths); equivalence first, then choose by cost | L7 | L6 | L4 | L4 | L3, L7 | S9 |
| Costs estimated Bayesianly from a database of measured runs | L7 | L14, L15 | L6 | L20 | L8 | S9; F5 |
| Minimal core, executable by hand; the rest libraries | L9 | L9 | L3 | L9 | L4 | S6 |
| A program is a DAG; statements commute; time from dependency | L10 | L10 | L9 | L5 | L9 | **no S**; F9 |
| Holes; declare, define, inhabit; nothing runs undefined | L11 | L10 | L11, L15 | L6 | L16 | S8; P14 |
| Forgetful functors; their choice defines the language | L12 | L16 | L7 | L7 | L6 | **no S**; cutoff C4 |
| Orchestrator of other languages; extern; agnostic | L14 | L13 | L8 | L12 | L10 | **no S**; F6, F16 |
| Certificates: graded evidence, hash over the cone | L6 | L18 | L16 | L13 | L11 | S10; F3 |
| Verification exact or statistical; type theory married to Bayes | L5, L18 | L18 | L20 | L15 | L14, L19 | S10; F8 |

Ideas found by some:

| idea | found by | matches |
|---|---|---|
| Coupled functions and types defined as one object (laws of the group) | claude L3, chatGPT L12, gemini L13, deepseek L18 | F1 |
| Execution is the verification of equivalences; declarative/executive split | claude L15, chatGPT L19, gemini L10, grok L15 | S5 |
| The certified subtype from a predicate, the fundamental construction pattern | claude L4, chatGPT L11, deepseek L10 | S3 |
| Levels of equality (`:=`, `=`, `==`, `≡`; each object its equality) | claude L16, chatGPT L7, deepseek L16 | spec 05 |
| Generators are named values, not one per type | claude L19, deepseek L14, grok L12 | F8 |
| Every criterion is a parameter, never a constant | claude L19, deepseek L17, grok L18 | **P11** |
| Expressivity over enforced robustness; failures explain themselves | claude L20, deepseek L19, gemini L12 | — |
| The ideal world realized with a precision guarantee (Real/Float64) | claude L17, chatGPT L17 | F13 |
| The law states the property that determines the operation; a second implementation is consistency | claude L13, gemini L19 | **S4; extends P10** |
| Multiple presentations, translations expressible inside | chatGPT L20, gemini L18 | — |
| A value is a type with one inhabitant | deepseek L8, gemini L14 | — |
| To express the invariances of the disciplines | grok L20 | **S7** |

## 2. The way of working

| idea | found by | matches |
|---|---|---|
| The specification on paper before the implementation | all five | — |
| A worked example before a rule enters; accept/reject `.lut` pairs | all five | — |
| Start minimal, add only what is used, reduce | all five | — |
| Concepts in `.lut`, execution delegated to Python via extern | all five | — |
| The pipeline audios, ideas, consolidation, mentor, specification | claude M8, chatGPT M2, gemini M6, deepseek M1 | — |
| Growth under pressure of the real application | claude M3, M4; chatGPT M4; gemini M3; deepseek M11 | — |
| A mechanical closing criterion per phase; rules become checks; state in files | claude M9, chatGPT M9, M11; deepseek M6; grok M3, M4, M13 | — |
| The designer remains PI; the AI in scoped, interpretable steps | claude M10, M11; chatGPT M10; deepseek M8, M9; grok M7, M17 | **P1** |
| Patches are named as patches | claude M16, chatGPT M16, gemini M14, grok M6 | — |
| Session ownership, commit discipline, tags | claude M19, chatGPT M12, deepseek M16, grok M5 | P6 |
| Negative controls; a test must fail when the thing is wrong | claude M12, chatGPT M8, deepseek M14 | — |
| Reports in concepts, the most important first; a count says nothing | claude M17, chatGPT M20, gemini M15 | **P12** |
| DOI pointers, no PDFs; repositories self-contained | claude M19, deepseek M17, grok M15 | **P7**; D-2026-10-09-a |
| Rethink the foundations repeatedly; the reasonable version, then the wild one | claude M7, chatGPT M18, grok M1 | — |
| A Python interpreter first, to validate design, not speed | claude M14, chatGPT M19, gemini M9 | — |
| Spanish in chat, English in what stays written | claude M20, chatGPT M20 | working rule |

Principles in force that no answer states: P3 (keep the original evidence and its corrections; put
the best reading in front), P4 (decisions follow guiding principles, found as the work goes), P5 (a
free choice is a legitimate principle), P8 (no more bureaucracy than it pays for), P9 (what Luciano
hasn't fully understood may come in, contained), P13 (a principle is worth the decisions it
guides). P2 (everything derived carries how it was derived) appears only obliquely, in the
certificates and in the content-addressed store (claude M18, grok M14).

## 3. What the comparison says (this model's reading)

- The consensus core, twelve ideas in five answers out of five, includes three the pipeline's ten
  left out: the program as DAG whose statements commute, the forgetful functor that defines the
  language, and Luthier as orchestrator. The pipeline's S3, S4, S5 and S7, Luciano's least repeated
  and most structural ideas, appear in at most three answers of five; S7 in one.
- The effort gradient is visible where recurrence ends: the one answer run at maximum effort
  (claude) cites twice the rows of any other and is the only one holding S3 and S4 together;
  the free runs (deepseek, grok) hold the consensus core as well as anyone.
- The method question recovers what no blind run over lineages ever found, but of the fourteen
  principles in force it reaches only P1, P6, P7, P11 and P12; the principles about evidence and
  judgment (P2, P3, P13) and about scope (P5, P8, P9) stay invisible to a naive reader of the
  ideas, perhaps because they live in the working rules and the decision log, which the timeline
  of ideas barely records.
