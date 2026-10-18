# 12. Files and tools

Chapter 12 of the specification, draft 0, 2026-10-12. Sources: `docs/spec/03-libraries.md` §1 to §4 and §6, `docs/spec/05-static-semantics.md` §7 ("As implemented" and "Added 2026-10-06"), `docs/spec/02-grammar.md` §8, all at commit 3445ad8, and `src/luthier/cli.py` (read only). Written by Claude Sonnet 5.5. It realizes L5 (the demand), L10 (the certificate) and L14 (what can be written in Luthier is).

## §1 What a file is

**12.S1. A file denotes a value of a dependent record type.** [decided D-2026-10-12-ah] A `.lut` file is a set of definitions with dependencies among them. It denotes a value of the record type whose fields are those definitions, each field typed by the declared type of its definition, with the laws of the definition as the refinement of the field. A file is then the same kind of object as a theory (spec 1): the signature of a library is its type, two interchangeable libraries are two models of one theory, and a library with holes is a function of its holes. The theory that states this is `lib/library.lut` (L14); it is not written yet. [decided D-2026-10-13-ad] `src/luthier/lib/library.lth` states the loader (kinds, what a file sees, what a demand reads, the file policies of spec 11); that a file denotes a record of its definitions is not yet a law there.

**12.S2. Version 0 builds no module value.** [implemented] A module is implemented by prefixing the names of its definitions. An implementation of a theory is a model already and travels as any other value (spec 9).

## §2 Import

**12.S3. The two forms of import.** [implemented] `import "x.lut"` brings the definitions of `x.lut` into the importer's namespace; `import "x.lut" as m` reaches them as `m.f`, with no collision between files. The extension `.lut` may be omitted. In the language designed `import` is the function of 12.S22.

**12.S4. Where a file is looked for.** [implemented] Next to the importing file, then in each directory of the environment variable `LUTHIER_PATH`, then in the `lib/` directory of the interpreter's package. The core, every file under `lib/core/` (`core.lut` and the files beside it), is imported implicitly, unless the command is given `--no-core` (`luthier check` takes it, 12.S14; D-2026-10-18-b, the core's bite 5).

**12.S5. Importing twice, and cycles.** [implemented] Importing a file twice under one prefix does nothing; one file may be loaded under two prefixes. A cycle of imports is an error.

**12.S6. Name resolution inside a module.** [implemented] Inside a module `m`, the name `x` is looked up as `m.x` first, then as `x` among core and what the root imported flat. A module does not see the definitions of the file that imports it. Constructors, data types and the labels of sums named by an alias are prefixed like functions. Replaced: 12.S22.

**12.S7. Order inside a file and between files.** [implemented] Inside a file the order of definitions is free: the file is read whole and checked object by object (spec 4). Between files order matters in the one sense import allows, a file sees what it imports.

**12.R1. A `.bib` file imports as a module of references.** [implemented] Importing a `.bib` file gives one `Reference` value per entry, named by its key (the `Reference` theory is `lib/reference.lut`), and `cite name key checked who` accepts only such a value as its reference. This is how a grade `proved` by citation reaches a program (D-2026-10-11-f, spec 6).
Files: cite_proved.accept.run.lut, cite_not_reference.reject.run.lut.

## §3 Declaration in one file, definition in another

**12.S8. A declared value may be defined elsewhere.** [implemented] Retired by D-2026-10-13-o: a model is a named value of its theory, imported by name with it (12.S22), so no file fills another's hole by repeating its name. As `v0.1-final` did it: a file may declare a value with its laws in its type, and another file may give it a body. The type of the definition, if written, must agree with the declaration; if omitted, it is inherited. The laws of the declared type become obligations of the definition, so a specification has as many implementations as files that fill it, all measured against the same laws. A declared type may likewise be defined by its laws in another file. The rules that forbid a definition using a type no file defined, and an extern that gives a type, belong to spec 4 and are not restated here.

**12.S9. The pattern of a library.** [implemented] A library with a faster implementation in the host comes as two files. The pure file defines its types natively, gives a native definition of each operation, declares as holes the operations the host computes faster, and states the laws. The `_python` file fills those holes with externs (L11), supplies the generators (spec 7) and has each extern certified against the native definition or the laws of its theory. The pattern is what the libraries do today; it is a rule of the language, stated here since no program can be accepted or rejected by it.

## §4 What travels with a file

**12.S10. What `luthier test` and `luthier certify` write.** [implemented] Each entry goes into the store `y.cert.json` of the file `y` that makes the claim it certifies: the file that defines the model of the library the line's binding names, or, when it names none, the file that states the law (L10.12, D-2026-10-16-b). A test program (`x.test.lut`, 12.R2), which only gathers evidence, keeps no store; a control's entry follows the same rule. For each definition it holds the entries of the laws run, and the hash of the definition's dependency cone: the definition and everything it refers to, transitively, with module prefixes removed and bound variables renamed canonically. The fields of an entry and its identity are spec 6 (L10.1, L10.4); this chapter assumes only that an entry carries a hash and an outcome.

**12.S11. What an importer reads.** [implemented] When a file is loaded, by a run or as the claim of a test line, its store is read; a store beside a test program is read by nothing. An entry is accepted unchanged, with no new check, if it passed and its hash equals the current hash of the cone; the definition is then certified and `test` does not run it again unless `--deep` is given. An entry whose hash differs is stale and its obligation is pending again. The hash also covers the host code behind each extern and the interpreter, so a change in either makes the entry stale (spec 6). [decided D-2026-10-15-d] The reading is the host's, in Python, and no action of the program performs it: until the stores are places of the world (spec 10.S6), a store another process changes during a run is seen by no law, and the run keeps only the hash of the bytes it read (`stores_read`, 12.S18).

**12.S12. Obligations of the importer.** [implemented] Laws of the importer that mention imported functions are obligations of the importer and always run. `luthier test x.lut --name m.f --deep` runs an imported definition and writes into the certificate of its own file; this certifies an obligation whose generator lives in another file. `--imports` runs every imported obligation that has no entry yet and writes each into its own file's certificate.

**12.S13. A pinned interpreter.** [implemented] When a `luthier.lock` is found in the directory of the program or the one above, every command that loads a program warns on standard error if the running interpreter is not the pinned commit; `run` records the lock and whether it agrees. [implemented] At c03e16f `run` searches the lock in the program's directory and the one above, pins the interpreter's revision as the certifier reads it (the last tag, D-2026-10-14's night default, not a commit), warns when it differs, writes it after a successful run when absent and records the status; `check`, `test` and `eval` do not warn yet.

## §5 The commands

**12.S14. `luthier check files`.** [implemented] Parses and checks the files and prints the count of definitions, of those with laws, of those certified, pending, and provisional. With `-v` it also lists the axioms (assumed names and what they assert), the citations with their reference and checker, the provisional externs with what they build on, and for each name with laws its certificate state: certified, failed or not run in its last test, stale with the part that changed, or pending. Option `--no-core` as in 12.S4.

**12.S15. `luthier test files`.** [implemented] Takes a test program, `x.test.lut`, and refuses another kind of file (12.R2). Runs the laws of the definitions the test directives name, or those of `--name`, and writes the certificate (`--no-cert` omits it). Options: `--n` sampled cases per law, `--exhaustive`, `--seed`, `--size` for the largest generated value, `--deep`, `--imports`, `--show-cases`, `--fuel` (per case, in place of each line's fuel budget and recorded in its entry; by default the line's, test.lth's 3,000,000 unless the line gives its own, spec 7.S8). A command-line count or mode overrides the directive's. The directive's own grammar and the generators are spec 7. A test whose cone contains a provisional extern records that and is never certified (spec 4). Testing is an action that demands certificates and no value (L5.5).

**12.S16. `luthier certify files`.** [implemented] Runs the test directives of several test programs, each in its own process, `--jobs` at a time, with `--seed` and `--imports` passed to each. A file given that is not a `.test.lut` refuses the whole command before any line runs (12.R2); `--prune`, which runs nothing, rewrites the stores of whatever files it is given.

**12.S17. `run` refuses a cone that is not certified.** [implemented] `luthier run file` takes a run, `x.run.lut`, and refuses another kind of file (12.R2). It evaluates `main`, or `--main`, and refuses to start when any name in the dependency cone of the entry is uncertified or provisional, listing each with its state; a provisional one the demand names with `--accept assumed:NAME` runs as assumed (D-2026-10-16-c, spec 10.S10). Certification is the default (L10.6, D-2026-10-11-n), so `--require-certified` becomes the default and is retired. There is no flag that opts out; if a real case asks for one it is O3. Today `run` refuses by default, and `--require-certified` no longer exists.

**12.S18. What `run` does and records.** [implemented] Before evaluating, `run` fills holes: `--set name=value`, repeatable, gives a parameter hole of a non-function type its value, typed against the hole's type; a name that is not a hole, or a function hole, is refused, and a hole in the cone left without a value is an error that asks for `--set`. Each run of `x.run.lut` appends to `x.run.json`, beside it, the entry, the hash of its cone, the time, the parameters, the result, the fingerprint of the cone, the interpreter's revision, the lock status, and the counts of states of the cone with the names that were not certified. `--checked` tests every value an extern returns against the refinements of its type as it crosses the bridge (L11.2); `--fuel` bounds the steps and `--time-limit` the seconds, neither by default (D-2026-10-16-d, spec 8.S1). [decided D-2026-10-12-ah] `--no-record` is retired: a run writes its record (P2), and `eval` (12.S19) is the probe that records nothing. Today `--no-record` still exists. [implemented] The entry also holds the hash of the run's key (`key_hash`, spec 8.S8) with the seed and the certificates it is computed from, the certificate stores read by the hash of their bytes (`stores_read`), and `result_store`: whether the cone is pure, whether the run was `--fresh`, and the entry of `x.results.json` that served it or what was done with its value. A pure entry (its live cone holds no `W`) is served from `x.results.json`, beside `x.run.lut`, when that file holds its key with one value, without evaluating; standard error says so. `--fresh` executes it whatever the store holds (L5.20) and writes nothing when the value agrees; when it does not, both values are kept and the key serves no more until one is removed (D-2026-10-15-f read for results). A cone that acts always executes (D-2026-10-15-d). [implemented] A run cut by its time limit or its fuel exits 1, says why on standard error, and appends to `x.run.json` a record marked as not finished (`finished` false), with its demand, plan and certification, the steps reached and the reason (`cut`: `fuel` or `time limit`, the steps, the message) and no output; it writes nothing to `x.results.json`, is never served, and enters no breach of `determined` (the coordinator's answer to 3g's question, P2).

**12.S19. `luthier eval files term`.** [implemented] Infers the type of a term in the context of the files, evaluates it, and prints the value with its type. It records nothing and demands no certificate. [decided D-2026-10-12-ah] `eval` is exempt from the strictness of `run` (D-2026-10-12-y) as a probe, and prints the states of the cone of its term, so that what it shows is never taken for a certified result. Today it prints no states.

**12.S20. `luthier session files`.** [implemented] Reads one item per line from standard input over the files, loaded with their imports and core as `eval` loads them (12.S19; with no file, core alone): `x := t` defines once (spec 2.R3), `x <- t` binds and rebinds (spec 2.R4), a bare term is evaluated and printed with its type and the states of its cone as `eval` prints them, an unused rebinding is reported as a note and not refused (spec 2.R6); `:items` lists the block and `:quit` ends. Each line re-evaluates the block so far, with no memo (D-2026-10-11-i); a refused line leaves the block as it was. Like `eval`, it records nothing and demands no certificate. [proposed] The session has a world only with `--world`: the block is then the body of `fn (w : W)` applied to the token, an action is performed once, when its line is entered, and served from the session's log when a later line re-evaluates the block; its first application is validated as `run` validates it (spec 10.S10), served by the stores but writing no entry; and a bare term that acts is refused, since an action is an item (spec 10.S2). Its semantics as a block over the dataflow of the demand are spec 8; the memo between items is O8.


## §6 When a file is read

**12.S21. A file is read when a demand needs it.** [decided D-2026-10-12-ad] Per L11.7, a model file is read at the first demand for one of its names, the checker needing it or `run` needing its value, and a theory file whenever the checker needs its names (12.S23);
an import no demand reaches is never read. An extern's file is read only when `run` or `test`
reaches its node (`spec 3 §8`). `test "x.lut"` is the action that demands everything in the module:
every name, every import, every law, so it is where latent errors appear (`spec 7`). There is no flat
import (12.S22).

**12.S22. An import names what enters, with its theory.** [decided D-2026-10-13-n] A theory is
imported by name from a theory file, `import "linear_algebra.lth" LinearAlgebra`, and a model by name
with the theory it is a model of, `import "linear_algebra_numpy.lut" Numpy : LinearAlgebra`,
optionally `as LA`; one line may name several things of one file, `import "ebnf.lth" Ebnf Rhs
derives`, each with its theory and alias where it has them (D-2026-10-13-o). The importer is checked against the theory alone, without reading the model's
file; when a demand first needs the model (12.S21), the file is read and the checker verifies that
it defines that name as a model of that theory, an error otherwise; and the importer sees only what
the theory names, which is the private part (L6.12, L6.14). There is no import without names, no
`la := import "x.lut"` (which D-2026-10-12-ad had, retired), no import of every name and no `open`
(D-2026-10-12-ae); the file carries no name of its own. The core, `lib/core/` (`core.lut` and the
files beside it), encloses the top-level scope of every file (a scope, not a block: spec 2.S17), so
its names (`Int`, `Bool`, `List`, `compose`, `Object` and the rest) are visible unqualified; a name
with no import is local or core's (D-2026-10-18-b). A file does not define a name the core defines:
the checker and the loader refuse it, naming the core file; an import of a core name by its path is
redundant, a notice of `check -v`.

**12.S23. Theory files and model files.** [decided D-2026-10-13-n] A theory file, extension `.lth`,
holds types, declarations and laws; the checker rejects an `extern`, an action or a model value in
it, since the checker reads theory files to check and laziness rests on a theory file never
touching the world (L2.6). It may hold the definitions its laws need to be stated, and the one value
the theory is about (the grammar of Luthier in `grammar.lth`); a model of another theory
belongs to a model file (D-2026-10-13-o). A model file, `.lut`, holds models of theories, each a value or a functor
written against a theory (L6.13), with its own dependencies and its own certificate; different
models of one theory live in different files (D-2026-10-13-i, -j). What another file imports has its
theory in a `.lth`. A `main` and the `test` lines belong to neither kind: they are the demands of the executive files of 12.R2.

**12.R2. Three kinds of file, declared by the suffix.** [implemented] A file is a theory (`.lth`,
12.S23), a model or library (`.lut`), or an executive file: one that holds a demand and its entry,
and that no file imports. A run, `x.run.lut`, holds the entry `main`, which `luthier run` gives the
world's token under the run's modes (12.S17, 12.S18), and a test program, `x.test.lut`, holds the `test`
lines that `luthier certify` and `luthier test` run (12.S15, 12.S16; spec 7.S21). The suffix
names the kind, and what the file holds must agree with it. The checker refuses an import of an executive file,
from any file; a `test` line, or a definition of `main`, in a `.lut` or a `.lth`; a `.run.lut`
without `main`; and a `.test.lut` without `test` lines. Each refusal names the file, its kind and
the rule (`check.py`'s `kinds`). The loader refuses the import too, when a run or a test reads it,
so an executive file is never loaded under another (`run.py`'s `executive_import`); `run` takes
only a `.run.lut` and `certify` and `test` only a `.test.lut`, each refusing another kind with the
suffix it wants (`require_kind`). Demands typed at the terminal (`eval`, `session`) are executive
without a file and read any file, recording nothing (12.S19, 12.S20). [proposed] Each executive
file carries only the demand its suffix names: a `test` line in a run and a `main` in a test
program are refused as well. Source: D-2026-10-16-e, L2.6, L5.1.
Files: kind_run.accept.run.lut, kind_test.accept.test.lut, kind_model.accept.lut, kind_main_in_model.reject.lut, kind_test_in_model.reject.lut, kind_test_in_theory.reject.lth, kind_main_in_theory.reject.lth, kind_run_without_main.reject.run.lut, kind_test_without_lines.reject.test.lut, kind_import_run.reject.lut, kind_import_test.reject.test.lut, kind_test_in_run.reject.run.lut, kind_main_in_test.reject.test.lut.

**12.S24. What an executive file keeps beside it.** [implemented] An executive file may define names
of its own (helpers, censuses, bindings), which no other file sees, since none imports it. What two
executive files share, such as the cases of a law and of its controls, lives in a library they both
import (`tests/tester/plot_cases.lut`, `fit_cutoffs.lut`). The records of a run live beside it:
`x.run.json` and `x.results.json` beside `x.run.lut`, the name of the file without the suffix of its
kind (`run.py`'s `base_name`). [implemented] Those of the `.run.lut` files under `examples/` are
tracked in git and those under `tests/` ignored (`.gitignore`, D-2026-10-16-h item 8). Certificates never live beside an executive file: each entry is written
where 12.S10 puts it, beside the claim (L10.12). [proposed] A law a test program states
itself, with no model of a library in its binding, has the test program as its claim, and its store
is `x.test.cert.json` beside it; only the fixtures of the test suite do this today.

## Open

Questions of `docs/principles.md` this chapter depends on:

- O3, the opt-out of certification in a demand: none at the start; 12.S17 is strict, and an opt-out flag waits for a real case.
- O8, the session block over the dataflow, and the memo between its items (12.S20).
- O11, the kernel's theory in Luthier, to which `lib/library.lut` (12.S1) belongs as the theory of files.

Carried from `docs/spec/03-libraries.md` §6, decided without an id (all of 2026-10-04):

- Modules as values (`fft : FFTLib := import "fft.lut"`): decided since, D-2026-10-12-ad and -af (12.S22). Explicit functors: [proposed], waits on 12.S1.
- Visibility: everything is public in version 0 [implemented]; a private part is [proposed] by ascription to a theory (D-2026-10-13-c, L6.12).
- The Python packages an extern depends on are declared nowhere; today the certificate's hash covers the installed package and its version (12.S11). A declared dependency is [proposed].
- Whether a file that imports a provisional definition may itself be certified: [proposed] no, since a cone with a provisional name is not certified (12.S17).
- Whether an importer may require a minimum grade of a certificate it accepts: answered by the demand's cutoff (L10.5, D-2026-10-12-h); the importer states no grade of its own.
