# Review of layer 3 (world and certification), round 1: what the replies say

2026-10-15, by Claude Opus 5.5, an agent of the coordinating session, on the brief
`prompt-summary.md` of this folder (section "The prompt"). Inputs: the five replies under `A/`
read whole (sha256 prefixes: gpt.md 958af9d35fb1, deepseek.md dea12a8b2285, perplexity.md
5a19ea43138c, grok.md 7083c9fc7e90, kimi.md 3ab955d719a4); the reviewed files at the frozen commit
055589c (`FROZEN`), read at the lines the findings quote; `src/luthier/host.py` where a finding
depends on the host. Claude's reply (Fable on the web) is pending and comes in a second pass.

Already fixed at HEAD (43a9d6d): nothing. `git diff 055589c..HEAD` over the four Luthier files,
the two chapters and `host.py` is empty, so every finding below stands as written.

Each finding gives the models that raised it, the line quoted with its number (at 055589c, the
same at HEAD), what I checked, and my reading of whose it is: the theory's (the `.lth` file), the
model's (the `.lut` file), the specimen's (the Python host the model is certified against), the
specification's (the chapter or a decision), or a reviewer's misreading. Findings raised by three
or more models come first in each file.

## For Luciano: the five things to change first

1. **`Host` certifies a host action against what the host itself supplies** (all five models, each
   on a part; Grok then says under its item 9 that nothing is missing). The description of `print`
   is any `Described` value the host's model chooses, the observer is the host's own route, and
   only the places the description declares are observed. Kimi's no-op host (print does nothing,
   described as doing nothing) passes every law of `Host`. In the specimen the gap is concrete:
   `print_line` appends to a Python buffer and `observe` reads that same buffer back
   (host.py 97, 100-103); what reaches the terminal is written by `run` at the end (run.py 2232),
   outside every law. The fix has three parts: `Host` takes the `Console` model and its descriptions
   are the console's; a host-side law that undeclared places do not change (10.S7 asks for it); and
   the observer's fidelity stated as a root of trust, cited or `assumed` (the grade for what is not
   checked), since no law inside Luthier can test it.
2. **The grade of a certificate is pinned only for exactly two passes** (all five). Both grade laws
   require `c.entries == nil` (certification.lth 280, 285), so one pass, or three, can get any
   grade: Kimi's model upgrades three passes graded cases, sampled, cases to proved and passes every
   law. The fix is a law per step of the fold (adding one current pass to any certificate) or
   `grade` defined in the theory instead of left to the model.
3. **The laws of `Host` act on the world and drop the token** (GPT, Perplexity; Kimi as not sure).
   `HostAgreesPrint` ends `{ (w1, holds) -> holds }` (world.lth 261): a Bool-valued definition that
   performs an action, and loses the token D4 (the token is used exactly once) says someone must use,
   and with it the action's result. GPT's fix: the law is a pure predicate over an observed case
   (before, arguments, after, result); `agreement` is the action that gathers the case and returns
   the token and the result to the program.
4. **A current failure does not stop a run** (Perplexity alone; verified, and heavy). With a failed
   and a passed entry of one law at the current hash (two seeds, so the store allows both), the
   certificate has no grade (`AFailureRefutes`, line 269), yet `RefusalSaysWhy` refuses nothing as
   soon as one entry serves (line 337), and the model does the same (certification_model.lut 70).
   A refuted law reaches `Certified`. The fix: a law is refused when its certificate has a current
   failure, whatever serves.
5. **What a repeated check leaves in the store** (GPT on budgets; GPT, Perplexity, Kimi on
   `record`). This one is yours, since it touches decided clauses. The identity of an entry has no
   budgets (line 86), so a test that ran out of fuel is "known" and, by 7.S13 (a known outcome is not
   recomputed, whatever its outcome), never run again with more fuel. And `record` drops an entry
   whose identity the store has (line 135), which 6.S8 (a new check writes a new entry, both kept)
   forbids and 6.S15 (writing a certificate is idempotent) allows. The question: is an exact replay
   absorbed by idempotence, and is a not-run for lack of fuel part of the identity (budgets in it) or
   never memoized?

Contradictions between the models, and my reading:
- Whether `Host` is complete: Grok says no law is missing; the other four find gaps. The four are
  right (Kimi's no-op host above).
- Roles (L2.7: every constructor of a `data` has a law stating its role): DeepSeek and Kimi say
  `Value` has none, Grok says `Value`, `Reach`, `Outcome` and `State` have none; GPT and Perplexity
  say the roles are stated. GPT and Perplexity are right: `ReachesAsSets` says intervals read
  `Number` and never `Printed` (lines 304-309), and the other three types name their role laws in
  their comments. `Value` lacks only the "Roles:" pointer.
- `ChangesOnlyDeclared` (line 99): DeepSeek and Grok call its premise rare; Kimi and Perplexity say
  a random place is the case to test. The premise is common, so Kimi and Perplexity are right on the
  shape; Grok's real point is that a random string rarely is the one place a wrong description
  writes, which a `World` operation listing its places would fix.
- `record` against 6.S8: GPT and Perplexity read it as the file breaking the chapter; Kimi reads the
  chapter as ambiguous between 6.S8 and 6.S15. Kimi's reading is the accurate one (item 5).

Also agreed, and routine (four or five models): several laws guard their consequent with a premise
random cases rarely meet, the two grade laws worst; they go over subtypes once item 2 is settled.

## world.lth

### Raised by three or more

W1. **`Host` does not determine agreement with the world** (all five, by parts). Verified at each:
- The descriptions are fields the host's model fills, with no tie to `Console` (Kimi, Perplexity):
  `printDescribed : String -> Described S Unit world,` (line 240). Kimi's no-op host passes:
  `describe = fn st { (st, unit) }`, `print w s = (w, unit)`; `Described`'s two laws hold of it and
  `agreement` compares two no-ops.
- The observer is not anchored to the world (GPT, Perplexity): nothing relates `observe`'s `S` to
  the places it names. The specimen shows it: `observe` returns `_stdout`, the buffer `print_line`
  appends to (host.py 97, 102), and the terminal gets the text from `run` at the end (run.py 2232).
- Undeclared places are never observed (DeepSeek, Perplexity, Kimi; GPT's counterexample is near):
  `match o.observe w0 d.places` (line 244); `ChangesOnlyDeclared` (line 99) constrains the
  description only. 10.S7 says "That an action changes only what its declaration says is a law of
  the world's library over the observations it defines, certified as any law".
- `HostObserveChangesNothing` is too weak (DeepSeek, Perplexity, Grok): `first == second`
  (line 265) holds for an observer that overwrites a file with a fixed value and reports it, or
  that writes an unobserved place.
Whose: the theory's, and 10's for not stating where trust in an observation comes from (GPT).
What can be fixed in the files: `Host` parameterized by `Console S`, a host-side frame law. What
cannot: observer fidelity, which is a cited or assumed root (GPT's "explicitly cited/assumed root of
trust"); it is a question of principle for Luciano only if he wants it checked rather than assumed.

W2. **The `Host` laws perform an action and drop the token** (GPT, Perplexity; Kimi as not sure).
`match agreement ... { (w1, holds) -> holds }` (lines 261, 263) and `{ (w2, second) -> first ==
second }` (line 265). Verified. The comment at lines 249-259 says the runner keeps the token and
runs the law once; the definition does not say it. A function `W -> Bool` is neither a definition
(10.S1: no effect) nor an action (10.S3: `W -> ... -> W * A`). Perplexity adds that the action's
result is lost, so a checked `readFile` cannot hand its text to the program. Whose: the theory's.
GPT's fix (pure predicate over the observed case; `agreement` the action that gathers it) keeps
D-2026-10-13-a (an action is checked by comparing the representation before and after) and fits the
line 254 rule that a law taking a token is not sampled.

W3. **An extern's declared type is absent, so "not applied without laws" cannot be said** (GPT,
Kimi, Perplexity). `Route = { name : String, route : String, provisional : Bool }` (line 125)
against the comment "An extern whose type has no law to validate against is not applied (L11.3)"
(line 130) and 10.S8 ("An extern has a name, a declared type and a route"). Verified. Kimi's
validator (`Confirmed` unless provisional, always applied, identity `appendStr r.route h`) passes
the three `Externs` laws. Whose: the theory's.

W4. **Implications over a type** (GPT, DeepSeek, Perplexity, Kimi). `not d.own or ...` in
`OwnIsIdempotent` (line 89) and `not r.provisional or ...` in `ProvisionalIsAssumed` (line 145).
Verified; random descriptions are mostly not own, random routes mostly not provisional. Quantify
over the own descriptions and the provisional routes. DeepSeek also lists `IdentityCarriesHash`
(`h == k or`, line 149) and `ReadGivesThePlace` (`p == c.stdout or`, line 212): there the premise
excused is the rare case and the common one is tested, a misreading. `ChangesOnlyDeclared`: see the
contradictions above.

W5. **`RecordCrossesByField` constrains one-field records only** (DeepSeek, Perplexity, Kimi).
`b.callField [(l, f)] l xs == b.callBack f xs` (line 182). Verified: a bridge right on singletons
and returning `(nil, 0)` for two fields passes, against D-2026-10-14-a (a record crosses with each
function a callback). Whose: the theory's.

### Raised by one or two

W6. **`OwnIsIdempotent` constrains the state and not the result** (Kimi). Line 89 compares
`stateAfter` only, while 10.S6 says own actions are "idempotent and memoizable"; memoizing needs the
result too. Verified. Whose: the theory's.

W7. **Provisional externs applied unconditionally** (Perplexity; GPT at the chapter level).
`e.applied r h == (r.provisional or settled (e.verdictOf r h))` (line 142) against 6.S14 ("if any
name of the cone ... is provisional, the demand is refused"). Verified, but `certification.lth`
already refuses a provisional name whole (`ProvisionalIsRefused`, line 331), so in a strict run the
two agree; the tension is between 10.S10/4.R5 (provisional applied as debt) and 6.S14, where the
exception would be O3 (the opt-out of certification). Whose: the specification's.

W8. **`settled` accepts a sampled verdict as a constant** (Perplexity). `settled (v : Verdict) ...
Supported -> true` (line 139); `Supported` is the verdict of a sample that confirmed every point
(laws.lth 190). Whether a sampled validation is enough to apply an extern is a criterion, and
D-2026-10-14-c (every cutoff a law needs is a parameter the demand supplies) puts it in the demand.
The only cutoff finding in the round that is a real constant. Whose: the theory's.

W9. **`Persistence` and `ChangesOnlyDeclared` over every string** (Grok). The laws hold, but a random
string rarely is the place a wrong `write` or description touches. Partly verified (see the
contradictions); the remedy needs an operation of `World` that lists the places of a state.

## world_model.lut

M1. **The three host routes cannot be checked from the files** (all five, as not sure). Lines
55-57. Reading `host.py` settles two of the questions:
- DeepSeek's `p = "stdout"` case breaks `HostAgreesReadFile`. `readFileDescribed "stdout"` describes
  `lookupFile st.files "stdout"` (lines 29, 43), but `observe` never puts a file named "stdout" in
  `files` (host.py 91-92: `if place == "stdout": continue`), while `read_file("stdout")` reads it
  from disk. With such a file present, the host is refused. Whose: the model's (one namespace for
  the stream and file paths; `ReadGivesThePlace` already excludes `p == c.stdout` for `Console`, but
  `Host` has no such exclusion).
- The observer reads the buffer the action writes (W1).

M2. **The pure part satisfies its laws** (GPT, Perplexity, Kimi, Grok). `console`,
`printDescribed`, `readFileDescribed` against `Console` and `Described`: verified at lines 26-46. No
finding.

M3. **"the token comes first and goes back unchanged"** (Perplexity). Line 48, against 10.S5's
`act` "gives a new token each time". The Python returns the same object (host.py 103), which is an
implementation of the abstraction; the comment states the implementation as if it were the theory.
Whose: the model's comment. Minor.

## certification.lth

### Raised by three or more

C1. **`grade` underdetermined** (all five). `not (c.entries == nil and ... ) or k.grade (withEntry
(withEntry c f) e) == just (weakest g h)` (lines 279-283) and its twin (284-288). Verified: for a
certificate with one current pass no law fixes the grade (`NoEntryNoGrade` is the empty case,
`AFailureRefutes` the failed one, the others say what adds nothing); for three or more passes,
nothing either. GPT's counterexample (`nothing` for one pass) and Kimi's (three passes upgraded to
proved) both pass. The model happens to do the intended thing (certification_model.lut 54-55).
Whose: the theory's. Kimi's fix: a law per step of the fold, or `grade` defined in the theory.

C2. **`record` absorbs a re-check** (GPT, Perplexity, Kimi). `match known k (k.identity e) st {
just f -> st ; nothing -> cons e st }` (line 135), with the comment "so `--deep` rechecks and adds
nothing" (line 132), marked [proposed]. 6.S8 says "A new check never edits an entry: it writes a new
one, and both are kept, the latest in front"; 6.S15 and D-2026-10-12-m say writing a certificate is
idempotent. Verified. Whose: the specification's, two decided clauses that do not say which wins for
an exact replay (Kimi). Item 5 of the top screen.

C3. **Implications over a type** (all five). Worst: the two grade laws (eleven conjuncts, one of
them `c.entries == nil`). Then `AFailureRefutes` (line 270), `ACoveringPassServes` (324-325),
`ServesIsMonotoneInTheCutoff` (329), and the laws guarded by `not (k.serves d e)` (312, 314, 318,
321). Verified. Kimi's subtypes (`ServedEntry k d`, `CurrentFailure c`, `CurrentPass c`) are the
domains. Whose: the theory's.

### Raised by one or two

C4. **Budgets are not in the identity** (GPT). `Identity = { law, cone, binding, seed, cases }`
(line 86), while `NotRunFor` covers "fuel spent" (line 74) and `determined` requires one outcome per
identity (lines 115-119). The same test with little fuel (not run) and with enough (passed) has one
identity and two outcomes, so the intended store breaks `determined`; and `known` (line 127) makes the
first outcome final. Verified, and the spec says the same: 7.S13 "An entry whose identity, seed and
`n` match is reused whatever its outcome" and "A test is deterministic given its code, its binding,
its seed and `n`" (spec 7, line 114), which budgets falsify. Whose: the specification's (7.S9,
7.S13), copied by the theory. Item 5.

C5. **A current failure is bypassed by a serving pass** (Perplexity). The comment says "A failure at
the current hash, under any binding, refutes the law" (lines 141-143); `RefusalSaysWhy` gives `nil`
whenever `anyServes k.serves d es` (line 337), and `serves` never looks at other entries. Verified,
and the model reproduces it (certification_model.lut 70). Whose: the theory's. Item 4.

C6. **`transport` takes any standing as the identity** (Perplexity). `transport : Standing ->
Standing -> String -> Standing` (line 257): nothing says that `i` is a standing of A ≡ B, nor that
two sampled links share a distribution (6.S12, L10.8). Verified. Whose: the theory's; the
distribution part waits for the cost types (D-2026-10-13-m), the identity part does not.

C7. **An entry's grade is not tied to its evidence, nor a cases entry's reach to its cases**
(Perplexity). `gradedAsOutcome` (line 121) only requires a grade exactly when the entry passed.
Verified. A store read from `x.cert.json` with an assumed evidence graded proved is a valid `Store`.
Whose: the theory's.

C8. **The roles of `Value`** (DeepSeek, Kimi; Grok on all four `data`). See the contradictions:
`ReachesAsSets` states them; add "Roles: `ReachesAsSets`" at line 57. Kimi's weaker point stands:
nothing constrains the strings of `Failed` (the counterexample printed) and `NotRunFor` (the reason).
Whose: the file's comment for `Value`; the payloads are minor.

C9. **`HashSees*` ask a fixed-width hash to be injective** (Perplexity). Lines 235-241. True in the
abstract; the file chose it with "a collision of the hash function is the host's, and a sample that
finds one refutes the model" (lines 230-231, [proposed]). Under testing no sample finds one. Not a
defect; Perplexity's point that nothing ties the hash to a stated encoding stands as a weaker gap.

C10. **"the latest in front" has no law** (GPT). Line 111 versus `Store`'s two predicates (line 122).
Verified; a reversed list is a valid `Store` and `latestOf` then reads the oldest. Whose: the
theory's; minor while only `record` builds stores.

C11. **`Certificate` holds no domain, bound or evidence** (DeepSeek, against 6.S6). Line 147. The
file says domain and grade are read from the entries (6.S7, the grade is computed, not stored) and
bound and evidence are holes by D-2026-10-14-c (lines 36-43). A partial misreading; what remains is
GPT's point that chapter 6 predates D-2026-10-14-c (S6-1 below).

C12. Minor, one model each, verified: `agreesWith` compares outcomes only, so one identity with two
grades is allowed (Kimi, line 117); the index marks §5 "done" while `C`, `entryBound` and
`entryEvidence` are holes (GPT, lines 29, 41-43; the holes are top-level declarations, so the model
need not fill them, Kimi's not-sure). Grok's claims that `TransportOnTheIntersection` misses the
greatest lower bound and that `RefusalSaysWhy` leaves the state free are misreadings: coverage
equality over every `given` is the intersection, and line 339 gives the state exactly.

## certification_model.lut

CM1. **No law of `Certifying` broken** (GPT, Perplexity, Kimi, Grok; DeepSeek none). Verified for
`grade`, `serves`, `refuse`, `contains`, `transport` (lines 29-91). It reproduces C5 (line 70), as
the theory requires.

CM2. **NaN in `meet`** (Perplexity, not sure). `larger 0 NaN` is 0, so `meet` would give
`Interval 0 1` for an empty second interval. Resolved: 11.S7 says NaN is not a value of `Float64`
("NaN is not a number and is always an error"). Not a finding.

CM3. **`hashing` is an extern** (all, as not sure). Line 100; its laws are certified when
`cone_hash` is, like any extern.

## 10-world.md

S10-1. **10.S5 allows two applications to one token** (GPT). "gives a new token each time, so two
applications to one token are two nodes the memo never merges" (line 26) against D4 (used exactly
once). Verified. Whose: the specification's wording, older than D4.

S10-2. **"before it is applied, it is tested" and the agreement at the first application**
(Perplexity). Both in 10.S10 (line 43). The agreement protocol runs the action to compare, so a wrong
destructive action has acted before it is refused. Verified. Whose: the specification's; the
chapter should say which obligations are checked before the act (the type's laws, by sampling) and
which from the one act (agreement).

S10-3. **10.S12 (an extern with no law runs in a named world) against 6.S14 (no opt-out)** (GPT,
Perplexity). Line 47 against 06 line 60. Verified; L10.6 says such an exception would be O3.
Whose: the specification's; `world.lth` §6 is still todo, so nothing depends on it yet.

S10-4. **Own actions memoized and the token used once** (Kimi). 10.S6 (line 33) with 10.S4: if a
memo hit stands for an own action, which token comes after? Not stated. Whose: the specification's.

S10-5. **No obligation on observation** (GPT) **or on descriptions** (Kimi): part of W1.

S10-6. **10.S13's heading names `lib/world.lut`** (Kimi), while its text says `world.lth` (line 51).
Cosmetic.

## 06-certification.md

S6-1. **The chapter predates D-2026-10-14-c** (GPT; DeepSeek through 6.S6). It presents cost-valued
bounds and evidence as the current theory, and 6.S16 says "The file is not written" (line 66).
Verified. Whose: the specification's; a "current Boolean slice" paragraph would end the apparent
non-conformance of `certification.lth`.

S6-2. **⊤ "refused by every cutoff"** (Perplexity). Line 27: a preorder lets ⊤ itself be a cutoff,
and ⊤ ≤ ⊤. The listed law (`⊤ ≤ 0` false) does not exclude it. Verified. Whose: the
specification's; `OnlyAPassServes` already refuses failures independently in the Boolean slice.

S6-3. **"whether they should be two cost types is left to the library"** (Perplexity). Line 31,
against D-2026-10-13-m ("A certificate's bound is a `Distance` and its evidence an `Evidence`, two
types"). Verified; the chapter is older. Whose: the specification's.

S6-4. **"up to four"** (Perplexity). Line 39, under [implemented]: a description of today's code, not
a norm. A misreading as a P11 (every criterion is a parameter) violation.

S6-5. **6.S8 against 6.S15** (Kimi): C2.

## Not sure (unverifiable from the files)

- Whether the runner returns the token and the action's result out of band when it evaluates a
  `Host` law (Perplexity, Kimi). The comment at lines 249-259 says so; I did not read run.py's
  validation path.
- Whether `Supported` and `Cites` are rightly `settled` (GPT); it turns on W8.
- Concurrent changes between two observations (Kimi): out of scope until a world has other writers.
