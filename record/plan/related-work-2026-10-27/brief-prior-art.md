# Brief: is there a project like Luthier, published or about to be?

Read concepts.md (what Luthier is), related-work.md (the related work already found) and
novelty-critique.md (a hostile review of its novelty) in this directory. Luciano (2026-10-27): the
only thing that would stop Luthier is a project that is essentially the same, already published or
about to be.

Search for such a project, beyond related-work.md: a language, library or system that joins most of
these: theories (types with laws) and their models; certification of implementations against laws
by testing with graded, persistent, composable evidence (proof, exhaustive, cases, sampled with a
confidence bound); negative controls (wrong models a law must refute) and vacuity; certificates keyed
by content hashes of what they depend on; floating-point or numerical laws stated within bounds;
demand-driven choice among certified implementations; provenance of values across languages; aimed
at scientific computing. Search recent work hardest: arXiv 2024 to 2026 (cs.PL, cs.SE, cs.MS,
cs.LO), PLDI, POPL, OOPSLA, ICFP, ECOOP, SC, JOSS and the US-RSE and SciPy conferences of 2025 and
2026, grant and project pages (NSF, ERC), GitHub. Include SciLean (Lean 4 for scientific computing),
verified numerics projects, property-based testing frameworks for scientific code, "certified
scientific software" and "executable specifications" efforts, and LLM-driven specification
synthesis for scientific libraries.

Write `prior-art.md` here: each candidate with what it is, a link you fetched, how close it is to
Luthier on each of the ingredients above (a table), and a verdict: same project, overlapping, or
distinct. End with the closest three and what Luthier would have to say about each in a paper.
Mark anything you could not verify. Plain English, no em-dashes as punctuation. Write only here.
