# Report: the token sugar on an imported model's action, and 2.S18's wording

2026-10-15, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-sugar.md` of this
folder (d9bc6bc). The Python is uncommitted: `src/luthier/elaborate.py`, `tests/test_elaborate.py`,
`tests/test_run.py`, `tests/run/print_twice.lut` (new). The chapter is committed alone at 264c098.

## The bug

As the brief guessed. `run.py` turns `host.print` into the projection `(host).print`, and `host` is
typed `HostConsole`, an alias of `Host State`. `infer` gave a projection a type only when its
record's type was already a record, so `Host State` (an application of the theory `Host`) gave
`?type`. `block` then saw no action and took the `Let` branch, binding `w` to the pair.

## The fix, narrower than the brief asked [proposed]

`theory_record(ty, c)` (new, factored out of `theory_domains`, which now uses it with the same
behaviour) reads the record of a theory applied to its arguments: `Host State` is `Host`'s record
with `S` as `State`.

I first applied it in `infer`'s projection case, as the brief says ("at the source"). That fixed
the bug and broke 7 tests: the cones of numpy's `PinvProjects`, `PinvSymmetric`, `PinvRestricts`,
`PinvScales` (arrays_model) and lm's `MaximizerStationary`, `QuadraticConverges` changed their hash
and went stale, so every run through numpy or lm was refused. The terms are the same; only the
type annotation of a `:=` on a projection changes, `p := m.pinvSym fl s` going from `?type` to the
field's type, and the cone hash covers it. Re-certifying in a scratch copy of the stores took 21
minutes for the files it could reach (the sonolocalizacion-dependent ones cannot run from a copy),
replaced the 11 old Pinv entries of `arrays_model.cert.json`, and touched four stores under
`tests/tester/`. Those stores would have to be committed with the Python, since the committed
elaborator would see them stale.

So the fix as left reads the theory's record only for the sugar's decision: `Context.models`
(default off) makes `infer` read it, and `block` sets it on a child context only when the item is
a bare name on `<-` whose value is not already seen as an action. If that reading finds an action,
the item becomes the one-arm match of 2.S17. No existing cone changes; no store was written.

## Tests

- `test_elaborate.py::test_Blocks_action_unit_through_an_imported_model`: `w <- (host).print w0
  "a"; w <- (host).print w "b"; w`, with `Host (S : Concrete) : { console : S, print : W -> String
  -> W * Unit }` and `HostConsole = Host State`, elaborates to two nested one-arm matches on
  `(n, _)`.
- `tests/run/print_twice.lut`: `w <- host.print w "first" ; w <- host.print w "second" ; (w, unit)`
  over `world_model.lut`; `test_run.py::test_a_bare_name_binds_the_token_of_an_imported_models_action`
  runs it.
- The session too: `printf 'w <- host.print w "a"\nw <- host.print w "b"\n:quit\n' | luthier
  session --world examples/hello.lut` prints `a`, `b` (after the two first-action notes).

## 2.S18

Rewritten to what is true (264c098): `[implemented]` with its decision kept, the command as 12.S20
describes it, a line not type-checked today (the session evaluates as `eval` does; verified with
`1 + "a"` printing `: Int`), and the world only with `--world` as `[proposed]`, pointing to 12.S20.
The stale "which `cli.py` does not have yet" and "waits for actions" are gone. 8.S13 still cites
`cmd_session` and says a line joins "only if it checked"; that chapter was out of scope.

## For the coordinator, one question

Should a projection's type be read from its theory's record everywhere (the brief's fix), at the
cost of re-certifying the 6 laws above plus whatever the sonolocalizacion-dependent law files hold,
with the stores committed together with the Python? The alternative that makes such improvements
free is a cone hash that erases binder type annotations; that touches 6.S8 and P2 (everything
derived carries how it was derived), so it is Luciano's. Until then the narrow fix holds and is
undone by one hunk.

Seen while re-certifying in the scratch copy, not inspected: two of the new `PinvProjects` and
`PinvRestricts` entries (seed 20261014) have grade `None`.

## Decisions taken on my own (each undone by one commit)

- The narrow fix (`Context.models`, read in `block` only) instead of the fix in `infer`.
- A bare name on a theory-model action whose result is not `Unit` (`r <- host.readFile w "f"`)
  now becomes a one-arm match binding the pair, as it does for an action declared alone; before,
  it was a `Let` of the pair.
- 2.S18 marked `[implemented]`, with the sentence that a line is not type-checked today.

## Accepted when

- The suite passes: 729 passed, 5 skipped, 9 xfailed, with the Python uncommitted.
- `luthier run tests/run/print_twice.lut` prints `first` and `second`, exit 0 (run from a scratch
  directory with `LUTHIER_LIBRARY_STORES` set to a copy).
- `scripts/check_spec.py` prints nothing.
