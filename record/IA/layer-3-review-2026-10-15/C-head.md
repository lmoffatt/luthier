# Review of layer 3 of Luthier, generators, tests and laws (round 1, bundle C)

You are reviewing theory files written in Luthier, a language whose interpreter is being rebuilt from its own theories: a type is a theory (a structure with laws), a value of it is a model, and the language certifies models against their theories by testing. A theory file (`.lth`) declares a record type of operations, states its laws as Bool-valued definitions over a model (`(m : T)`), and defines the theory as their conjunction (`T := Law1 & Law2`); a model file (`.lut`) holds values of theories. Every constructor of a `data` must have a law stating its role (principle L2.7: a definition is a concept; distinct constructors and accessors state no role). A law quantifies over the subtype it means rather than over an implication whose premise random cases rarely meet. The files parse with the project's parser; nothing yet type-checks or certifies them, so you are the first check of their meaning. Grammar, kernel and earlier layers were reviewed in earlier rounds and are not in scope. Do not reopen a decision listed under "Decisions the files cite" unless a file contradicts it; where you disagree with the specification itself, say so as a separate item.

This prompt covers generators, tests and laws (layer 3, bundle C of its external review; world, certification, demand and plan are reviewed apart and not included). `generators.lth` states generators as values (from a size and a seed, a value and the next seed), the generic ones over a type's form, sizes, subtypes, censuses and budgets, each with the theory it is a model of. `test.lth` states a test as data, what running it gives, and the grade of what it gives. `laws.lth` states what a law's value must give, the laws of relations, and a law as a theory with its evidence. `generators_model.lut` and `test_model.lut` are models. The chapters they realize are `docs/spec/07-tests.md` and `docs/spec/05-laws.md`. The material below, in this order: terms and principles L2.7, L9.6, L10, L11 and P11; the decisions the files cite; then the seven files. Frozen at commit @COMMIT@.

Cutoffs: D-2026-10-14-c says every law is a Boolean predicate and every cutoff it needs (a tolerance, a resolution, a rank floor, a convergence threshold, a level) is a parameter of the law that the demand supplies (P11), never a constant in a file.

Answer per file, numbered, quoting the line you mean, as briefly as each allows:
1. **Laws that are wrong**: false of the intended model, or unsatisfiable together.
2. **Laws that do not determine what they claim**: where a wrong model passes every law; give it.
3. **Roles (L2.7)**: a constructor of a `data` with no law of its role, or a role law that only lists constructors.
4. **The models against their theories**: a law a `*_model.lut` breaks, with the case.
5. **Against the specification**: where a file says other than its chapter or a cited decision.
6. **Implication over a type**: laws stated over a type with an implication a random case rarely meets, where the subtype should be the quantified domain.
7. **What you would change first**, one thing, with the reason.
8. **Cutoffs**: a cutoff written as a constant where it should be a parameter the demand supplies (D-2026-10-14-c, above).
9. **A missing generator**: which generator is missing for a sampled law that today runs on listed cases only (spec 7.R1 and 7.R4: a test names its generators; a law over the models of a theory is certified per model). Name the law, the type it quantifies over, and the generator it would need.

Put anything you cannot verify from the files in a final "not sure" list instead of asserting it. Do not rewrite the files.
