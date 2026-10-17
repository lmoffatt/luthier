# Brief: D-2026-10-18-c into the principles record (L3 and L5)

Read `CLAUDE.md` first. Edit only `record/principles-language.md`. Add each clause after the last
clause of its principle (L3's last is L3.4, L5's last is L5.20), with the History line "2026-10-18:
clause N added, proposed (D-2026-10-18-c)". Rewrap to 100 columns; change no other word.

1. After L3.4, as L3.5:
   "(His words, on the third version) The core has three planes: the objects (`Bool`, `Int`,
   `Float`, `List`, `Map`, functions, functors and the universal constructions), each with its
   theory; the levels of equivalence, objects too, one structure enriched over a base (`Bool` with
   `and` gives an equivalence, [0, ∞] with `+` a metric, distributions with a t-norm a probabilistic
   metric; Lawvere 1973, Menger 1942), compared by refinement or by Lipschitz equivalence, order
   being the same structure without symmetry; and the computable types, models of the first two,
   certified against them. The theories of the first two planes only declare and state laws, with
   the mathematical references they are tested against; whatever computes lives in the third, and
   the second version failed by mixing them (D-2026-10-18-c). [proposed]"
2. After L5.20, as L5.21:
   "(His words) The tower of levels is cut by the demand, not by a rule of the theory: a theory is
   a finite rule between two nodes, the graph its rules generate may be infinite, and a computation
   walks only what its demand reaches, as values are computed forward on demand (clause 2), the
   parameters of each level it touches coming from the demand (clause 17). Infinity is potential, as
   Haskell implements it: no limit for whoever walks the road, and each computation comes with its
   limits (D-2026-10-18-c). [proposed]"

Then `python3 scripts/project_principles.py --write` and `--check`. Accepted when `--check` prints
ok and `git diff` touches only the two principles files and those two clauses and History lines.
Commit the record, then the projection, two-line messages (subject, blank line, body) ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"; stage by path; other agents commit at
the same time (retry on .git/index.lock). Final message: the hashes and the --check output.
