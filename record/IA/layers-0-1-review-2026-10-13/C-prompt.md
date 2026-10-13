# Prompt C: laws, checks and the library

Bundle `C/bundle/`: `principles.md`, `05-laws.md`, `12-files-and-tools.md`, `decisions-cited.md`,
`laws.lth.txt`, `checks.lth.txt`, `checks_model.lut.txt`, `library.lth.txt`.

## The prompt

(The common opening of `intro.md`.) This prompt covers three small theories. `laws.lth` states
what a law's value must give (a verdict in a cost `C`, with `lift` and `exact`), templates of the
laws of relations, and a law as a theory: its forms (`Case`, `Forall`, `Exists`, the connectives),
its evidence, and what each kind of evidence settles. `checks.lth` states a check written once in
the form that explains its failures, and its projections. `library.lth` states the loader: file
kinds, what a file sees through its imports, what a demand reads.

Answer in this order, numbered, as briefly as each allows, quoting the line you mean:
1. **Laws that are wrong or unsatisfiable together.**
2. **Evidence**: does `Settling` say what D-2026-10-13-l says (a `forall` refuted exactly by a
   counterexample and confirmed over an infinite domain only statistically; an `exists` confirmed
   by a witness; `then` material; a citation models a law whole)? What is missing?
3. **Checks**: do the projections and `both`/`either` state 5.S9 and 5.S11?
4. **The library**: do the laws state 12.S21 to 12.S23 and the privacy by ascription of L6.12?
   What a loader could do wrong and still pass?
5. **Roles (L2.7)** in `Law`, `Evidence`, `Verdict`, `Reason`, `FileKind`.
6. **What you would change first**, one thing, with the reason.
Do not rewrite the files.
