# Applications of Luthier's thesis, noted for a paper or a grant

2026-10-27. Two ideas of Luciano's, recorded as he stated them in the coordinating session
(chat:luthier-3e:0, 2026-10-27; and his dialogue with GPT, record/IA/gpt-2026-10-22/dialogo.md,
c312464). Neither is a decision; both are candidate demonstrations of the thesis that a program is a
collection of models of theories, certified, among which a demand chooses a realization.

## 1. Luthierizing a library

An agent proposes, for a scientific library Luthier does not own, the theories its functions model,
the laws they should satisfy and the wrong models that control them; Luthier's tester refutes or
certifies each proposal. Source: his dialogue with GPT (GPT's vertical C, "una librería ajena que
ustedes no controlan"), which he took up. This is where Claude would live inside Luthier, as a
feature others use, which needs an API key rather than a seat.

## 2. Choosing among language models by certified results per cost

His words: "alguien que usa API no usa una sola, usa varias y justamente ve cuál es más eficiente
(resultados / costo) para cada uso". The coordinator's reading: this is Luthier's own architecture
applied to the agents. The theory is the task (for example, "propose laws for this library that
certify"); the specimens are the models (Claude, DeepSeek, GPT, a local model); the evidence is the
fraction of a model's proposals that the tester certifies and that are neither vacuous nor trivial;
the planner chooses, per demand, the cheapest certified specimen that meets the asked quality
(the planner's identities, wave E of record/plan/audit-algebras-2026-10-22/execution.md). What
differs from existing routers, which choose by price and generic benchmarks, is that the criterion is
the certification rate measured on one's own task. The model is a parameter, never a dependency
(P11: every criterion is a parameter). Caveats noted: the verifier certifies trivial laws too
(vacuity and controls catch some of it); data jurisdiction (a provider processing in another
country may be excluded for collaborators' code); tool-use quality in long agent runs.
