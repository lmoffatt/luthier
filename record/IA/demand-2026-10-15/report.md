# demand.lth and plan.lth: the demand and the plan as values (report)

Written 2026-10-15 by Claude Fable 5.1, an agent of the coordinating session, on
`record/IA/demand-2026-10-15/prompt.md` (step 6.1 of the plan from zero). Four files, one commit
each: `src/luthier/lib/demand.lth` (5df0c75), `demand_model.lut` (e3e8ea2), `plan.lth` (c205571),
`plan_model.lut` (a18c4a9). All four parse and `luthier check` clean (nothing refused that is not
mine; the three refusals met while writing, 4.R1 and 4.R2 on a missing import of `Term`, 4.R3 on
`Strategy`'s constructors touched by no law, were mine and are fixed). certification.lth was not
edited.

## What is stated

demand.lth (8.S1, 8.S2, 6.S10, 6.S15, 12.S18, L12.3, L5.18, L5.19):

- `Demand`: `entry`, `decoration : Maybe Decoration` (the identity when `nothing`), `accepts :
  Grade` (the cutoff, the weakest grade accepted, D-2026-10-14-c), `delta : Maybe Float64`, `fuel`,
  `sets : List (String * Value)` (`--set`), `checked`, `pinned : Maybe String` (the lock, 12.S13).
- Holes `C : U`, `bound`, `evidence`, `assumed : Demand -> Maybe C` (D-2026-10-13-m); holes
  `Decoration : U`, `decorate : Decoration -> Term -> Term` (8.S1's decorated form).
- `LawDemand`, the record certification.lth §3 calls `Demand`, by structure; `inner d entry`, the
  demand an inner action receives with every cutoff kept (L12.3); `admitsAssumptions`.
- `Record` (what `x.run.json` holds of the demand) and `Runs`, a store of runs refined by
  `determined`: one record, one result (8.S3).
- Theory `Demanding { lawDemand, recorded }` with four laws: `PassedDownNotRecomputed` (L12.3,
  6.S15), `NoPriceRefusesAssumed` (6.S10), `LoweringLosesNothing` (certification.lth's
  `ServesIsMonotoneInTheCutoff` applied to the demand passed down, not restated),
  `RecordsEveryCutoff` (12.S18, L5.18).
- demand_model.lut: `theDemand` with every argument of `run` a declared default (L5.19);
  `demanding`.

plan.lth (8.S3, 8.S4, 8.S5, 8.S8 to 8.S11, L5.2, L5.6, L5.11, L5.13):

- `Node`, `Dataflow A` over names; `reaches`, the live subgraph (the backward pass over names
  that computes no value, 8.S3).
- `Schedule`, `LinearizesOn`, `run`, `EquivalentOn`, `Confluent` as a Boolean law with the two
  schedules as parameters (D-2026-10-14-c), the law a dataflow is certified against (8.S11,
  L5.11). The retired `lib/plan.lut` of v0.1-final (a718abc) is the source, rewritten over names
  since the current library has no `forallPairs` over `Fin n`.
- `Strategy` (`ForwardOnDemand`, `CallByNeed`), `Plan A`, the hole `dataflowOf : Program ->
  Dataflow Term` (8.S11's backward pass, not written), `planOf` with the strategy as a default
  argument.
- `DemandKey` (the decoration and the sets the live cone reads), `MemoKey` (demand key, cone,
  mode, seed, plan hash, certificates), theory `Keying A { key, planHash }` with the laws
  `KeySeesTheDemand/Cone/Mode/Seed/Plan/Certificates`, `PlanHashSeesTheSchedule`, in the pattern
  of certification.lth §4. No model (8.S10).
- Theory `Planning A eq { plan }` with `PlanIsTheLiveCone`, `PlanLinearizes`, `StrategiesAgree`,
  `TheDefaultsAgree`, `PlanIsConfluent`, `KeyReadsOnlyTheCone`, `KeyReadsTheType`.
- plan_model.lut: `byNeed` (depth-first order of first demand, run.py's order), `forward`
  (strict rounds), `planning`, and `example` (five names, the entry reaches four; `bothLinearize`,
  `agree` state the check). `luthier eval` on these gives their weak head form only, so the
  values were not confirmed by evaluation; a test line waits for a generator of dataflows.

## Every [proposed]

1. demand.lth §1, `Decoration`: whether the generic form is written by hand or derived from the
   cone, and the interface of `P` beyond 8.S2's functor and applicative laws, are holes (8.S1).
2. demand.lth §1, `Demand`: the entry is a name; 8.S1's term as entry waits for an action that
   asks for one.
3. demand.lth §1, `delta`: `nothing` in this draft, since no statistic becomes a cost before
   D-2026-10-13-m; then required as `assumed` is, with no default (8.S1, D-2026-10-12-r).
4. demand.lth §2, `admitsAssumptions`: until the cost types come, `run --accept assumed` is where
   a demand names the price of assumptions; the Boolean law says a demand whose cutoff does not
   admit `AssumedGrade` refuses every assumed entry (6.S10).
5. demand.lth §3, `Run`: in the Boolean draft the record is the identity of a result; the key of
   8.S8 is plan.lth's (8.S3).
6. demand.lth §4, `PassedDownNotRecomputed`: the name a law certifies, printed to its model
   parameter, is the run's binding and not the demand's, so `given` is what `--set` gave
   (certification.lth §3).
7. demand_model.lut, the defaults: `Sampled`, 10,000,000 steps, `main`, no set, not checked,
   nothing pinned, no decoration, no confidence (L5.19; the values are cli.py's and run.py's).
8. plan.lth §1: the nodes are in the program's order; a name read that no node defines is a leaf
   that keeps `init` (8.S3: a hole is a value that flows).
9. plan.lth §3, `Strategy`: whether the strategy is a field of the demand is open; 8.S1 does not
   list it, so it is an argument of the plan with its default (8.S4).
10. plan.lth §3, `planOf`: call by need as the default, what is implemented; 8.S3's decided
    default is forward on demand; `TheDefaultsAgree` says they give one result.
11. plan.lth §4, `MemoKey.mode`: a string; 8.S1 names `m` and the spec does not define it; today
    the only mode is `--checked`, printed (8.S8).
12. plan.lth §4, `Keying`: a collision of the hash function is the host's, as in certification.lth
    §4.

Decisions of the agent, each one commit to undo: `LawDemand` as a structural alias instead of
moving certification.lth's `Demand` (the brief's "import back" would make a cycle with
`ServesIsMonotoneInTheCutoff`, which demand.lth imports; renaming certification.lth's record to
`LawDemand` touches certification.lth, certification_model.lut and run.py's docstring and is open
to the coordinator); `inner` a definition and not an operation with a law (its statement is its
body); `Runs` as a refinement type in the pattern of certification.lth's `Store`; the lock in the
demand as `pinned : Maybe String`; `Decoration : U` as the hole rather than a type operator, since
the checker takes a hole of type `U` and `Term -> Term` cannot be written as `U -> U` today.

## What run.py must change, one line per law

- `PassedDownNotRecomputed`: build one `Demand` in `run` (entry, accept, fuel, sets, checked,
  lock) before anything, and derive every law's demand and the record from it; today `accept or
  ACCEPT` is resolved twice, in `certification` and in `FirstActions`, and `given` is assembled
  per law inside `certification`.
- `NoPriceRefusesAssumed`: holds today (`--accept assumed` is the only way an assumed entry
  serves); when the cost types come, `--accept assumed` becomes a price in `C`, with no default.
- `LoweringLosesNothing`: holds (`certify.serves` is monotone in the grade); nothing to change.
- `RecordsEveryCutoff`: `record` scatters the demand over the entry (`parameters`, `fuel.given`,
  `checked`, `lock`, `certification.accept`); write it as one object, the model's `Record`, with
  `delta` once it exists.
- `Runs` (`determined`): `x.run.json` is never read back (8.S10); a reader checks `determined`
  before serving anything from it.
- `PlanIsTheLiveCone`: `runtime_slice` is the backward pass over names and gives the live cone;
  expose it as the plan's `live` instead of a tuple of acts.
- `PlanLinearizes`, `TheDefaultsAgree`: the order in which `Runner.force` reduces shared cells is
  the schedule of the call-by-need plan; record it, so the plan is a value with a hash (L5.6).
- `PlanIsConfluent`: nothing; a test runs the example under two schedules.
- `KeyReadsOnlyTheCone`: `fill` accepts and `record` writes every `--set`, read or not; the key
  keeps only the sets whose hole is in the live cone (a set the cone does not read is still
  recorded as given, and does not enter the key).
- `KeyReadsTheType`: nothing until a decoration exists.
- `Keying`: nothing until the result store of D-2026-10-10-d exists; `certify.cone_hash` is the
  route to reuse.
- `dataflowOf`: the hole is the host's `runtime_slice` plus the references of the elaborated
  program, as an extern route; writing it is 8.S11's backward pass.

For the coordinator: 8.S4, 8.S11, 9.S17 and L5.6 cite `lib/plan.lut` as existing; it was retired
with v0.1 at dcd27fd and the carrier is now `lib/plan.lth`.
