# Brief: floating point as Luthier's flagship case, a design in two documents

Luciano (2026-10-27, in the coordinating session), his words:
"Yo creo que el elefante en el room son los floats. No creo que Luthier necesite solucionar los
floats para ser válido. Pero cómo Luthier formule claramente el caso de los floats (que creo que no
es trivial) tiene que ser como nuestro pet project o modelo donde se ve cómo Luthier funciona. Y no
tener miedo de mostrar en qué fallamos, porque los floats son esa picazón para cualquiera que hace
simulaciones, te basás en un modelo que es difícil de razonar bien cómo falla. Y por otro lado es
probable que otros modelos más complejos también fallen en forma similar a cómo falla float. La
teoría de cómo es la relación entre las operaciones entre Reals y entre Floats y entre Reals y
Floats tiene que ser impecable y bien entendible. Posiblemente tengamos que tener otra teoría (los
Floats con error distinto de epsilon, las regiones, o quizás esos sean los floats) para poder
componer bien los errores (es decir que la teoría necesite de Floats decorados) o que la teoría se
aplique a un cálculo completo quizás y que si queremos componer dos cálculos concluidos entonces sí
necesitamos la teoría de Floats decorados."

What exists, read it first: `src/luthier/lib/numbers.lth` and numbers_model.lut (the doubles'
within-bound laws: associativity and distributivity within 3γ₂, `Moderate` and `Tame` domains,
`Doubles (F : U)` at Float64); report-bite-8.md (why 3γ₂ and not γ₂: the error was measured in
floating point); report-bite-11.md (the summing laws with 3γₙ, Higham 2002); report-C1.md (the
`Within` form, the worst ratio, the bound transformer (L, η, D, r) in core/properties/functions.lth);
report-B2.md (the error base ([0, ∞], +, ≥) in core/structures/algebraic.lth); D-2026-10-17-f,
D-2026-10-18-j, D-2026-10-25-a question 3 (L13.3, L13.4: the transformer and its composition);
L13 in record/principles-language.md; spec chapter 11 (numbers); src/luthier/rational.py (what
exact arithmetic exists); docs/concepts.md section 9. Grep before reasoning; cite what the record
settles.

Design, do not implement. Write:
1. `record/plan/floats-2026-10-27/decisions.md`, for Luciano, one screen or a little more: the
   design in plain words, and at most five questions only he can answer, each with what it implies,
   what it costs and your recommendation.
2. `record/plan/floats-2026-10-27/execution.md`, for the sessions: bites, files, acceptance
   criteria, order, model fit.

The design must state, impeccably and readably:
- The theory of the reals as a theory (an ordered field, and what more: completeness, the
  elementary functions), knowing it has no total exact model; which specimens it has and where
  each is exact (rationals exact on their domain, a float exact as a rational number).
- The relation between the reals and the floats: rounding fl : R → F and the embedding F → R; the
  standard model fl(x op y) = (x op y)(1 + δ), |δ| ≤ u, on a domain (no overflow, no underflow);
  what fails outside it (overflow, underflow, NaN, signed zero) stated as the domain's boundary,
  not hidden. Consider stating the floats' laws against an exact reference (every double is a
  rational, so the exact result of x op y is computable): say whether that makes the textbook
  bounds (γₙ, not 3γₙ) testable exactly, and what it costs.
- Forward and backward error, and the condition number, as Luthier objects; which of them a law
  states.
- The two ways of composing errors his words point to, and how they meet: a whole computation
  characterized by its bound transformer (static: (L, η, D, r), D-2026-10-25-a question 3), and
  decorated floats (dynamic: a value with its error, a midpoint and a radius, as ball arithmetic,
  Arb's model, or interval and affine arithmetic), where applying a transformer (L, η) to a ball of
  radius r gives radius L·r + η. Say when each is needed (his hypothesis: the theory applies to a
  concluded computation, and composing two concluded computations needs the decorated floats) and
  whether he is right.
- The failures shown, not hidden: cancellation, ill-conditioning, accumulation, non-associativity,
  and the cases the theory cannot bound; and his second point, that other approximate models
  (discretization, Monte Carlo, surrogates) fail in the same shape: whether the same theory
  (a specimen within a bound of an ideal, on a domain) covers them, and what changes.
- How this becomes the flagship example a scientist reads: what document or chapter, what
  example (a sum, a dot product, a Newton step, a small simulation).

Mark what is the record's, what is the literature's (cite: Higham 2002, Goldberg 1991, Muller et
al., the Arb papers, Moore for intervals), and what is yours. Write for Luciano: no em-dashes as
punctuation, no "not X but Y" constructions, every symbol defined at first use, numbered references
with their statement. Touch only record/plan/floats-2026-10-27/; other agents change code. Commit
both documents, staged by path (subject, blank line, one body line, ending with "Co-Authored-By:
Claude Fable 5.1 <noreply@anthropic.com>"). In your final message: the design in ten lines, the
questions in one line each, decisions taken on your own.
