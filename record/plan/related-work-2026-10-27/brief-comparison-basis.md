# Brief: the basis for comparing Luthier with its antecedents

Read plan.md (Part 1), related-work.md and concepts.md in this directory. Write
`comparison-basis.md` here: for each antecedent of related-work.md where Luthier has a counterpart
(at least: FitSpec and mutation testing against Luthier's controls; the rule of three, Clopper-Pearson,
Wald's SPRT and confidence sequences against Luthier's sampled evidence ε̂ at δ; Herbie, Daisy and
Rosa on FPBench against Luthier's floating-point bounds and bound transformers; Arb (or
python-flint) against Luthier's proposed balls; Unison's and Nix's content hashing against Luthier's
cones; AC-normalization in term rewriting and egg's e-graphs against Luthier's law normal form;
vacuity detection after Beer et al. against Luthier's `Vacuous`), state: the exact question the
comparison answers; the inputs (a public benchmark or dataset where one exists, with its URL, else
how to build the inputs); the metric; what result counts as "the same", "Luthier weaker" or
"Luthier stronger"; the tools to install (with versions, checked) and whether they run on Linux
with Python 3.12; and the effort, in hours, for one agent. Order by what a comparison would most
change in a paper's claims. Cite only what you verified; plain English, no em-dashes as punctuation.
Write only inside this directory.
