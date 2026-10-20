# Brief: two principles clauses (D-2026-10-18-i, -j) and the spec text of 4.R13 and 4.R9

Read `CLAUDE.md` first. Another agent (Codex) is editing lib/core, src/luthier, docs/spec/02 and
docs/spec/07 now: touch none of those. You edit only record/principles-language.md, its projection
docs/principles.md, and docs/spec/04-static-semantics.md.

1. In `record/principles-language.md`, after L6's last clause, as the next number, with the History
   line "2026-10-20: clause N added, proposed (D-2026-10-18-i)", exactly:
   "(His words) What was called cost is four things: the error, a value's propagated bound, the
   metric level; the uncertainty, a value as a distribution, the probabilistic level; the evidence,
   what a certificate knows with a finite budget, a bound at a confidence; and the resources, the
   budget, which scales with the bound demanded (L9.17). Error and uncertainty are data, decorations
   computed in the third plane (L5.4); a law is a Boolean claim at a bound about them, the tester
   recording the quantity and the demand collapsing it. Each is a model of one structure, a quantale,
   the base of the levels of equivalence (L3.5): error over [0, ∞] with +, uncertainty over
   distribution functions with a t-norm, evidence over [0, 1] with + or max, resources with + in
   sequence and max in parallel; and a function propagates them when it is non-expansive or
   Lipschitz (clause 8) (D-2026-10-18-i). [proposed]"
2. After L9's last clause, as the next number, with the History line "2026-10-20: clause N added,
   proposed (D-2026-10-18-j)", exactly:
   "(His words) A numerical law relates an input tolerance to an output tolerance, and that relation
   is its content: an agreement between a specimen and its definition is two laws bounded by
   theorems, the algorithm's stability at exact inputs (for a dot product, |dot(x, y) − x·y| ≤ γₙ
   Σ|xₖyₖ|) and the function's sensitivity (|(x + dx)·y − x·y| ≤ ‖dx‖‖y‖), so that the output's error
   is at most the sensitivity times the input's plus the algorithm's error. The demand fixes one
   tolerance and the law gives the other (L6.8); the certificate records the largest ratio of error
   to bound, the law holding at a ratio of at most one; and every such law states as a premise its
   range of validity, a region sampled on both sides (L9.16), since the bounds hold for small
   tolerances only (D-2026-10-18-j). [proposed]"
   Rewrap both to 100 columns. Then `python3 scripts/project_principles.py --write` and `--check`.
3. Apply to docs/spec/04-static-semantics.md the text that
   `record/plan/core-2026-10-17/report-bite-4.md` gives in its section "For the spec's agent (4.R13
   and 4.R9 ...)", keeping each item's status as the report says.

Accepted when: `--check` prints ok; `python3 scripts/check_spec.py` prints only its known finding
(03-kernel.md:190) or says what new finding your text causes and you fix it; `python -m pytest -q
tests/test_check_spec.py tests/test_project_principles.py` passes. Three commits (the record, the
projection, the spec chapter), each a subject, a blank line and one body line, ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>", staged by path; Codex cannot commit, so
never stage any other path. Final message: the hashes, the clause numbers, the checks' output.
