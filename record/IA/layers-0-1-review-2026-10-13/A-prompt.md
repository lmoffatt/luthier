# Prompt A: the kernel

Bundle `A/bundle/`: `principles.md` (Terms, L2, L3, L6, L14), `03-kernel.md`, `decisions-cited.md`
(the decisions the files cite), `kernel_laws.lth.txt`, `kernel_models.lut.txt`, `term.lth.txt`,
`term_model.lut.txt`.

## The prompt

(The common opening of `intro.md`.) This prompt covers the kernel: `kernel_laws.lth` states the
structures the kernel's types are (an object with its equality; terminal and initial objects; a
Boolean algebra; the free monoid and the recursion of lists; an ordered commutative semiring for
`Nat`; exponential, product and coproduct, with records and labeled sums as named products and
coproducts), and `kernel_models.lut` says which core type is which. `term.lth` states the kernel
term as data and the theories of alpha-equivalence, substitution, canonical form, reduction with
fuel, and quote/eval; `term_model.lut` is the interpreter written in Luthier. One point is pending
the designer's mark: kernel_laws §1 makes substitutivity over every function a law of the
structural equality only, an observational equality being respected by its theory's operations
(question Q5 to him); review it as written.

Answer in this order, numbered, as briefly as each allows, quoting the line you mean:
1. **Laws that are wrong**: false of the intended model, or unsatisfiable together.
2. **Laws that do not determine what they claim**: where a wrong model passes every law; give it.
3. **Roles (L2.7)**: a constructor of a `data` with no law of its role, or a role law that only
   lists constructors.
4. **The models against their theories**: a law `kernel_models.lut` or `term_model.lut` breaks,
   with the case.
5. **Reduction**: do `Beta`, `Delta`, `Iota`, `ProjOfRecord`, `Prim`, `HolesStay`, `ValuesStay`,
   `Final` state 3 §4 faithfully, and is the treatment of fuel (`agree`) sound?
6. **Against the specification**: where a file says other than chapter 3 or a cited decision.
7. **What you would change first**, one thing, with the reason.
Do not rewrite the files.
