# The naive review of the world: one screen for Luciano

Written 2026-10-15 at 10:30 by the coordinator (luthier-3e) from C.md (the judge's table, 72
rows), as the brief's last section asks. A read the principles, B did not, C classified without
ranking. The ranking is yours.

## The counts

Both reports: class 1 (found by both) 39 items; class 2 (only A, attributed to a clause) 6;
class 3 (only A, no clause) 7; class 4 (only B) 3; class 5 (a law that could have been stated
and was not) 17. A, 42 items: 18 shared, 6 by a clause, 7 of its own, 11 missing laws. B, 30
items: 21 shared, 3 of its own, 6 missing laws (asked for as fixes, which C read as laws).

## Class 5, the laws that could be stated (the reviewer that read the principles produced 11 of 17)

- The host, not only `describe`, changes nothing at undeclared places (A5/B3; 10.S7).
- An own action's idempotence covers the result, not only the state (A7/B4; 10.S6).
- The store only grows: earlier certificates stay (A9; 10.S7's second half, L10.4).
- `Host S` is a theory whose law is `agreement`: today `hello.lut`'s `print` has no law and runs
  with no validation (A16/B25; L11.2, D-2026-10-13-a). The strongest finding of the review.
- The identity carries the hash, and there are two identities (A18/B8; 10.S9).
- The validation happens the first time an action asks (A19; 10.S10's last sentence).
- `Crossing` covers records with fields of different types, an absent label, counts per
  callback, and what a failing callback gives the host (A20/B9, A22/B22; D-2026-10-14-a).
- An extern with no `W` in its type leaves the world unchanged (A25; L4.7, 10.S3).
- The array and table conventions of the bridge as laws, keyed by declared type and not by
  field names (A30/B20; 3.S24, 11.S6).
- The world's equality is "read at every place", not structural `==` on the state (A4/B11;
  D-2026-10-13-a).

## Class 2, what a clause produced (only A)

L4.11 (A1, A8: the `act` row of 10.S5 missing; `own` has no home for "declares nothing");
L2.1 (A12: `appendStr` and `hash` declared without body cannot run); L11.4 (A13: no declared
type, library version or platform in `Route`); L5.19 and L5.18 (A33: the default `Sampled` is a
module constant); L10.4 (A35: a law's cone hash moves with the name of an unrelated law).

## Two contradictions both reviewers found, for you

- A provisional extern: world.lth applies it as debt (10.S10), `run` refuses its cone whole
  (12.S17, 6.S14). One gives (A15/B7).
- `settled` fixes which grades let an extern run; the demand's cutoff is ignored (A14/B6;
  6.S10, L5.17).

## What B saw that A did not (class 4)

`Persistence` has no model, no `Assumes`, no `writeFile` (B5; 10.S13); `--set` values reach
laws by parameter name, so equal names collide (B26); `Console`/`HostConsole`/`readFile` name
two things each (B28).

The prediction of the coordinator before the run (the night plan, 06:00): the principles find
design debts, the artifact-only reviewer finds correctness; the difference real but orthogonal.
Borne out: A's own findings are laws and clause-driven; B's three are a model, a collision and
names; the 39 shared ones are the correctness bugs. The practice costs one more Sonnet read of
the principles per review and produced 17 laws to state.
