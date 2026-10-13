# Luthier for VS Code

Syntax colours for `.lth` and `.lut`, and parse diagnostics on open and save.
Requires Python 3.11 or later. No npm install, compilation or bundler is needed.
From the repository root, launch an Extension Development Host:

```sh
code --extensionDevelopmentPath="$PWD/tools/vscode-luthier" "$PWD"
```

Set `luthier.pythonPath` in VS Code settings if the interpreter is not `python3`.
The extension searches upward from the file's workspace folder for the repository's
`src/luthier/cli.py` and `src/luthier/lib/grammar.lth`, then runs
`python3 -m luthier.cli parse FILE` with that repository's `src` as `PYTHONPATH`.
Diagnostics describe the saved file; unsaved edits are parsed after saving.

Regenerate and check syntax from the extension directory:

```sh
python3 scripts/gen_grammar.py
python3 scripts/gen_grammar.py --check
```

Run tests from the repository root:

```sh
PYTHONPATH=src python3 -m pytest tools/vscode-luthier/tests -q
```

Source: `src/luthier/lib/grammar.lth`'s `luthierSyntax` and `precedenceLevels`,
read through `luthier.ebnf`; core names come from `src/luthier/check.py`'s
`coreNames`. The generated JSON header records both input hashes and generator
version (v1, deterministic, no seed or rendering parameters). Lexical patterns
implement `docs/spec/02-grammar.md` 2.S1, including its three string escapes.
Implementation choices: plain JavaScript and one diagnostic collection; word
operators have the `keyword.operator` scope, and core names use `support.type`.
