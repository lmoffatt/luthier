# run.py bite 5: core in every run, the primitives' operands reduced by the Runner, report

2026-10-14, Claude Opus 5.5 (an agent of luthier-1b), on prompt-5.md at 69094ae; saved verbatim
by the coordinator from the agent's final message (the harness refused the agent's write).
Files: `src/luthier/run.py`, `tests/test_run.py`, `tests/run/{connective_on_match,
host_cell_under_operator}.lut`. `host.py` unchanged.

## What changed

1. `run_file` loads `lib/core.lut` before the file. When the file (or something it imports)
   defines a name, core's definition of that name is left out, so the file's own shadows the core
   (12.S22). Core's data (`Unit`, `Empty`, `Bool`, `Maybe`, `List`) is a root of the runtime slice
   in every run, and a constructor named in a term or a pattern pulls in its data. Core's `x : A
   := primitive "name"` becomes the kernel's `Primitive name` when the name is in
   `kernel.BOOTSTRAP_PRIMITIVES`; otherwise a declaration (`Int`, `Float64`, `String`, which the
   bridge reads by name). Core's `operator` acts are not used tonight. `runtime_slice` keeps only
   definitions, declarations and aliases, so `a + b` stays `Var "+"` and `a and b` stays `Var
   "and"`, and the kernel's bootstrap of the symbols does the work, as in `luthier eval`. `not` is
   core's definition, a match, which the Runner drives with the host.
2. `run_file` defines every name of `kernel.BOOTSTRAP_PRIMITIVES` after the program, so a file's
   own definition comes first.
3. When an application's head is a `Primitive`, `Runner.whnf` brings the operands to weak head
   normal form itself, with the host, before `kernel.step` takes the operator's step; left first;
   `toFloat64` has one operand. For `==` it reduces every concrete part: pairs, records,
   injections and a constructor's arguments. On `and`/`or`, when no act defines them, it reduces
   the left operand; the kernel gives back the right operand, which the Runner reduces in turn.

Tests: the port's smallest program prints `yes`; `showInt (intAt t "a" 0 + 1)` on a parsed table
prints `8`; `not (0 >= 3) and 7 mod 3 /= 0 and "ab" == "a" + "b"` gives `ok`. `tests/test_run.py`
32 passed; `pytest tests` 472 passed, 7 xfailed, 1 failed (`test_render_grammar.py::
test_repository_is_current`: `docs/spec/02-grammar.md` stale against the grammar, not this bite's).

## Where validate_graph.lut stops next

`luthier run examples/sonolocalizacion/validate_graph.lut` from the root gives `fuel spent` at
the default 10,000. With `--fuel 1000000` it gives `stuck match` in the invariant over distinct
node names, on `"mic2" /= "mic1"`: the kernel defines `/=` on `Int` and `Float64` constants only,
as term.lth states it (lines 515 and 530); `luthier eval` is stuck on it too. Smallest program:

    import "world_model.lut" HostConsole host : HostConsole
    main (w : W) : W * Unit := host.print w (if "a" /= "b" then "yes" else "no")

4.R8 makes `==` one operation on every concrete type; whether `/=` should likewise be `not (a ==
b)` on every concrete type is for kernel.py's and term.lth's owners.

In a scratch probe patching the kernel in memory so `/=` works on two strings (nothing in `src/`
changed, not committed), the run reaches the end and prints:

    valid: 10 nodes, 22 measurements, 21 distinct pairs; directions the distances do not see: 14 (of which 10 are the heights and 3 the rigid motions of the plane)

270 s and 1,082,929 Runner steps of fuel. Checking 21 and 14 against v0.1 needs a run of v0.1 on
this graph, Luciano's to do. 14 is one more than the 10 heights and 3 rigid motions together.

## Found on the way (reported, not fixed)

- The kernel reads constructors only from a `data` body at the top level of a definition. Core's
  `Maybe` and `List` are parameterized, so they give it no constructors, and `[1, 2] == [1, 2]`
  and `just 1 == just 1` are stuck (EqualityStuck), in `run` and in `eval`. The Runner's own
  match path does not need them, so the graph's run is unaffected.
- The run's default fuel (10,000) is about 100 times too small for this program; `--fuel`
  reaches it; the run is slow (about 4.5 minutes).

## Choices the brief left open (the agent's; each undone by reverting this bite)

1. A file's own definition shadows core's of the same name: core's act is dropped, not appended.
2. Core's data is always in the slice, and a constructor named in a term or a pattern pulls in
   its data (this also covers a file's own data).
3. `primitive "name"` outside the bootstrap set becomes a declaration of the name with its type.
4. The Runner reduces `==`'s operands in every concrete part before the kernel compares them.
