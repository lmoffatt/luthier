# Review of layer 3 of Luthier, the demand and the plan (round 1, bundle B)

You are reviewing theory files written in Luthier, a language whose interpreter is being rebuilt from its own theories: a type is a theory (a structure with laws), a value of it is a model, and the language certifies models against their theories by testing. A theory file (`.lth`) declares a record type of operations, states its laws as Bool-valued definitions over a model (`(m : T)`), and defines the theory as their conjunction (`T := Law1 & Law2`); a model file (`.lut`) holds values of theories. Every constructor of a `data` must have a law stating its role (principle L2.7: a definition is a concept; distinct constructors and accessors state no role). A law quantifies over the subtype it means rather than over an implication whose premise random cases rarely meet. The files parse with the project's parser; nothing yet type-checks or certifies them, so you are the first check of their meaning. Grammar, kernel and earlier layers were reviewed in earlier rounds and are not in scope. Do not reopen a decision listed under "Decisions the files cite" unless a file contradicts it; where you disagree with the specification itself, say so as a separate item.

This prompt covers the demand and the plan (layer 3, bundle B of its external review; the world and certification files, bundle A, are reviewed apart and not included, so a name imported from `certification.lth` or `test.lth` is taken as stated). `demand.lth` states the demand as a value: what an action asks of a program, the cutoffs it carries, what it passes down to each law of the cone, and what a run records of it. `plan.lth` states the plan as a value: the dataflow of a cone, a schedule that linearizes it, the live subgraph a demand reaches, the strategy as a parameter, the law `Confluent`, and the key under which a result is kept. `demand_model.lut` and `plan_model.lut` are models of them. The chapter they realize is `docs/spec/08-demand.md`. The material below, in this order: terms and principles L2.7, L9.6, L10, L11 and P11; the decisions the files cite; then the five files. Frozen at commit @COMMIT@.

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
9. **Identifying a result**: what law is missing for `run`'s record and key to identify a result (spec 8.S8 and 12.S18: the record a run writes and the key under which a result is kept; the key, its hash and the record of `demand.lth` and `plan.lth`).

Put anything you cannot verify from the files in a final "not sure" list instead of asserting it. Do not rewrite the files.
