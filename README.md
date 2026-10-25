# Luthier

A language that verifies models of theories. A theory is a type together with its laws. A model is
a value of that type, a claim that its operations satisfy the laws, and declaring a model declares
its tests. What runs is decided by a demand from outside, which asks for a value, a test or a
program run. Version 0 tests; it does not prove.

The interpreter is at the tag `v0.3` (`git tag`): the core of the language is written in Luthier
and loaded before every file as a prelude, so its names are visible without an import. The
interpreter is a Python package (3.11 or later) that imports numpy (`tester.py`, `run.py`); `pyproject.toml` declares no dependency, so install numpy yourself. What exists, what is decided and what is only
proposed is marked clause by clause in the specification (`docs/spec/`); where this page and the
specification differ, the specification holds.

## Where to start

- `docs/concepts.md` (draft 1, awaiting Luciano's annotations): the key concepts and the logic that
  joins them, written around one small example, a tape measure. Its four files are in
  `docs/concepts/`. Start here.
- `docs/guide/00-fundamental-elements.md`: the few ideas a program is made of, one program executed
  by hand and one read through.
- `docs/principles-for-readers.md` (draft 7, unapproved): the ideas behind Luthier in prose, with
  no apparatus.
- `docs/spec/00-index.md`: the specification, twelve chapters; each rule carries its status
  (implemented, decided or proposed) and its accept and reject programs in `tests/spec/`.
- `docs/principles.md`: the principles the specification realizes, for the people writing it.

## An example

The theory of a tape measure, from `docs/concepts/tape.lth`. A mark on a fifty-metre tape is an
integer number of millimetres from its zero, and a tape is a way of reading the distance between
two marks. Each law is a predicate over a model of the theory, and the theory is the conjunction of
its laws (a shortened excerpt):

```
Mark : U := { k : Int | 0 <= k and k <= 50000 }
Tape : { reading : Mark -> Mark -> Float64 }

ReadingSymmetric (t : Tape) (a b : Mark) : Bool := t.reading a b == t.reading b a
InOrder : U := { a b c : Mark | a <= b and b <= c }
ReadingAdds (t : Tape) (p : InOrder) : Bool := t.reading p.a p.c == t.reading p.a p.b + t.reading p.b p.c
Step : U := { k : Mark | k < 50000 }
ReadingSteps (t : Tape) (a : Step) : Bool := t.reading a (a + 1) == 1.0

Tape (t : Tape) := ReadingSymmetric t & ReadingAdds t & ReadingSteps t & MetresWithin t
```

The first line of `Tape` declares it as a record of operations, with no body. The last line gives
it one: the records for which the four laws hold. A model, in its own file (`tape.lut`), is a value
of the theory:

```
tape : Tape := { reading := fn a b { toFloat64 (if a <= b then b - a else a - b) } }
```

A test program (`tape.test.lut`) is the demand that checks the claim. It names the law, a mode, the
number of cases, the seed and where each argument comes from. `luthier test docs/concepts/tape.test.lut`
printed, among other lines (the store already held these entries, so they are marked known):

```
Tape: conjunction of 4, 800 cases, sampled (known)
  conjunct ReadingSymmetric t: sampled (seed 20261021, size 50000, placement ignored), 200 cases, sampled (known, ...)
  conjunct MetresWithin t: sampled (seed 20261021, size 50000, placement ignored), 200 cases, sampled, worst ratio 0.414938 (known, ...)
control of Tape: sampled (seed 20261021, size 50000, placement ignored), 400 cases, refuted at ReadingAdds t: t = hooked, p = { a := 36254, b := 41964, c := 44418 }: the control passed (known, ...)
```

A law that passes proves nothing if it could not fail, so each test line can be repeated with a
model broken on purpose, a control, which the law must refute. Here `hooked` is a tape whose hook
adds one millimetre to every reading, and `ReadingAdds` refutes it with a counterexample.

## What a program is made of

- A program is a set of declarations (`x : T`), definitions (`x : T := t`) and aliases (`x = t`),
  in any order. The order of the text carries no meaning; the dependencies among the names are the
  only order (L4.1, time is rebuilt from the dependencies, never from the text).
- A type with laws is a theory, and a value of it is a model. A declaration with no body is a hole:
  a name with a type, no value yet. A hole of a plain type such as `String` or `Float64` is a
  parameter, which `luthier run --set` fills.
- A file has one of three kinds, declared by its suffix (spec 12.R2): a theory `.lth` (types,
  declarations and laws, never an action or a model value), a model or library `.lut` (definitions
  that claim a theory), and an executive file, which holds a demand and is never imported: a run
  `x.run.lut` with its `main`, or a test program `x.test.lut` with its `test` lines. An import names
  what enters with its theory, `import "world_model.lut" HostConsole host : HostConsole`, and the
  importer sees the model only through that theory.
- The names of the core resolve by the type of their arguments: `d` or `+` means the operation of
  the model that the type names (spec 4.R13).
- The world is a token `W` that an action takes and gives back, so that the order of actions is an
  edge of the dependency graph (spec 10). `examples/hello.run.lut` is the first program with an
  action.

## Install and run

```
pip install -e .
luthier check docs/concepts/tape.lut              # parse and check; -v lists certified, stale, pending
luthier test docs/concepts/tape.test.lut          # run the test lines of one test program
luthier certify docs/concepts/tape.test.lut       # the same for several programs, each in its own process
luthier run examples/hello.run.lut                # evaluate main against the world
luthier eval docs/concepts/tape.lut "tape.reading 1200 3450"
luthier session docs/concepts/tape.lut            # one item per line from standard input
pytest
```

Each command has `--help`. The options that matter most:

- `check [-v] [--no-core] files`: parses and checks; `-v` lists each name's certificate state;
  `--no-core` reads the files without the prelude.
- `test file` and `certify files`: `--seed SEED` replaces each line's seed, `--fuel FUEL` bounds the
  reduction steps per case, `--deep` runs again a line whose outcome the store knows, `--no-cert`
  neither reads nor writes the store. `certify` also takes `--jobs JOBS` (files run at a time) and
  `--prune` (rewrite the stores bounded, running nothing).
- `run file`: `--set NAME=VALUE` fills a parameter hole of type `String`, `Int`, `Float64` or
  `Bool`; `--main MAIN` names another entry; `--fuel` and `--time-limit SECONDS` cut the run;
  `--accept GRADE` sets the weakest grade (`proved`, `exhaustive`, `cases`, `sampled`, `assumed`)
  a certificate may have to serve the run, and `--accept assumed:NAME` runs the provisional extern
  or the refuted law `NAME` as assumed; `--bound RATIO` caps the worst ratio of error to bound that
  a numerical law's certificate may have; `--combine {weakest,strongest}` says how a law's grades
  combine over its regions; `--checked` tests each value an extern returns against its declared
  type; `--fresh` executes even when the results store holds the run's key; `--strategy
  {forward-on-demand,call-by-need}` asks for an evaluation strategy. `--accept` defaulting to
  `sampled`, and `--combine`, are marked proposed in the help text.
- `eval files term` and `session [--world] [files]`: probes that record nothing and demand no
  certificate; `--world` is proposed.

`luthier run` refuses to start when a name in the cone of `main` is not certified (spec 12.S17,
certification is the default). It appends each run to `x.run.json` beside the file. The entries of
a certificate go to `y.cert.json` beside the file `y` that makes the claim (spec 12.S10); a store
is accepted by the hash of the definition's dependency cone, so what has not changed is not run
again unless `--deep`. A run also writes `luthier.lock`, which pins the interpreter's version
(spec 12.S13).

## Layout

- `src/luthier/`: the interpreter and the host functions it calls. `parse.py` (lexer and parser),
  `elaborate.py` (elaboration and typing for resolution), `kernel.py` (reduction), `check.py` (the
  static rules), `tester.py` (`luthier test`), `certify.py` (the hash of a cone, the store,
  `luthier certify`), `run.py` (`luthier run`), `host.py` (the world's actions), `generators.py`,
  `cli.py`; `arrays.py`, `tables.py`, `rational.py`, `lm.py` and `plots.py` are the Python behind
  libraries.
- `src/luthier/lib/core/`: the prelude. `core.lut` holds the primitive data and operations (`Unit`,
  `Empty`, `Bool`, `Int`, `Float64`, `String`, `Maybe`, `Nat` and the rest) and claims, for each,
  the theory that says what it is; `lists.lut`; `structures/` (universal, algebraic, order,
  equality, containers) and `properties/` state the theories.
- `src/luthier/lib/`: libraries imported by name, each a theory `.lth` with its model `.lut` and
  its store: `numbers`, `arrays`, `tables`, `probability`, `laws`, `test`, `world`, `demand`,
  `plan`, `plot` and others.
- `tests/`: `tests/spec/` holds a program the checker must accept and one it must reject per rule;
  `tests/tester/` holds the test programs that certify the library; the rest is the interpreter's
  own suite.
- `examples/`: `hello.run.lut`, and `sonolocalizacion/`, a distance-graph check over the first
  measurements of the sonolocalización project. `docs/concepts/` holds the tape example.
- `docs/`: the guide, the specification, the principles and the rationale. `record/` holds the
  record of the development: sources, plans, decisions and audits.

The earlier interpreter, from before the specification, is at the tag `v0.1-final`.
