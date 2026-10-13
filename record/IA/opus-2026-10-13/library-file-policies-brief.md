# library.lth §4, the file policies as laws of the loader: brief for an Opus subagent

Written 2026-10-13 by Claude Fable 5.1 (session luthier-03) for the coordinating session to launch.
Scope: one section of one file, `src/luthier/lib/library.lth` §4 (its index names it, todo), and
nothing else.

## The task

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/library.lth` states the
loader as a theory (`Loader`, with its laws, in the pattern of `src/luthier/lib/ebnf.lth`: a record
type of operations, laws as Bool-valued definitions over a model `(l : Loader)`, `Loader := laws`).
Its index marks §4 todo: the file policies of spec 11.R1 to 11.R3, which D-2026-10-13-ae (in
`record/decisions.md`) takes out of the checker (`program.lth`) and makes laws of the loader, since
they need the file's kind and the library set: `primitive` is a body allowed only in core (11.R2);
`axiom` only in core and the libraries of the distribution (11.R3); `R` names no type (11.R1,
`Real` and `Float64` do). Read 11.R1 to 11.R3 in `docs/spec/11-numbers.md`, 3.S2 and 3.S39 in
`docs/spec/03-kernel.md` (the bodies `primitive "..."` and `axiom "..."` are applications of core
names), and 12.S23 in `docs/spec/12-files-and-tools.md`.

Write §4 of library.lth:
- `Loader` gains what the policies need, as fields: `isCore : String -> Bool` and
  `isLibrary : String -> Bool` on a path (core is not written yet, so which path is core and which
  are the distribution's libraries is the model's; declare nothing global).
- Three laws, each a case law over a small `FileSystem` written as data in the section (as §2's
  `sample` does), stating that `admits` refuses: a program with a `primitive` body in a file that
  is not core; a program with an `axiom` body in a file that is neither core nor a library; and
  one direction only ("such a body implies not admitted"), as `TheoryFileRejectsExtern` does. For
  11.R1, the law that a program mentioning `R` in type position is refused, read on the surface
  tree: `R` as a `name` in a declared type or in a binder's type.
- Helpers you need (`hasPrimitive`, `hasAxiom`, `mentionsR`) in the section, written like
  `hasExtern` in §1; use `grammar.lth`'s constructors (`declare`, `define`, `app`, `name`, the
  binder forms) as the file already imports them, adding to the import line what you need.
- Set §4 to done in the index; keep every other section as it is.

Check with `PYTHONPATH=src python3 -m luthier.cli parse src/luthier/lib/library.lth`; it must exit
0. Commit with an explicit path (`git add src/luthier/lib/library.lth`), one commit, message naming
11.R1 to 11.R3 and D-2026-10-13-ae, ending with the attribution line the session uses. Touch no other
file. Report in a few lines to `record/IA/opus-2026-10-13/library-file-policies-report.md`: what you
wrote, and any place where the specification did not tell you what the law should be.
