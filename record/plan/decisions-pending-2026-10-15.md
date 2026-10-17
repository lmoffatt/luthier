# Decisions waiting for Luciano, 2026-10-15

Collected by a Sonnet agent of the coordinating session from the sources named under each item
(read only). 40 questions, merged where several sources ask the same thing. Skipped as already
answered: Q1 and Q2 of `record/plan/questions-2026-10-14.md` (D-2026-10-14-a, -b), D-2026-10-14-c,
D-2026-10-15-a, D-2026-10-15-b. Items marked [proposed] below are readings an agent took that one
commit undoes (P6, every change can be undone); a recommendation is only stated when a source gives
one, and the source is named.

## How to answer

1. Under each item write "ok" to take the recommendation, or the letter of the option (a, b, ...).
2. Where an item has no recommendation, write the letter; "skip" leaves the night's default in force.
3. Items 1 and 2 first: each starts a bite. The rest can wait in any order.

## Unblock work

**1. The stores across runs: what may be served, and are the stores places of the world?**
(Rewritten 2026-10-15 by the coordinator after the chat on this item; the first version is in git,
37e458a.) A certificate or a result that survives from one run to the next was written in the world,
and reading it is observing the world. Today `luthier certify` writes `x.cert.json`, and `luthier
run` reads it and writes a first action's entry into it, in Python, outside the token W: no action
declares these writes and `agreement` checks none of them. The run record does not keep the hash of
the store it read. A real case already happened: the suite and `certify` running together overwrote
the stores, a third party writing in the same file, patched with a temp copy and a lock. 10.S6 calls
these own actions (idempotent, memoizable); the code does not yet treat them as actions.
D-2026-10-15-c (every possible behavior has a way to be said) holds in every option: whatever is
served by default, the demand or the program can ask for the literal execution.
Options:
(a) Now: pure results only are served across runs (an acting run always executes); each run
    records the hash of the stores it read; the hole is marked in certification.lth (L14.4, what
    the kernel cannot yet express is written in the host and marked). Later, with the full result
    store: both stores become places of the world with own actions (10.S6 and 12.S11 rewritten).
(b) Now, for v0.4: both stores modeled as places of the world with own actions, and an acting run
    served when its key and the effects the world shows match.
Recommendation (coordinator): (a). It costs an afternoon and makes the hole visible; (b) rewrites
10.S6 and 12.S11 and is better done once, together with the result store.
Unblocks: v0.4's criterion (c). Sources: `record/IA/v04-2026-10-15/report.md` (section 1,
criterion c); `record/plan/night-2026-10-13.md` ("Questions", the v0.4 item); src/luthier/run.py
(the first action's entry), src/luthier/certify.py (the store's write).

a
**2. Does the cone's hash cover the type annotations the elaborator writes?** 6.S8 (a new check
writes a new entry) and P2 (everything derived carries how it was derived) put the cone in the
hash; today the hash covers the annotations, so typing a projection better (reading a model's field
type from its theory) makes six certified laws stale (numpy's `PinvProjects`, `PinvSymmetric`,
`PinvRestricts`, `PinvScales`; lm's `MaximizerStationary`, `QuadraticConverges`) though their terms
are the same. Options: (a) keep the hash and re-certify on every such improvement (about 20
minutes, the stores committed with the Python); (b) a cone hash that erases binder type
annotations (touches 6.S8 and P2). The agent's narrow fix (the sugar reads the record only for its
own decision, `Context.models`) changes no cone and holds meanwhile; no source recommends (a) or
(b). Unblocks: the elaborator fix at the source (a projection typed everywhere), and any later
typing improvement without a re-certification wave. Source:
`record/IA/v04-2026-10-15/report-sugar.md` ("For the coordinator, one question");
`record/plan/night-2026-10-13.md` ("Questions", the cone-hash item).
*Recommendation (coordinator, 2026-10-15, after the chat on levels of equality):* (b). The cone's
hash is the strict level of equality, fixed by the language and the same for every demander, free
and without parameters (as the strict layer of two-level type theory); the levels above it, how
close and how sure a reuse must be, are the demand's. An annotation that leaves the term unchanged
should not stale a certificate. Condition: no erased annotation changes what the term does (today
an operator is resolved in the term itself); it can be stated as a law and tested by elaborating
with and without a typing improvement and comparing the erased terms. Costs do not touch this item.
b
## Identity of evidence and results

**3. Is an exact replay absorbed or kept?** 6.S8 (a new check writes a new entry, both kept) and
6.S15 (writing a certificate is idempotent) disagree on a check whose identity the store already
has; `certification.lth` `record` drops it (line 135 at the frozen commit). Options: (a) absorbed by
idempotence (6.S15), 6.S8 reworded; (b) kept as a new entry (6.S8), `record` and `--deep` changed.
No recommendation (Kimi's reading in the summary: the chapter is ambiguous). Unblocks: the
certificate's store law and `--deep`. Sources:
`record/IA/layer-3-review-2026-10-15/summary.md` (item 5);
`record/IA/layer-3-review-2026-10-15/report-second-line.md` (C3, S6-5, "Luciano: the replay in the
identity"); `record/plan/night-2026-10-13.md` (certify.py item).

a, salvo discrepancia. 

**4. Do fuel and budgets enter an entry's identity?** 7.S13 (a known outcome is not recomputed,
whatever its outcome) means a test that ran out of fuel is "known" and never rerun with more. Today
fuel and budgets are not in the identity (certification.lth line 86). Options: (a) put them in the
identity; (b) let `--deep` write a new entry with the same identity (breaks `determined`);
(c) never memoize a not-run for lack of fuel. Recommended: (a), the certify.py agent's lean (night
plan). Night default: neither until answered. Unblocks: a fuel-starved line becoming runnable
again; the exact form of 3. Sources: `summary.md` (item 5);
`report-second-line.md` (C4); `record/plan/night-2026-10-13.md` (certify.py item).
*Note (coordinator, 2026-10-15, after his reading in the chat):* fuel only cuts a run; it never
changes the result of a run that finishes. So a pass is the same pass at any larger fuel, and (a)
would wrongly make a pass at 1e6 not serve a demand at 1e8. Only a not-run for lack of fuel depends
on it, and it holds only for fuel up to what it was given. Origin: a reading of the theory by an
external review (GPT, C4), not an incident; today neither the fuel given nor the fuel used is
recorded in an entry. A further option: (d) fuel out of the identity; a pass serves any fuel (the
fuel it used recorded, a cost for the planner); a not-run for fuel records the fuel it was given
and serves only demands with that much or less; the same for a sequential test's budget (an
undecided outcome at budget B serves only budgets up to B). Recommendation: (c) now (never memoize a
not-run for lack of fuel: simplest, and correct), (d) when the costs come.
c
**5. Is the run's record the memo key, or does `x.run.json` carry the key's hash?** 8.S8 (a value
and its derivative have two keys) against `demand.lth` 107-108 (`Record` has no decoration, seed,
plan or certificate hashes) and `plan.lth` 151 (`MemoKey` has them; nothing relates the two), so
`determined` forbids two results for one record, which a run with another seed legitimately breaks.
Options: (a) the record is the key (extend `Record` with decoration, seed, plan and certificate
hashes); (b) `x.run.json` carries the key's hash and `Record` stays as it is. No recommendation
(all five reviewers answered question 9 the same way, without choosing). Unblocks: the equal-key
law, B1, B2, B14, and item 1's store. Sources:
`record/IA/layer-3-review-2026-10-15/summary-BCD.md` (top screen item 5, B1, B2);
`report-second-line.md` (B1, B2, B14).
*Recommendation (coordinator, 2026-10-15):* (b). The record says how to reproduce a run (P2); the key
says when two results are the same result; they differ on purpose. Item 4 shows it: fuel belongs in
the record and must stay out of the key, since a pass is the same pass at any larger fuel. The law
`determined` then speaks of the key, and a law relates the two: the key is a function of the
record, the seed, the plan and the certificates. Today `x.run.json` already holds the record
(`demand`), the plan with its hash and the demand key (`key`: decoration and live values), but no
seed and no hash of the whole key.
b
**6. Does the interpreter enter the hash by every commit or by the last tag?** 6.S8 as written puts
the interpreter's revision in the hash, so every store goes stale at any commit to
`src/luthier/*.py` (re-certifying the library takes about 25 minutes). Night default taken at 02:30
[proposed]: the last reachable tag (`v0.2`), no dirty marker, host code behind the cone's externs
hashed by file. This is the tension P2 (exact derivation) against P8 (no more bureaucracy than it
pays for). Options: (a) the last tag (the night's); (b) every commit (6.S8 as written);
(c) the hash of `src/luthier/*.py` content. No recommendation. Unblocks: how often re-certification
is needed. Sources: `record/plan/night-2026-10-13.md` (certify.py and run's refusal items);
`record/principles-candidates-2026-10-15.md` ("Tensions to name").

a--> for now. Cuando Luthier se estabilice c, cuando escribamos el nucleo b. 


**7. Where does `certify` write an entry?** 12.S11 (a run reads the stores of the files it
imports). Entries written beside the test programs are not found by a run. Night default
[proposed]: also written into the store of the file that defines the model named in the binding
(`src/luthier/lib/*_model.cert.json`, un-ignored by .gitignore). Options: (a) the night's default;
(b) the test lines live inside the model files. Unblocks: a run finding the certificates the library
earned. Source: `record/plan/night-2026-10-13.md` (run's refusal, point 1).



**8. Are `*.run.json` files tracked or ignored by git?** 12.S18 (a run writes its record). Night
default: ignored, as `*.cert.json` is. P2 (everything derived carries how it was derived) argues for
tracking those of the slice's runs. Options: (a) ignored; (b) tracked for the slice's runs only;
(c) all tracked. No recommendation. Sources: `record/plan/night-2026-10-13.md` (run 7 item);
`record/principles-candidates-2026-10-15.md` (tensions).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (b). A slice run is the evidence
Luciano will compare and cite, and D-2026-10-15-h made the record the object that says how to
reproduce a run, so it belongs in git beside the program; the suite's runs and probes stay ignored.
P2 (everything derived carries how it was derived) decides it, P8 (no more bureaucracy than it pays
for) bounds it to the slice. Cost: a `.gitignore` exception for `examples/sonolocalizacion/` and a
commit after each of his runs.

*Answered in chat (2026-10-16): (b), D-2026-10-16-h.*

## The world and the host

**9. How much validates a host action: one case at its first application, or one per cone hash?**
10.S10 validates an extern at its first action with one case, which then serves every later
application at any argument (no binding, no reach). Also, an entry per run argument (7.S9) grows
the store by one entry per distinct argument (the fit prints computed numbers) and `print "0.3"`
says little about `print "0.4"`; and a refused run of an action that writes a file has already
written it. Options: (a) one case at the first application serves the run (10.S10 today);
(b) validate once per hash of the model's cone, host code included, the arguments kept as evidence
(not entries); (c) a case per distinct declared place. Recommended: (b), the agent's lean and the
coordinator's (night plan, first-action report). Unblocks: the host's validation scaling to the fit;
closes W10, S10-2, S10-3. Sources: `summary.md` (top screen item 3, question b);
`report-second-line.md` (W10, S10-2, S10-3); `record/plan/night-2026-10-13.md` (first-action item).

*Item 9 answered in chat (2026-10-16): (b), D-2026-10-16-k.*

**10. What does a run do with a provisional extern?** 6.S14 and 10.S12: `world.lth` applies a
provisional extern while `run` refuses it (a contradiction between the two), and a name with no
laws gets no grade (`NoLawNoGrade`). Options: (a) refuse in both; (b) apply in both, printing the
debt; (c) `run` applies only under `--uncertified` (see 11). No recommendation. Unblocks: S10-4,
the O3 of the slice. Sources: `summary.md` (W5, contradictions); `report-second-line.md` (W5,
S10-4, "Luciano: the provisional extern"); `record/plan/night-2026-10-13.md` (naive review item).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a) by default. world.lth's
`applied` should refuse a provisional extern as `run` does: L10.6 (a cone with an uncertified or
provisional name is refused; an exception is O3 and leaves grade `assumed`) and 6.S14 say so. L5.20
(every possible behavior has a way to be said) is met by the demand's price for assumptions
(`--accept assumed` today), with no new flag. Cost: one law of world.lth; 10.S10's "never certified"
becomes "certified only as assumed"; item 11's flag becomes moot.

*Answered in chat (2026-10-16): (a), D-2026-10-16-c; item 11 moot.*

**11. Does `run --uncertified` exist until certification lands?** 12.S17 makes `run` refuse an
uncertified cone with no opt-out (D-2026-10-12-y); D-2026-10-13-ac puts the slice's run before
certification exists. Recommended: `run --uncertified`, printing the debt (the coordinator, with
the inventory, night plan, O3). Now that certification exists the flag may be moot; say whether it is
still wanted. Unblocks: running a cone whose stores are stale (item 2). Source:
`record/plan/night-2026-10-13.md` ("Questions", the inventory item).

**12. What is the default price of the observer's fidelity?** The fidelity of `observe` to the world
cannot be tested by any law inside Luthier; the fix stated it as a root of trust, `assumed` (the
grade for what is not checked), its default price yours. Options: (a) `assumed` with no default
price (8.S1, 6.S10: a demand supplies it); (b) a stated default price. No recommendation. Unblocks:
W1 and W9 (host and disk persistence) closing. Sources: `report-second-line.md` (W1, W9);
`summary.md` (top screen item 1).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a), answered by L10.2 (an
`assumed` certificate's evidence cost is the demand's parameter for assumptions, with no default, so
a demand naming none refuses assumed values) and 6.S10 (D-2026-10-12-t), specific enough to win over
L5.18's declared defaults. Cost: every acting run holds the observer in its cone, so each names a
price (`--accept assumed` today). Where the host gives a guarantee, L9.7 (verification by delegation
is `proved` by citation) removes the price for that place.

*Item 12 answered in chat (2026-10-16): D-2026-10-16-n.*

**13. Which token follows a memo hit of an own action?** 10.S6 (own actions memoized, the token
used once, D4). When an own action is served from the memo, which token comes back is a decision,
not a wording fix. No options given in the source; the agent's reading is that it needs yours.
Unblocks: S10-5. Source: `report-second-line.md` (S10-5).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* answered for now by D-2026-10-15-d
(the stores are read and written in Python, outside the token W, until the full result store), so no
own action is served from a memo under the token today. Later a memo hit is a read of the store, and
L4.10 (an observation is itself an action) gives the token: the one that read returns, as for any
observation. No special rule is needed. Cost: one sentence in 10.S6 when it is rewritten.

*Answered in chat (2026-10-16): ok, D-2026-10-16-f.*

**14. Is a bare value where `Maybe` is declared a `just` in `--checked`?** `tables.py`'s `parse`
returns a table or None and `Table.cell` a pair or None, and the fit reads its CSVs through them.
Options: (a) lenient, the docstring says a bare value is `just` (the night's default [proposed]);
(b) strict bridge, tables.py returns `host.Just`. No recommendation. Unblocks: the strict
`--checked` over the fit. Source: `record/plan/night-2026-10-13.md` (report-12 item).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (b). `--checked` exists to test
what crosses the bridge, and the lenient reading cannot tell `just nothing` from `nothing` in a
`Maybe (Maybe T)`, nor a host that forgot to wrap from one that answered. L11.1 (an extern is
declared over what it really receives and returns) decides it, with L11.8 (what crosses the bridge
is recorded). Cost: `parse` and `Table.cell` in tables.py return the host's `Just` and nothing,
their callers follow, and the cones that read tables are re-certified.

*Answered in chat (2026-10-16): (b), D-2026-10-16-h.*

## Certification and grades

**15. A certificate's grade across bindings.** Reading taken [proposed]: the strongest pass under
one binding, the weakest across bindings. Alternative: the weakest over all entries, which would
pin a law at `sampled` after an exhaustive run with the same generators. Options: (a) the proposed
reading; (b) the weakest over all entries. The certification agent names (a) as the reading most
worth your attention; no source recommends it. Unblocks: the grade rules of `certification.lth`
standing. Source: `record/plan/night-2026-10-13.md` (certification.lth item).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a). Taking the weakest over all
entries would let a later sampled run undo an exhaustive pass under the same generators, against
L10.4 (a later check issues a new certificate that supersedes the old, both kept, so progress is the
chain). Across bindings the weakest is 7.S10's own text ("summarized by the weakest"). Within one
binding, item 41's pooling and L10.11 (cases drawn under several seeds are an aggregate) refine
"strongest pass". Cost: none; the file already states it.

**16. May a failure (the top element) be a cutoff?** 6.S15: today the Boolean slice refuses
failures by `OnlyAPassServes` and every cutoff refuses the top. Options: (a) no, a failure is
refused outside the cutoff; (b) yes, a cutoff may accept it. No recommendation. Unblocks: S6-2.
Source: `report-second-line.md` (S6-2).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a). A cutoff that accepts a
failure accepts anything, which is running uncertified, the opt-out 6.S14 forbids (a cone with a
name lacking a certificate is refused; no opt-out, D-2026-10-12-y). Running past a failure is said
through L10.6's exception (O3, priced as an assumption), which keeps L5.20 (every possible behavior
has a way to be said). The Boolean slice already refuses failures by `OnlyAPassServes`. Cost: one
sentence in 6.S15.

*Item 15 answered in chat (2026-10-16): evidence per region, D-2026-10-16-i.*

*Answered in chat (2026-10-16): (a) by naming the law, D-2026-10-16-h.*

**17. What grade does a bounded exhaustive run give, and in what order?** 7.S10 (a `Bounded n` is a
grade of its own): `test.lth` 125 gives `Confirmed` with `Bounded`, while `laws.lth` 190's
`ForallOnPoints` gives `Confirmed` only under `Exhaustive`, and `CoverageIsTheWeakest` wants an
exhaustive run's coverage to be `Bounded size` while the comments give `Exhaustive`. Also `gradeRank`
is a fixed order where L10.2 orders without a domain (T5). Options: (a) `Bounded` is a grade below
`Confirmed`; (b) `Bounded` of the whole domain is `Exhaustive`; (c) leave and say which file is
right. No recommendation. Unblocks: T4, T5, L7, and the three-file agreement. Sources:
`summary-BCD.md` (T4, T5, contradictions); `report-second-line.md` (T4, T5);
`record/plan/night-2026-10-13.md` (tester item).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (b), which is what 7.S10 already
says ("bounded is exhaustive on the box the domain names"): `Bounded n` is a domain, not a grade,
and L10.2 (the grade is derived from the domain and the evidence cost) decides it. test.lth grades
it so; laws.lth's `ForallOnPoints` should confirm under `Bounded` on its box. `gradeRank`'s fixed
order is the Boolean slice's stand-in until the cost types, to be marked so. Cost: two theory files,
no certified store.

*Answered in chat (2026-10-16): (b), D-2026-10-16-k.*

## The demand and the plan

**18. Is the strategy an argument of the plan or a field of the demand, and is call by need the
default?** 8.S1 lists the demand's fields without the strategy; 8.S3 decides forward on demand,
while `plan.lth` takes call by need as its default (law `TheDefaultsAgree`) [proposed]. Options:
(a) the strategy is an argument of the plan, call by need the plan's default (the draft); (b) a
field of the demand (8.S1 changed), forward the default (8.S3, changes run.py); (c) the strategy an
argument, forward the default. No recommendation (the draft marks its own reading [proposed]).
Unblocks: B10, B22, and 8.S3 against 8.S4. Sources: `report-second-line.md` (B10, B22);
`record/plan/night-2026-10-13.md` (demand.lth and plan.lth item).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (b) for the place, forward for the
default. D-2026-10-13-f (8.S1: the demand is the gate through which parameters change what the
program does) puts a parameter separate from the program in the demand, and L5.2 (by default,
forward on demand) is settled. By D-2026-10-15-h the strategy is in the record and out of the key,
as `Confluent` justifies. Cost: 8.S1 gains the field; run.py's call by need stays the host's
specimen, held to `TheDefaultsAgree`.

*Answered in chat (2026-10-16): (b), D-2026-10-16-d.*

**19. Does a model enter a result's key by the plan's hash or by its cone?** 8.S8 and 8.S11. The
spec's list omits the laws; whether the model enters by plan hash or cone is open. Options:
(a) plan hash; (b) cone hash. No recommendation. Unblocks: B24 and the key law. Source:
`report-second-line.md` (B24).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (b), the cone. The model a type
names is code the result depends on, so it enters where all code enters, the cone's hash, which
D-2026-10-15-e made the strict level of equality fixed by the language; the plan's hash says how the
cone was realized, and a plan over names would miss a changed model. B24's other law (the key
identifies) is ordered by D-2026-10-15-h (the key is a function of the record). Cost: one sentence
in 8.S8 and `Keying`.

*Item 19 answered in chat (2026-10-16): (b), D-2026-10-16-k.*

**20. Do per-law cutoffs get a field in `Demand`?** Today they travel in `sets` under the laws'
parameter names and `DemandKey` keeps one only if the name is in `live`; whether the backward pass
reaches laws is not written. Options: (a) a field (per-law cutoffs, typed); (b) `sets` stays.
No recommendation. Unblocks: B23, and D-2026-10-15-b's alpha, beta, delta reaching a law. Sources:
`summary-BCD.md` (B23); `report-second-line.md` (B23).
*Recommendation (coordinator, 2026-10-15):* (a). When a law returns its cost (its distance) instead of
comparing it with a tolerance it takes, the tolerance leaves the law and becomes the demand's cutoff
for that law; a typed field is where it will live.

*Item 20 answered in chat (2026-10-16): (a), D-2026-10-16-k.*

**21. What is `run`'s default fuel?** 8.S1 (fuel is a resource limit the demand carries). The
default of 10,000,000 (kernel bite 10, proposed) is spent before the fit converges (about 10^9
steps); `--fuel` reaches it. Options: (a) keep the default and pass `--fuel`; (b) a larger default;
(c) unbounded, the budget a recorded `--set`-like parameter of the demand. No recommendation.
Unblocks: the fit without a flag. Source: `record/plan/night-2026-10-13.md` (fuel item).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (c). D-2026-10-15-g settles that
fuel only cuts a run and a pass is the same pass at any larger fuel, so a default bound buys only
cut runs, as the fit showed; 8.S1 lists "limits on resources if the action wants them". The bound
stays sayable, declared and recorded (L5.18, no unrecorded policy constants; fuel in the record,
D-2026-10-15-h). Cost: a runaway program is stopped by hand; `certify` keeps its own budget, since a
test needs one (7.S8).

## Tests and generators

*Answered in chat (2026-10-16): (c) with an optional time limit, D-2026-10-16-d.*

**22. Is a default or a generator's domain constant a cutoff under P11?** P11 (every criterion is a
parameter, never a constant in the code) and D-2026-10-14-c. Four cases wait on one criterion:
`defaultBudgets` (T8; 7.S8 asks for defaults), the eligibility constants of `RankOfDiagonal` and
`ClearFloor` (A3: `f < 0.001`, `1.0 <= |d| <= 1000.0`), the `tailSeriesTerms`/`tailSeriesFrom` of the
Kolmogorov series (P6; the fit's truncation took two named constants), and the evidence's tol 1e-12
as the demand's value [proposed]. Options: (a) a domain or precision of a definition is not a
cutoff (Fable and Grok on A3, P6; the 100th term is exp(-800)); (b) any constant a reader could
vary is a parameter (DeepSeek, Perplexity). No recommendation; the summaries lean (a) for A3 and P6.
Unblocks: T8, A3, P6, and the families' constants (GM1). Sources: `summary-BCD.md` (T8, P6, A3,
contradictions); `report-second-line.md` (T8, A3, P6); `record/plan/night-2026-10-13.md` (fit's
theories, evidence items).

**23. 7.S12: is a vacuous law a pass or a not-run?** Two decided sentences of chapter 7 conflict
(7.S12, vacuous against not run), and which wins is a decision. Options: (a) vacuous is `NotRun`
(coverage zero); (b) vacuous is a pass with its premise count recorded. No recommendation.
Unblocks: S7-1 and the tester's report of rare premises. Source: `report-second-line.md` (S7-1).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a). 7.S12 counts the cases with a
false premise apart from `n`, so a law whose premise never held evaluated nothing and is not run,
its premise count the reason. L9.14 (a law is evidence of nothing until a wrong model refutes it)
decides it: no broken model can fail a vacuous run, and BE2 showed the price, a give-up maximizer
passing `MaximizerStationary` vacuously. Cost: 7.S12's last sentence reworded and one branch of
tester.py.

*Answered in chat (2026-10-16): (a), with convergence laws for iterative algorithms, D-2026-10-16-m.*

**24. Three rules for binding a law's parameters (7.R1, 7.R2, 7.S-profile).** G6: a parameter bound
by a `where` type binding versus a profile parameter (7.R1); L5: `(A : U)` inside a law needs a rule
(7.R2); P8: whether a `Bool` definition outside a `T :=` conjunction is tested or pulled by a
demand. Options per rule: (a) the draft's reading; (b) state the stricter rule in the chapter.
No recommendation; the review says each is the spec's. Unblocks: G6, L5, P8. Source:
`report-second-line.md` (G6, L5, P8).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a) for G6 and P8, written into the
chapter; L5 has its strict rule. G6: the draft's `resolve` takes the parameter first, then the
scope, by 7.R1's reason (only a parameter binding tells two parameters of one type apart). L5: 7.R2
(testing a law quantified over a type `U` is a static error) answers it; `Settling`'s laws move to
an instance. P8: a Bool definition is tested when a conjunction claims it or a test names it. Cost:
three sentences.

*Answered in chat (2026-10-16): (a) for the three, D-2026-10-16-l.*

## The specification's wording

**25. Keep the lexer's three readings of 2.S1?** ASCII letters and digits; blanks space, tab, CR;
backslash a class of its own, marked [proposed] in grammar.lth's lexicon. Options: (a) keep;
(b) name changes. Unblocks: closing 2.S1's wording. Source: `record/plan/night-2026-10-13.md`.
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a). ASCII names keep the cone's
hash, which D-2026-10-15-e made the strict level of equality, free of Unicode normalization (two
encodings of `á` would be two names); the blanks and the backslash class are what today's files and
the three escapes of D-2026-10-13-q need. No source asks for more. Cost: Greek or accented names are
refused (`σ` is natural for a biologist); widening later is one commit to grammar.lth and parse.py,
with a normalization rule stated then.

*Item 25 answered in chat (2026-10-16): ASCII, with rules for symbols to be proposed, D-2026-10-16-k.*

**26. Which stands: 3.R1's first paragraph and 3.R2, or D-2026-10-13-x?** 3.R1 and 3.R2 say names
and labels are binders and `Int * Bool` is one structure with the record; D-2026-10-13-x says the
opposite. The night left both texts. Options: (a) the decision stands, 3.R1 and 3.R2 reworded;
(b) the chapter stands, the decision reversed. No recommendation. Unblocks: the spec's consistency
on 3.R1. Source: `record/plan/night-2026-10-13.md` (the audit finding 4).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a). D-2026-10-13-x is his, later,
and carried out: term.lth keeps the labels, the hash covers them, and 3.R1 already holds a `[decided
D-2026-10-13-x]` paragraph, so its first paragraph and 3.R2 describe the old checker. L2.7 (what
makes a definition a concept is a law stating the role of each part) agrees: two labeled units are
not `Bool` without `Bool`'s laws. Cost: 3.R1 and 3.R2 reworded; `k_named_product` and
`k_bool_is_sum` flip to reject when the checker follows.

*Answered in chat (2026-10-17): (a), D-2026-10-17-a.*

**27. A refutable pattern on `<-` (`(w, just x) <- ...`).** 2.S17, D-2026-10-13-ag. Night default:
the checker refuses it with a message; alternative: a `Failures` of the block. Options: (a) refuse
until a real case; (b) `Failures`. Recommended: (a), the night default (the night plan asks "keep the
refusal until a real case?"). Source: `record/plan/night-2026-10-13.md` ("Questions").

*Item 27 answered in chat (2026-10-17): (a), D-2026-10-17-h.*

**28. Ratify, in bulk, the `[proposed]` readings the agents took.** Each is one commit to undo (P6).
The batches: the slice's theories (18 readings, `record/IA/slice-theories-2026-10-14/`), the fit's
theories (14, `slice-theories-2-2026-10-14/`), plot.lth (15, with the canvas as a field of `Plot`),
certification.lth (13), demand.lth and plan.lth (12), the spec flips (4.S5, 4.S10, 4.S11, 4.S22
`[proposed]`; 4.S13 `[decided D-2026-10-12-z]`; 2.S18; 4.R4 rewritten), the elaborator's readings
(a conjunction with a `Law` part typed `Law`, 5.S6; a `primitive` name declared at a type is a type,
11.R1; a `Record` label binds in later fields, 3.S31, term.lth §2 to say it), and the tester's
inconsistencies (`Exhaustive` declared twice, `Assumed` clashing, `LeqBoth`). Options: (a) ok all,
naming exceptions; (b) read the lists. No source recommends; the night marks each reversible.
Unblocks: the `[proposed]` markers clearing from the spec and theories. Source:
`record/plan/night-2026-10-13.md` (the several items named).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* (a), naming the exceptions below:
each reading is one commit to undo (P6, every change can be undone) and no source contradicts the
ones ratified; the held ones are reversed by a decision of this week or wait on his own open
questions.
- The slice's theories (18): ratify, except 12 (a theory file importing a model by name), held with
  T7, since L2.6 says a theory file never holds a model of a theory declared elsewhere.
- The fit's theories (14): ratify, except 2 (the same import), 5 (the series' truncation as two
  constants; D-2026-10-16-b derives it from the demand's tolerance) and 9 (the damping as the host's
  own values; D-2026-10-16-b makes it a declared default, recorded).
- plot.lth (15): hold all, with G1 to G5 of `record/plan/plots/plan-plots-2026-10-14-decisions.md`,
  which he has not answered.
- certification.lth (13): ratify; the reading on a known identity is now D-2026-10-15-f (kept when
  it disagrees), and the provisional refusal follows item 10.
- demand.lth and plan.lth (12): ratify, except 5 (the record as identity, reversed by
  D-2026-10-15-h), 7 (the fuel default, item 21), 9 and 10 (item 18).
- The spec flips: ratify 4.S5, 4.S10, 4.S11, 4.S22 as `[proposed]`, 2.S18 and 4.R4; hold 4.S13,
  whose borrowed `[decided D-2026-10-12-z]` presents the model's reason as his decision (P1,
  Luciano's part stays discernible), to be marked `[proposed]`.
- The elaborator's readings: ratify the three (a conjunction with a `Law` part typed `Law`; a
  `primitive` name at a type is a type; a `Record` label binds in later fields, which fixed a
  capture).
- The tester's inconsistencies: ratify the fixes (rename the duplicate `Exhaustive` and the clashing
  `Assumed`; `LeqBoth` as a constructive subtype, 7.S6); they are defects, not readings.

## Principles

*Item 28 answered in chat (2026-10-17): (a) with exceptions, D-2026-10-17-h.*

The four clauses below are proposals of a fork (luthier-5d); the wording is the model's, the
quoted words his. Source for 29 to 33: `record/principles-candidates-2026-10-15.md`.

**29. L2.8 (a definition and the law of its role live in one file; nothing is said twice).** Where
the role is a theory stated elsewhere, the defining file claims that theory's model. Guided
D-2026-10-14-b. Options: (a) add as proposed; (b) reword; (c) leave in the record. Recommended:
(a), the fork (candidates, C1). Cost: one clause.

**30. L2.7 sentence and a P13 clause: the conceptual is the practical at another level.** Adds "To
be conceptual is to be practical at another level: the law pays when it bites, not when it is
read" to L2.7, and under P13 that a review counts laws that could have been stated as a class of
finding, which a judge classifies and does not rank (P1, P12). Options: (a) both; (b) the sentence
only; (c) neither. Recommended: (a) (candidates, C2). Cost: a sentence and a clause.

**31. L13.5 (a cutoff below the realization's resolution buys nothing).** A demand's tolerance below
what rounding resolves there asks for evidence the computation cannot give; the law's comparison
carries the scale (11.S14). Evidence: the fit at tol 1e-6 and 1e-12 agree to 4e-7 m. Options:
(a) add; (b) leave in the record. Recommended: (a) (candidates, C3). Cost: one clause.

**32. L11.8 (what crosses the bridge is recorded; a host value Luthier cannot reduce is opaque).**
States D-2026-10-14-a as a clause. Options: (a) add; (b) leave in the decision. Recommended: (a)
(candidates, C4). Cost: one clause.

**33. O1's note and L5.6's citation.** (i) A sentence in O1 that the cutoff parameters the Boolean
laws take are the hook where the cost enters (D-2026-10-14-c; candidates, C5). (ii) L5.6 cites
`lib/plan.lut`, retired: name `plan.lth` (the principles record is yours; the spec's 8.S4, 8.S11,
9.S17 already corrected). Options: (a) both; (b) one. Recommended: (a) (candidates C5; night plan).
*Addition (coordinator, 2026-10-15):* the first case for (i): `PinvProjects` (arrays.lth) computes
the distance inside `approxMatOf` and discards it when comparing with `tol`; returning it lets the
certificate record "worst residual over n cases" once and every demand decide by its cutoff without
re-testing. With a sampled cost the certificate keeps the sample (or a sufficient summary), not only
the verdict, since a cutoff near the observed values may need more sampling.

## The sonolocalización slice

**34. Keep or drop the A2 block in session A's graph?** Decision of D-2026-10-06-sa/sb, still
yours. The corrected graph is `python src/prepare_experiment_zero.py 2026-09-07/distancias.csv
<out> --array 3.5m`, which you run; the slice runs on the 2026-10-04 graphs in the meantime.
Options: (a) keep A2; (b) drop it. No recommendation. Unblocks: the corrected graph and step 4 of
the slice's plan, and the comparison with v0.1 (sigma 25.7 cm with every standardized residual below
0.8, against this port's 0.235 m, residuals -1.46 to 0.95, which needs your v0.1 run on the same
graph). Source: `record/plan/night-2026-10-13.md` (sonolocalización items).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* technical reading, his call.
Without the three A2 rows sigma falls from 0.235 m to 0.022 m, the tail probability rises from 0.048
to 0.58 and every standardized residual is within 1.2: a tenfold change from 3 of 22 measurements
points to a systematic error in that block, not noise. Both fits predate D-2026-10-06-sa/sb.
Regenerate the corrected graph first, then decide; if A2 goes, record why and keep the with-A2 fit
(P3, keep the original evidence).

*Answered in chat (2026-10-17): both, and compare, D-2026-10-17-i. Items 35 to 37 wait for the core.*

**35. How to make the fit faster?** About 95 s per iteration, mostly the native 22 x 30 Jacobian
crossing entry by entry through the Runner, and the score and information asked twice at the same
point. Options: (a) speed the Runner (kernel.step rebuilds its environment per call; the native
Jacobian stays certified by laws); (b) the model gives the Jacobian as one extern over the whole
vector (v0.1's `distances_python.lut`). The night does (a) as far as it goes. No recommendation.
Unblocks: the fit's wall time. Source: `record/plan/night-2026-10-13.md` (fit's cost item).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* technical reading, his call. Mostly
answered by events: bite 12 (69c78ad) made the Runner 13 times faster, 4.8 s per iteration against
95 s, and the fit runs in about 5 minutes. So (a), as the night did; the native Jacobian stays
certified by `IsJacobian`, and (b) would bring an extern that L11.2 (an extern is validated against
its type's laws before it is applied) holds to the same law. Revisit (b) on a real case. Cost: none
now.

**36. S4 (macroir after) and S5 (the VS Code extension) of the sonolocalización plan.** Written,
untried by you; S2 and S3 applied by your instruction. Options: (a) accept; (b) hold; (c) drop.
No recommendation. Source: `record/plan/night-2026-10-13.md` (first item list).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* technical reading, his call. (a)
for both. S4's condition, the slice running end to end, is nearly met: the fit runs, and step 4
waits only on the corrected graph; macroir's own inventory comes first, as it did here. S5's minimal
extension exists in `tools/vscode-luthier` and costs him one try. Neither has a dependent yet, so
holding them costs nothing either.

**37. Laplace by information or by curvature?** `laplaceUpdate` takes the precision as the
information; for a nonlinear mean the negative Hessian differs from Fisher. Options: (a)
information (as written); (b) the negative Hessian (curvature); (c) both, the law `InfoIsTheHessian`
relating them. No recommendation (the review says it is a design question; the candidates note the
law is missing from belief.lth). Also whether `laplaceUpdate` should carry `converged`. Unblocks:
BE5. Sources: `summary-BCD.md` (BE5); `report-second-line.md` (BE5);
`record/principles-candidates-2026-10-15.md` (C2).
*Recommendation (an Opus agent of the coordinator, 2026-10-16):* technical reading, his call: (c).
For a nonlinear mean the negative Hessian of the log-likelihood is the information minus the
residuals times the mean's second derivatives, over the variance; they nearly agree at a good fit,
and the fit already computes the information. Keep it, and state `InfoIsTheHessian` with its
distance, the law the fit's bad smell found missing, with a refuted model (L9.14, a law is evidence
of nothing until a wrong model refutes it). `laplaceUpdate` should carry `converged` (BE2).

## Tags and pushes

**38. The quote lint's old debt.** `check_quotes.py` fails on 87 lines of `record/decisions.md`
(D-2026-10-09-a to D-2026-10-12-w) and P15: sources not in its grammar, from before the lint.
Options: (a) list the debt and tag with the other lints green (the night default); (b) source the
old entries first. Recommended: (a), the night plan. Unblocks: a clean lint set at the next tag
(v0.4's criterion f states the exit 1 as "the old debt, his question"). Sources:
`record/plan/night-2026-10-13.md`; `record/IA/v04-2026-10-15/report.md` (criterion f).

**39. A typing bite before the next tag?** `check.py` runs program.lth's predicates and is not a type
checker (`asBad (x : Int) : Bool := x` passes), so the `k_*` accept programs show no predicate
fires, not that the typing is right (4.R9 strict, 4.R11). Options: (a) after the next tag (the
night's default); (b) before it. Recommended: (a), the night plan's default. Source:
`record/plan/night-2026-10-13.md` (audit finding 1).

**40. Which of v0.4's open criteria block its tag?** (b) `session` met by the later work (state
should be rechecked); (c) the result store, item 1; (e) six uncontrolled laws, all in
`sonolocalizacion_laws.lut`, none yet in world.lth, demand.lth, plan.lth. Options: (a) tag when (c)
and (e) are met; (b) tag with (e) listed as debt. No recommendation; no push is asked by any source
(CLAUDE.md: push only tagged milestones). Source: `record/IA/v04-2026-10-15/report.md` (section 1).

## Added after the list

*Item 40 answered in chat (2026-10-16): (b), D-2026-10-16-f.*

**41. Does a law's evidence pool its cases across seeds?** (Added 2026-10-15 by the coordinator,
from his remark in the chat: a seed makes the stochastic deterministic, and matters for the identity
of stochastic functions and for immutability, but to see whether a function passes its laws one
wants many cases, and the seed is beside the point.) Today each seed writes its own entry and the
grade is the strongest pass under one binding (certification.lth `pool`, line 408): two passes of
100 cases with different seeds count as two certificates of 100, not one of 200. Under the
sequential test (D-2026-10-15-b) another seed is more sample. Options: (a) the seed enters the
identity of each stretch of sample, so it can be replayed (item 3), and the verdict is computed on
the union of the stretches of one law, cone and binding; (b) each seed stays a separate entry, as
today. Recommendation (coordinator): (a). The seed keeps its two other uses: in a run's result key
(item 5) and in comparing two stochastic functions on the same draws.

*Answered in chat (2026-10-16): (a), D-2026-10-16-g.*

**42. Is `fresh` a field of the demand or only an argument of `run`?** (Added 2026-10-16, the
result-store agent's question relayed by the coordinator.) `luthier run --fresh` executes literally
whatever the store holds (L5.20, every possible behavior has a way to be said); today it is an
argument of `run`, recorded in the run's `result_store`. Options: (a) a field of demand.lth's
`Demand`, declared with its default (L5.19, the outermost demand carries its defaults as declared
arguments), like every other argument of `run`; (b) only an argument of `run`. Recommendation
(coordinator): (a), by L5.19 and D-2026-10-13-f (the demand is the gate through which parameters
change what the program does). Source: `record/IA/code-follows-2026-10-16/report-store.md`.
*Answered in chat (2026-10-16): (a), D-2026-10-16-d.*

## Not listed

Skipped as not waiting on Luciano: findings stated as fixed or "left" with a technical reason
(G7, G8, G11, T1, T2, T7, B3, B4, B5, B18, B21, GM1, BE4, BE6, BE7, C8, CM3, M2, A1, A2, E1 of
`report-second-line.md`); `report-e.md`, `report-findings-e.md` and `report-session.md`
(not in the named sources); the stale "12.S20 says implemented" question (the sugar report
rewrote 2.S18 and the session exists). Scripts for you to run, not decisions: the corrected graph
of session A (34), the v0.1 fit on the same graph, `check_quotes.py` sourcing if 38 is (b).
