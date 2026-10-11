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

## 3. His correction, same night

"¿Cómo que toda función empieza con cero leyes? Eso es para definir una teoría." The premise of the
four L14 counterexamples, and of the draft 5 and 6 wording of L14, came from Claude max's second
round ("which is where D-d says every function starts"), not from D-2026-10-11-d, which says laws
accumulate and need not characterize, nothing about zero. A function with no laws is a hole of a
theory being defined (L8). So L14 stands in his words: an extern is validated against its type's
laws before it is applied and refused if it fails; W5's agreement test is in addition; substitution
is D-2026-10-11-m with the round's scope and sensitivity rules. The L14 question is closed; the
four counterexamples remain useful as spec tests for the planner, under a type with one weak law.

## 4. Kimi, added after the others (69db1e8)

Same L10 break (a sampled link used outside its support; draft 7 already has the fix). Two new
holes, both of the same shape Kimi names: the rule records the protective information and does not
make it a condition of the act.

- L19: the grade the demand states is not in the result's identity, so an exploratory run with a
  lenient grade and a calibration run demanding `sampled` share one memo entry, and the gate "serves
  every demand whose tolerance and grade it meets" is checked at issue, never at the memo hit. Fix
  taken in draft 7: the demand's grade is in the identity and the hit is re-gated.
- L14/L21: an identity certificate graded `sampled` can satisfy a demand's grade requirement, so a
  node whose laws are only `assumed` presents `sampled` evidence from a certificate that certifies
  nothing about the description. The example (laws stated, never run; an extern that pads to a
  power of two and breaks shift-invariance on long signals) survives his correction on zero laws.
  Fix taken in draft 7: an identity certificate admits a specimen and never raises a node's grade;
  the grade a demand requires is met only by certificates of the laws.

## 5. Claude, last to arrive; the round is complete

Three breaks with float arithmetic worked to the bit (ties-to-even), the only response that did.

- L10, the sharpest of the round: two `proved` links certified on a subtype (`Fin 3 -> Prob`, sums
  bounded by 3), chained, and used at an input outside the subtype (`[2^53, 1, -2^53]`); every link
  proved, the sum a bound, the cheapest representative returns 0 for 1 under a certificate that
  says proved within 2.7e-15. Draft 7's scope rule covered sampled links only; this shows the
  domain of a link matters at every grade, and that `cite` drops a theorem's hypotheses (γ_n needs
  n·u < 1, false for float32 over an hour of audio). Both taken in draft 7.
- L19: the reduction order inside a threaded BLAS flips a near-tie, so one identity holds two
  values on two machines, and L21's `Bool` identity reports an implementation change that did not
  happen. Taken: thread count and scheduling in the runtime the identity binds; an extern whose bits
  depend on scheduling has a `Cost` identity, never `Bool`. Not taken: "memoize no result an
  identical rerun fails to reproduce", which doubles every run.
- L14: a lookup table of the native's outputs on the grid passes the identity law exactly on
  G × S and is wrong off the grid (2.5 ms at 1 m cells, 25 tolerances), and `delay s s = 0` would
  have refused it. After his correction this is a rule of the planner, not of application: taken
  in L21, merged with Kimi's, the identity law admits a specimen only beside a certificate of at
  least one law of the description at the grade the demand requires.

Six models, eighteen counterexamples, four rules changed (L10, L19, L21 and, by his correction, L14
restored to his words). The prompt is kept for the next round: `record/IA/principles round 3/` holds
it in each response's head.
