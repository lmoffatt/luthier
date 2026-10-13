# Review of the first Luthier code: prompt for an external model

Written 2026-10-13 at 93eaec4 by Claude Fable 5.1 for Luciano, who sends it to several models.
The replies go to this folder, one file per model (`<model>.md`), unedited (P3), and the
integrating session answers them point by point in `reply.md`.

## The prompt

You are reviewing the first three files ever written in Luthier, a language whose interpreter is
being rebuilt from its own theories. Luthier is a language in which a type is a theory (a
structure with its laws), a value of it is a model, and the language certifies models against
their theories by testing. The three files state the grammar of Luthier itself as a theory, and
one model of a piece of it. Nothing can check them yet: no interpreter of this version exists.
They will be the pattern every later theory copies, so what is wrong in them propagates. Your
job is to find what is wrong, unclear or missing, against the documents that define the language.

Attached, in reading order:

1. `principles.md`: the principles of the language. Read its Terms, G0 to G2, and L2, L7, L8, L9,
   L12, L14. The rest as you need it.
2. `01-terms.md`, `02-grammar.md`: the notation, and the chapter of the specification that the
   grammar files state. `03-kernel.md` §1 to §3 for `data`, `04-static-semantics.md` R1 to R8 for
   what the checker will accept, `05-laws.md` for what a law is, `12-files-and-tools.md` S22 and
   S23 for imports and for theory files (`.lth`) against model files (`.lut`).
3. `ebnf.lth`: a theory of grammars in EBNF as data, with `derives` declared and determined by
   laws.
4. `ebnf_model.lut`: a model of `derives`, a backtracking recognizer.
5. `grammar.lth`: the grammar of Luthier: the surface tree as data, the EBNF of chapter 2 as a
   value (`luthierSyntax`), the theory `Grammar` (a lexer, a layout pass, a parser, a printer),
   and its laws.

Answer these, in this order, numbered, as briefly as each allows. Quote the line you mean.

1. **Conformance to the specification.** Where does a file contradict chapter 2, chapter 3 §1 to
   §3 or chapter 4 R1 to R8? Where does it add something the specification does not say, without
   marking it? (The files mark additions with "proposed" or "a question for the specification".)
2. **Conformance to the principles.** Where does a file violate a principle? Two to watch: 4.R10
   and L9.2 (a law characterizes; a definition by its implementation is a model, not a law) and
   L14 (what can be written in Luthier is written in Luthier). Is `derives` now determined by the
   laws of `ebnf.lth`, or does something still depend on the implementation in `ebnf_model.lut`?
3. **The laws of `ebnf.lth`.** Are the ten laws complete, in the sense that any two models
   satisfying them agree on `derives` for every grammar and token list? Are any of them
   redundant, inconsistent or wrong? Does `withStart` (a fresh start symbol to speak of one
   right-hand side) break anything?
4. **The laws of `grammar.lth`.** `RoundTrip`, `Canonical` and `ParsesWhatDerives` quantify over
   programs and texts; the rest are single cases. Which case laws are wrong (the two texts would
   not parse to the same tree, or the expected tree is wrong)? Which rules of chapter 2 have no
   law? Is `luthierSyntax` faithful to chapter 2's productions, and is it free of left recursion?
5. **The surface tree.** Is `Surface` (the term) complete for chapter 2? Are there forms that
   should be one constructor and are two, or the reverse? Would you carry positions in the tree,
   and if so how would `RoundTrip` survive it?
6. **Syntax of the files themselves.** Each file is written in the syntax chapter 2 decides,
   including the keywords of 2.S21 and the import form of 12.S22. Point to every line you believe
   would not parse, and why.
7. **The model file.** Is `ebnf_model.lut` a correct model of the laws? Where does it diverge
   (the files say left recursion), and is that acceptable for a certifier that tests by sampling?
8. **What you would change first.** One thing, with the reason.

Do not rewrite the files. Do not propose a different language. Where you disagree with the
specification itself, say so under 1, as a separate item, since the specification is what the
files must follow and a disagreement with it is a different kind of finding.

## The files to attach

- `docs/principles.md`
- `docs/spec/01-terms.md`
- `docs/spec/02-grammar.md`
- `docs/spec/03-kernel.md`
- `docs/spec/04-static-semantics.md`
- `docs/spec/05-laws.md`
- `docs/spec/12-files-and-tools.md`
- `src/luthier/lib/ebnf.lth`
- `src/luthier/lib/ebnf_model.lut`
- `src/luthier/lib/grammar.lth`

All at commit 93eaec4. About 2500 lines in all; `principles.md` is 770 of them.
