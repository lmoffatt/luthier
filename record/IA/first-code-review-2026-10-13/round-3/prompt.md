# Review of the first Luthier code, round 3: prompt for an external model

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 for Luciano, who sends
it to the same four models. The replies go to this folder, one file per model (`<model>.md`),
unedited (P3).

## The prompt

This is the third round of a review you took part in. In the first two rounds four models reviewed
the first three files written in Luthier, a language whose interpreter is being rebuilt from its
own theories: a type is a theory (a structure with its laws), a value of it is a model, and the
language certifies models against their theories by testing. The files state the grammar of
Luthier itself as a theory, and one model of a piece of it. Nothing can check them yet.

Since round 2 the language's designer decided the rules your findings raised, the specification and
the principles were changed accordingly, and the three files were rewritten. `reply.md` says what
was done with each finding of round 2, including what was not taken and why. Your job now
is to check the rewrite, not to repeat the earlier rounds.

Attached, in reading order:

1. `reply.md`: what was done with each finding of round 2.
2. `principles.md` (Terms, G0 to G2, L2, L6, L7, L8, L9, L12, L14), and the specification:
   `01-terms.md`, `02-grammar.md`, `03-kernel.md` §1 to §3, `04-static-semantics.md` R1 to R8,
   `05-laws.md`, `12-files-and-tools.md` S22 and S23. They changed since round 2.
3. `ebnf.lth`, `ebnf_model.lut`, `grammar.lth`: the rewritten files.

Answer these, in this order, numbered, as briefly as each allows. Quote the line you mean.

1. **Was each finding fixed?** For each item under "fixed" in `reply.md`, say whether the rewrite
   does what it claims. Name only the ones it does not, with the line.
2. **The uniqueness argument of `ebnf.lth`.** On `WellFormedEbnf`, with `RepRounds`, do the nine
   laws have exactly one solution? Is the well-founded order the file describes correct? Do the
   definitions `nullable`, `leftCalls` and `reachesLeft` compute what they claim, and are their
   bounds (`ruleCount`) enough? Is `WellFormedEbnf` the right domain, or too strict or too loose?
3. **`luthierSyntax`.** Is it a `WellFormedEbnf` (no left recursion, every nonterminal defined)?
   Is it faithful to chapter 2 as it now reads? Are there texts with two trees left (two
   productions deriving the same token list into different trees)? Does `argAtom` against `atom`
   do what 2.S10 asks?
4. **The new laws of `grammar.lth`.** `wellFormed` and `WrittenProgram`, the lexical laws, the
   layout laws, the tree laws. Which are wrong? Which forms or rules still have no law? Is
   `wellFormed` exactly the set of trees a text gives (so that `RoundTrip` and `ParsedIsWritten`
   hold together), or does it admit trees no text gives or reject trees some text gives?
5. **Meaning of the constructors.** The designer's rule is now L2.7: a definition is a concept, and
   a collection of types is not; each constructor of a `data` needs a law stating its role, and an
   observer that only lists constructors does not count. `Keyword`, `Op` and `TokenKind` were
   removed and derived from the grammar. Does each `data` left have a law of each constructor's
   role? Is the derivation of reserved words, operators and token kinds from `luthierSyntax` sound?
6. **The precedence table** of 2.S8 and its realization in `luthierSyntax` (`term`, `openForm`):
   is it clear, is the grammar now unambiguous except for the dangling `else`, and does
   `endsInOpenIf` settle that one exactly?
7. **Syntax of the files.** Every line you believe would not parse under chapter 2 as it now reads.
8. **What you would change first**, one thing, with the reason.

Do not rewrite the files. Do not reopen what `reply.md` lists as not taken unless the rewrite made
it worse. Where you disagree with the specification itself, say so as a separate item.

## The files to attach

The folder `bundle/` next to this file: `reply.md` (round 2), `principles.md`, `01-terms.md`,
`02-grammar.md`, `03-kernel.md`, `04-static-semantics.md`, `05-laws.md`, `12-files-and-tools.md`,
`ebnf.lth.txt`, `ebnf_model.lut.txt`, `grammar.lth.txt` (the three files, as text so they upload).
