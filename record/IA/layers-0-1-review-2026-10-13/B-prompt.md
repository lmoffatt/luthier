# Prompt B: the checker

Bundle `B/bundle/`: `principles.md`, `02-grammar.md` (2.S12, the translation table, and the
generated grammar), `04-static-semantics.md`, `decisions-cited.md`, `grammar.lth.txt` (for its
surface tree only, reviewed before), `term.lth.txt` (for the kernel term only, prompt A),
`translation.lth.txt`, `program.lth.txt`.

## The prompt

(The common opening of `intro.md`.) This prompt covers the checker. `translation.lth` states the
elaboration of the surface tree into the kernel term as a theory, one case law per row of the
table 2.S12, results compared up to alpha-equivalence. `program.lth` states the rules of chapter 4
as predicates (`violatesR1`, ...) and one generic law, `ReportsExactly`: a checker reports a
failure of a rule for a name exactly when the name violates it; it also states a typing theory and
the rules that read types.

Answer in this order, numbered, as briefly as each allows, quoting the line you mean:
1. **Rows of 2.S12 without a law**, or a law that translates other than the row says.
2. **Rules of chapter 4 misstated**: a predicate that accepts what the rule rejects or the reverse;
   give the program.
3. **The approximations**: `program.lth` reads a law as a definition at `Bool` until typing exists,
   and reports rather than rejects loose functions (4.S17). Are these sound as stated?
   And can `ReportsExactly` be met by a checker that reports nothing, because on the programs a
   random generator gives no name violates any rule, so the law is vacuous in practice (L9.6)? If
   so, what should its domain or generator be?
4. **Typing**: are the laws of `Typing` right and enough for the rules that use it (4.R6, 4.R8,
   4.R9, 4.R11)?
5. **Names**: does `namesIn` compute D(n) and B(n) of 1.S7, binders respected?
6. **What you would change first**, one thing, with the reason.
Do not rewrite the files.
