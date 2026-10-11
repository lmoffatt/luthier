# Third round: counterexamples against three rules of draft 6

2026-10-11, late night. Luciano changed the prompt on the model's suggestion: no more lists of
contradictions; break three rules with worked examples on paper, give the verdict step by step and
the one-line fix, rank by how early it bites sonolocalización on floats. The three rules: L10
(draft 5, substitution along certified equivalences), L19 (draft 6, the identity of a result), L14
(draft 5, proposed, an extern with no laws). Responses in `record/IA/principles round 3/`
(d824b21): chatGPT, DeepSeek, Gemini, Grok; Claude and Kimi pending. The document they read was
draft 6 under the name `principles_2.md`. Written by Claude; the counterexamples are theirs.

## 1. The three rules broke, and the four agree on how

All four break all three. The fixes converge, which is what W2 (no rule enters without a worked
example) predicts and the three earlier rounds never produced.

**L10 broke in two ways.**

- *Scope.* A sampled identity certificate says nothing about inputs outside the distribution it
  sampled, and L10's admissibility rule never asks whether the current input is covered. chatGPT:
  an FFT extern certified on even-length traces, demanded on a prime-length one, 16 µs off under a
  1 µs tolerance. DeepSeek and Grok: two sampled links of distance 0 on their samples, chained,
  wrong by ulps on a fresh input. Draft 5 already said the sum of sampled links is an estimate, not
  a bound, and then let the planner use the estimate.
- *Sensitivity.* Gemini: a swap certified at 1e-5 feeds a subtraction of close floats and the
  demanded tolerance of 1.0 on the output is violated by a hundredfold; the local distance must be
  pulled back through the condition number of the cone between the node and the demand, which the
  rationale §5 has and L10 did not use.

Fix, taken in draft 7 (mine, reversible): a sampled edge is admissible only on inputs its
distribution covers and only as a direct edge, never summed into a path, until a probabilistic bound
exists as a law (G4: the chain becomes allowed when its law does); the tolerance charged at a node
is the demand's pulled back through the sensitivity of the cone from the node to the demand (`11`
§5), and where no sensitivity is known there is no substitution.

**L19 broke the same way for all four.** Same code, inputs, mode, type, tolerance, model, seed and
plan; the host library or the platform changed between runs (OpenBLAS to MKL, SciPy 1.10 to 1.12,
x86 to arm). Draft 6 bound version and platform into the extern's certificate and left the
certificate out of the result's identity, so the memo serves the old result. chatGPT's fix is the
cleanest: the identity of a result includes the hashes of the certificates in its live cone. Taken
in draft 7 (mine).

**L14 broke the same way for all four, and the pending proposal was wrong.** An extern with no
laws, admitted by the identity law alone, provides the scientific value without any description
having been checked: chatGPT's `delay` returning the strongest arrival where the concept meant the
first; DeepSeek's `sin_fast` that is zero beyond the sampled interval; Gemini's LAPACK solver that
crashes on the singular matrix the native handled; Grok's speed of sound with the wrong physical
model. The draft 5 sentence "admits a specimen and never certifies the description, so G2 is not
bypassed" was right epistemically and wrong executively (chatGPT's distinction): the undescribed
specimen still delivered the value. The fix all four give: an extern with no laws runs where it is
named, as a specimen, and neither it nor the native enters the planner's graph for the function
until at least one non-identity law of the type is certified against it. The proposal pending his
mark is amended to that in draft 7; it remains his to mark.

**Ranking.** Three of four put L14 first (the first extern of the application arrives with zero
laws), Gemini puts L10 first (TDOA subtracts close floats from day one). L19 bites when the memo
across runs exists, which is still pending.

## 2. What this round changes in the way of working

The prompt that asks for a counterexample against a named rule produced, in one round, three
repairs that three rounds of "find contradictions" did not, and each counterexample is one
accept/reject pair away from the spec (W2). The four examples of L14 and the two of L10 are
candidates for `tests/spec/` once the planner exists; logged here so they are not lost:
`delay` first against strongest arrival (chatGPT), `sin_fast` outside the sample (DeepSeek), the
singular matrix (Gemini), the FFT on a prime length (chatGPT), the cancellation under a swap
(Gemini), the stale memo across a library version (all four).
