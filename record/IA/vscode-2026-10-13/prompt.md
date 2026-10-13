# A minimal VS Code extension for Luthier: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session), launched by it with `codex exec`. S5 of
`record/plan/sonolocalizacion/plan-sonolocalizacion-2026-10-13-decisions.md` (recommended, not yet
marked; one commit undoes it).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: write only under a new directory
`tools/vscode-luthier/` and the report; touch nothing else; a failure from another file is someone
else's, report it, do not fix it.

Write the smallest VS Code extension for Luthier files (`.lth`, `.lut`) that gives (1) syntax
colours and (2) parse errors as diagnostics, with nothing listed twice: the grammar is the value
`luthierSyntax` in `src/luthier/lib/grammar.lth`, read by `luthier.ebnf.luthier_syntax()`
(`lits_of`, `cats_of`, `lits_of_names` give the literals, the categories, the operators), and the
parser is `luthier parse FILE` (`src/luthier/cli.py`, `path:line:column: message` per error, exit 1).

1. `tools/vscode-luthier/scripts/gen_grammar.py`: generates `syntaxes/luthier.tmLanguage.json`
   from `luthier_syntax()`: keywords (the literals that are words), operators (the literals of the
   precedence levels), the symbolic literals, comments `--`, strings with the escapes of 2.S1,
   numbers, names (a dotted name one token), and the names of core from `src/luthier/check.py`'s
   list if it exposes one. The file carries a header line naming the generator and the sha256 of
   `grammar.lth`, as `scripts/render_grammar.py` does for chapter 2; `--check` fails when stale.
2. `package.json`, `language-configuration.json` (brackets `( ) [ ] { }`, line comment `--`), and
   `src/extension.ts` (or plain JavaScript, no bundler): on open and on save of a Luthier file, run
   `python3 -m luthier.cli parse <file>` with `PYTHONPATH=<repo>/src` (the repository root found
   from the workspace), and show each error as a diagnostic at its line and column; clear them when
   the parse succeeds. Configuration: the path to the Python interpreter.
3. `README.md` in the extension: how to run it from source (`code --extensionDevelopmentPath`), and
   how to regenerate the grammar.
4. A test runnable without VS Code: `tools/vscode-luthier/tests/test_gen_grammar.py` (pytest), that
   the generated grammar lists every keyword and operator of `luthierSyntax` and nothing else as a
   keyword, and that `--check` passes.

Check: `python3 scripts/gen_grammar.py --check` from `tools/vscode-luthier/` and
`python3 -m pytest tools/vscode-luthier/tests -q` (with `PYTHONPATH=src` from the repository
root). Do not commit. Report in a few lines to `record/IA/vscode-2026-10-13/codex.md`.
