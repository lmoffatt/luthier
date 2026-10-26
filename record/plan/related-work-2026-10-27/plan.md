# Plan: compare what has antecedents, defend what is new

Luciano (2026-10-27), on related-work.md: "Lo que tiene antecedentes, debemos comparar nuestra
implementación y demostrar que es igual o no. Respecto a lo novedoso debemos demostrar que no es
erróneo y qué es lo que aporta, no sea cosa que no se use por alguna razón que se nos escape."

## Part 1. Antecedents: a comparison per item, by experiment where possible

For each antecedent in related-work.md: what exactly is compared, on which data, and what result
counts as "the same" or "different" (Gemini drafts this, comparison-basis.md). Candidates:
controls against FitSpec and mutation testing on the same laws; ε̂ (rule of three) against exact
Clopper-Pearson and the SPRT and confidence sequences; Higham's bounds and the bound transformer
against Herbie and Daisy on FPBench; the proposed balls against Arb (python-flint); the cone against
Unison's and Nix's hashing; the law normal form against AC-normalization and egg's e-graphs; vacuity
against Beer et al. Claude agents implement the comparisons afterwards, one bite each.

## Part 2. What is new: not wrong, what it gives, why nobody does it

For each of related-work.md's five claims of novelty (graded evidence over a domain; controls and
vacuity inside the certificate; static transformers and dynamic balls as models of one theory;
substitution only along certified identities; typed derivations across languages): a soundness
argument or an active search for a counterexample; a concrete case where it gives what existing
work does not; and the reasons it might not be used (an impossibility result, a cost, a practical
obstacle). Codex argues the case against, read-only (novelty-critique.md).
