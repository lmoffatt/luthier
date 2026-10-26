# Brief: related work for Luthier, with verifiable citations

You are in a scratch directory with five files about Luthier, a language for scientific computing
being built by Luciano Moffatt: concepts.md (its key concepts), gpt-dialogue.md (a dialogue that
names related systems), applications-2026-10-27.md and idea-law-normal-form-2026-10-27.md (two
notes of ideas), decisions.md (a design for floating point). Read them first.

Write `related-work.md` in this directory: a review of the related work a paper or a grant on
Luthier must cite. For each system or line of work: what it does; one or two key references with
authors, year, venue and a DOI or URL you checked exists; how it resembles Luthier; how it differs;
and what Luthier could take from it. Cover at least:
- PetaBricks and algorithmic choice with accuracy;
- Herbie and Daisy (floating-point accuracy);
- Arb and ball arithmetic, interval arithmetic (Moore), affine arithmetic;
- Higham's and Goldberg's floating-point error analysis;
- F*, Dafny, Lean, Coq/Rocq (proof-oriented programming);
- QuickCheck, Hypothesis and property-based testing, including mutation testing (the closest thing
  to Luthier's "controls": a wrong model the law must refute);
- proof-carrying code and proof-carrying data;
- provenance (W3C PROV, RO-Crate, workflow provenance);
- content-addressed code (Unison, Nix, Bazel), for Luthier's cones;
- e-graphs and equality saturation (egg) and AC-normalization in term rewriting, for the
  normal-form idea;
- graded and quantitative type theories (Granule, Fuzz), for the cost algebra;
- sequential testing and confidence sequences (Wald; Howard, Ramdas et al.), for sampled evidence;
- LLM routing and model selection by cost, for the applications note;
- anything else you find closer to Luthier than these.

End with a short section: where Luthier's combination is new and where it is not, stated without
salesmanship. Every citation must be one you could verify by fetching it; mark any you could not.
Write in English, plain, no em-dashes as punctuation. Write only inside this directory.

Addition (the coordinator, after launch; include it if you read this in time): cover formal
verification of floating point: Flocq and Gappa (Coq/Rocq, Boldo and Melquiond), Harrison's HOL Light
work, Isabelle's IEEE_Floating_Point, and the current state of Float in Lean 4 and Mathlib (opaque
or modelled; any IEEE 754 formalization in Lean), checked against current sources.
