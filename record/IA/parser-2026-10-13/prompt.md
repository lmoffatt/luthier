# The parser of Luthier: brief for an external model

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 for Luciano, who sends it
to ChatGPT (step 1.2 of `record/plan-from-zero-2026-10-13-execution.md`; Z9, D-2026-10-13-r). The
reply goes to this folder as `chatgpt.md`, unedited (P3); the session reads it whole, runs the
tests, and commits the files only then.

## The prompt

You are writing the first Python specimen of a theory written in Luthier, a language in which a
type is a theory (a structure with laws), a value is a model of it, and the language certifies
models against their theories by testing. The theory is the grammar of Luthier itself:
`grammar.lth` states the surface tree as data, the grammar as a value `luthierSyntax` of the type
`Ebnf` of `ebnf.lth`, and the laws a lexer, a layout pass, a parser and a printer must satisfy
together (`Grammar`). Your code is a model of `Grammar`. There is no Luthier interpreter yet; your
parser is the first program that will read Luthier's theory files.

Attached: `grammar.lth.txt` and `ebnf.lth.txt` (the theories, the authority), `02-grammar.md`
(chapter 2 of the specification, which explains the grammar; where it and `luthierSyntax` differ,
`luthierSyntax` wins, 2.S9), `ebnf.py.txt` (already in the repository: it reads `luthierSyntax`
from `grammar.lth` and counts derivations of a token list), `test_ebnf.py.txt` (its tests, which
show how to use it), `ebnf_model.lut.txt` (a third file in Luthier, for your parser to read), and
`pyproject.toml.txt`.

### What to write

Four files, Python 3.11, standard library only, tests with pytest. The package is `luthier`, in
`src/luthier/`.

1. `src/luthier/surface.py`: the surface tree, one frozen dataclass per constructor of the `data`
   types of `grammar.lth` (`Literal`, `SurfacePattern`, `LambdaParam`, `Item`, `Surface`,
   `Binder`, `Body`, `SurfaceAct`), and one per record type (`Token`, `LexError`, `Field`,
   `Clause`, `ImportName`, `ParseError`) and per sum label (`lexed`, `lexFailed`, `parsed`,
   `parseFailed`). Naming, mechanical: a constructor or label `c` is the class `C` (first letter
   upper case: `intLit` is `IntLit`, `pApp` is `PApp`, `ifThen` is `IfThen`, `parseFailed` is
   `ParseFailed`); a record keeps its name and its field names. Each `data` type is a union alias
   of its classes, named after the type with the suffix `Data` where the type name collides with a
   class (`LiteralData`), otherwise the type's name. Fields in the order of the constructor's
   arguments. `List A` is a `tuple`, `Maybe A` is `A | None`, a pair `A * B` is a 2-tuple. So
   `define "x" [] nothing (termBody (literal (intLit 1)))` is
   `Define("x", (), None, TermBody(Literal(IntLit(1))))`.
2. `src/luthier/parse.py`: the four operations of `Grammar`, as functions:
   - `lex(text: str) -> Lexed | LexFailed`;
   - `layout(tokens: tuple[Token, ...]) -> tuple[tuple[str, str], ...]`, token views
     `(kind, text)` as `TokenView`;
   - `parse(text: str) -> Parsed | ParseFailed` (lex, then layout, then the parser);
   - `print_program(program: tuple[SurfaceAct, ...]) -> str` (`print` in the theory).
3. `src/luthier/cli.py`: `luthier parse FILE...` reads each file and prints
   `path:line:column: message` for each error, exit status 1 if any file fails, 0 otherwise;
   `--tree` prints each parsed act. Add `[project.scripts] luthier = "luthier.cli:main"` to
   `pyproject.toml` (give its full new text).
4. `tests/test_parse.py`: one test function per law in the conjunction `Grammar (d : Derives) :=
   ...` at the end of `grammar.lth`, named as the law in snake case (`test_dangling_else`), that
   transcribes the law's texts and trees literally. The general laws (`RoundTrip`, `Canonical`,
   `ParsedIsWritten`, `ParsesWhatDerives`, `ErrorsHaveLines`, `LexErrorsHaveLines`, `LayoutEnds`,
   `KindsAreTheGrammars`) are tested on every text of the case laws, on the three attached `.lth`
   and `.lut` files, and on texts generated from `luthierSyntax` with a bound on depth (pick the
   shortest alternative once the bound is reached). `ParsesWhatDerives` is checked against
   `luthier.ebnf.derives(luthier_syntax(), layout(tokens))`. One more test: the three files parse.

### Rules your code follows

- The parser accepts exactly what `luthierSyntax` derives from the laid-out tokens, and builds the
  tree the tree laws give. Write it as recursive descent with one function per nonterminal of
  `luthierSyntax`, named after it, its production in the docstring. Where your parser and
  `luthierSyntax` would disagree, `luthierSyntax` is right.
- Nothing of the grammar is listed twice. The literal set comes from
  `luthier.ebnf.lits_of(luthier_syntax())`, the binary operators from `lits_of_names` over the
  precedence levels, as `grammar.lth` derives them; no hand-written keyword or operator lists.
- Lexer (2.S1, the lexical laws): kinds `"name"`, `"number"`, `"string"`, `"literal"`, and
  `"newline"` (made by layout only). A word or symbol that is a literal of the grammar is a
  `"literal"` token of its own text; any other word is a `"name"`. Symbols by longest match over
  the symbolic literals (`:=` before `:`, `<-` before `<`). A dotted name is one name token. `--`
  starts a comment to the end of the line, so `--1` is a comment. A string token keeps its quotes
  and its escapes as written; the parser decodes `\"`, `\\`, `\n`. A number with a point or an
  exponent is a `floatLit`, otherwise an `intLit`. Lines count from 1, columns from 0.
- Layout (2.S4, and the comment above `luthierSyntax` in `grammar.lth`, which is the fuller
  statement; the layout laws pin it).
- The dangling `else` derives twice; the parser gives it to the nearest `if` (`DanglingElse`).
  Parentheses leave no trace in the tree.
- Printer: its output parses back to the same tree (`RoundTrip`) for every tree the parser can
  give. It writes a projection as `(a).b` (`a.b` would lex as one dotted name), a negation of a
  negation as `-(-a)` (`--` is a comment), strings with their escapes, a float so that it lexes as
  a float, and parentheses wherever the precedence table of 2.S8 would read the text otherwise,
  `PrintParenthesizes` among them. Beyond that, print plainly; one act per line.
- Errors carry a line (`ErrorsHaveLines`); a parse that fails gives at least one error.
- Do not change `ebnf.py`, the theory files, or the specification. Where the theory or chapter 2
  is ambiguous, silent or wrong, do not settle it silently: take the reading that keeps the laws,
  and list it in your report.

### What to return

Each file complete, in a code block preceded by its path. Then a report: every place where you had
to choose a reading of the theory or the chapter, every law your code does not satisfy and why,
and anything in `grammar.lth` you believe is wrong. If you can run Python, run the tests before
answering and say what passed.

## The files to attach

The folder `bundle/` next to this file.
