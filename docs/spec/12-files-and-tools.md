# 12. Files and tools

Chapter 12 of the specification, draft 0, 2026-10-12. Sources: `docs/spec/03-libraries.md` §1 to §4 and §6, `docs/spec/05-static-semantics.md` §7 ("As implemented" and "Added 2026-10-06"), `docs/spec/02-grammar.md` §8, all at commit 3445ad8, and `src/luthier/cli.py` (read only). Written by Claude Sonnet 5.5. It realizes L5 (the demand), L10 (the certificate) and L14 (what can be written in Luthier is).

## §1 What a file is

**12.S1. A file denotes a value of a dependent record type.** [proposed] A `.lut` file is a set of definitions with dependencies among them. It denotes a value of the record type whose fields are those definitions, each field typed by the declared type of its definition, with the laws of the definition as the refinement of the field. A file is then the same kind of object as a theory (spec 1): the signature of a library is its type, two interchangeable libraries are two models of one theory, and a library with holes is a function of its holes. The theory that states this is `lib/library.lut` (L14); it is not written yet.

**12.S2. Version 0 builds no module value.** [implemented] A module is implemented by prefixing the names of its definitions. An implementation of a theory is a model already and travels as any other value (spec 9).

## §2 Import

**12.S3. The two forms of import.** [implemented] `import "x.lut"` brings the definitions of `x.lut` into the importer's namespace; `import "x.lut" as m` reaches them as `m.f`, with no collision between files. The extension `.lut` may be omitted. In the language designed `import` is the function of 12.S22.

**12.S4. Where a file is looked for.** [implemented] Next to the importing file, then in each directory of the environment variable `LUTHIER_PATH`, then in the `lib/` directory of the interpreter's package. `core.lut` is imported implicitly, unless the command is given `--no-core`.

**12.S5. Importing twice, and cycles.** [implemented] Importing a file twice under one prefix does nothing; one file may be loaded under two prefixes. A cycle of imports is an error.

**12.S6. Name resolution inside a module.** [implemented] Inside a module `m`, the name `x` is looked up as `m.x` first, then as `x` among core and what the root imported flat. A module does not see the definitions of the file that imports it. Constructors, data types and the labels of sums named by an alias are prefixed like functions.

**12.S7. Order inside a file and between files.** [implemented] Inside a file the order of definitions is free: the file is read whole and checked object by object (spec 4). Between files order matters in the one sense import allows, a file sees what it imports.

**12.R1. A `.bib` file imports as a module of references.** [implemented] Importing a `.bib` file gives one `Reference` value per entry, named by its key (the `Reference` theory is `lib/reference.lut`), and `cite name key checked who` accepts only such a value as its reference. This is how a grade `proved` by citation reaches a program (D-2026-10-11-f, spec 6).
Files: cite_proved.accept.lut, cite_not_reference.reject.lut.

## §3 Declaration in one file, definition in another

**12.S8. A declared value may be defined elsewhere.** [implemented] A file may declare a value with its laws in its type, and another file may give it a body. The type of the definition, if written, must agree with the declaration; if omitted, it is inherited. The laws of the declared type become obligations of the definition, so a specification has as many implementations as files that fill it, all measured against the same laws. A declared type may likewise be defined by its laws in another file. The rules that forbid a definition using a type no file defined, and an extern that gives a type, belong to spec 4 and are not restated here.

**12.S9. The pattern of a library.** [proposed] A library with a faster implementation in the host comes as two files. The pure file defines its types natively, gives a native definition of each operation, declares as holes the operations the host computes faster, and states the laws. The `_python` file fills those holes with externs (L11), supplies the generators (spec 7) and has each extern certified against the native definition or the laws of its theory. The pattern is what the libraries do today; stating it as a rule of the language is the proposal, since no program can be accepted or rejected by it.

## §4 What travels with a file

**12.S10. What `luthier test x.lut` writes.** [implemented] The file `x.cert.json`. For each definition it holds the entries of the laws run, and the hash of the definition's dependency cone: the definition and everything it refers to, transitively, with module prefixes removed and bound variables renamed canonically. The fields of an entry and its identity are spec 6 (L10.1, L10.4); this chapter assumes only that an entry carries a hash and an outcome.

**12.S11. What an importer reads.** [implemented] When a file is imported its certificate is read. An entry is accepted unchanged, with no new check, if it passed and its hash equals the current hash of the cone; the definition is then certified and `test` does not run it again unless `--deep` is given. An entry whose hash differs is stale and its obligation is pending again. The hash also covers the host code behind each extern and the interpreter, so a change in either makes the entry stale (spec 6).

**12.S12. Obligations of the importer.** [implemented] Laws of the importer that mention imported functions are obligations of the importer and always run. `luthier test x.lut --name m.f --deep` runs an imported definition and writes into the certificate of its own file; this certifies an obligation whose generator lives in another file. `--imports` runs every imported obligation that has no entry yet and writes each into its own file's certificate.

**12.S13. A pinned interpreter.** [implemented] When a `luthier.lock` is found in the directory of the program or the one above, every command that loads a program warns on standard error if the running interpreter is not the pinned commit; `run` records the lock and whether it agrees.

## §5 The commands

**12.S14. `luthier check files`.** [implemented] Parses and checks the files and prints the count of definitions, of those with laws, of those certified, pending, and provisional. With `-v` it also lists the axioms (assumed names and what they assert), the citations with their reference and checker, the provisional externs with what they build on, and for each name with laws its certificate state: certified, failed or not run in its last test, stale with the part that changed, or pending. Option `--no-core` as in 12.S4.

**12.S15. `luthier test files`.** [implemented] Runs the laws of the definitions the test directives name, or those of `--name`, and writes the certificate (`--no-cert` omits it). Options: `--n` sampled cases per law, `--exhaustive`, `--seed`, `--size` for the largest generated value, `--deep`, `--imports`, `--show-cases`, `--fuel`. A command-line count or mode overrides the directive's. The directive's own grammar and the generators are spec 7. A test whose cone contains a provisional extern records that and is never certified (spec 4). Testing is an action that demands certificates and no value (L5.5).

**12.S16. `luthier certify files`.** [implemented] Runs the test directives of several files, each in its own process, `--jobs` at a time, with `--seed` and `--imports` passed to each.

**12.S17. `run` refuses a cone that is not certified.** [decided D-2026-10-12-y] `luthier run files` evaluates `main`, or `--entry`, and refuses to start when any name in the dependency cone of the entry is uncertified or provisional, listing each with its state. Certification is the default (L10.6, D-2026-10-11-n), so `--require-certified` becomes the default and is retired. There is no flag that opts out; if a real case asks for one it is O3. Today the interpreter prints the states of the cone and refuses only under `--require-certified`.

**12.S18. What `run` does and records.** [implemented] Before evaluating, `run` fills holes: `--set name=value`, repeatable, gives a parameter hole of a non-function type its value, typed against the hole's type; a name that is not a hole, or a function hole, is refused, and a hole in the cone left without a value is an error that asks for `--set`. Unless `--no-record` is given, each run appends to `x.run.json` the entry, the hash of its cone, the time, the parameters, the result, the fingerprint of the cone, the interpreter's revision, the lock status, and the counts of states of the cone with the names that were not certified. `--checked` tests every value an extern returns against the refinements of its type as it crosses the bridge (L11.2); `--fuel` bounds the steps.

**12.S19. `luthier eval files term`.** [implemented] Infers the type of a term in the context of the files, evaluates it, and prints the value with its type. It records nothing and demands no certificate. [proposed] Under D-2026-10-12-y a value demanded from outside the program meets the same strictness as `run`; whether `eval` is exempt as a probe is not decided.

**12.S20. `luthier session files`.** [implemented] Reads one item per line over the loaded files: `x := t` defines once, `x <- t` binds and rebinds, a bare term is evaluated and printed with its type, an unused rebinding is reported as a note and not refused; `:items` lists the block and `:quit` ends. Each line re-evaluates the block so far, with no memo (D-2026-10-11-i). Its semantics as a block over the dataflow of the demand are spec 8; the memo between items is O8.


## §6 When a file is read

**12.S21. A file is read when a demand needs it.** [decided D-2026-10-12-ad] Per L11.7, a module is read at the first demand for one of its names: the checker meeting `la.f`, or `run` needing its value;
an import no demand reaches is never read. An extern's file is read only when `run` or `test`
reaches its node (`spec 3 §8`). `test "x.lut"` is the action that demands everything in the module:
every name, every import, every law, so it is where latent errors appear (`spec 7`). A flat import,
whose names cannot be traced to their file, is open (D-2026-10-12-ad).

**12.S22. Modules are values.** [decided D-2026-10-12-ab] `import` is a function whose value is a
module, a value of the record type of 12.S1; the form by which a module's names enter the importer's
namespace is to be specified.

## Open

Questions of `docs/principles.md` this chapter depends on:

- O3, the opt-out of certification in a demand: none at the start; 12.S17 is strict, and an opt-out flag waits for a real case.
- O8, the session block over the dataflow, and the memo between its items (12.S20).
- O11, the kernel's theory in Luthier, to which `lib/library.lut` (12.S1) belongs as the theory of files.

Carried from `docs/spec/03-libraries.md` §6, decided without an id (all of 2026-10-04):

- Modules as values (`fft : FFTLib := import "fft.lut"`) and explicit functors: [proposed], waits on 12.S1.
- Visibility: everything is public in version 0 [implemented]; a private part is [proposed] and undecided.
- The Python packages an extern depends on are declared nowhere; today the certificate's hash covers the installed package and its version (12.S11). A declared dependency is [proposed].
- Whether a file that imports a provisional definition may itself be certified: [proposed] no, since a cone with a provisional name is not certified (12.S17).
- Whether an importer may require a minimum grade of a certificate it accepts: answered by the demand's cutoff (L10.5, D-2026-10-12-h); the importer states no grade of its own.
