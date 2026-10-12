# Recommendations on `docs/principles.md` from six IA critiques

2026-10-12. Written by the model from the critiques Luciano collected in
`record/IA/principles 2026 10 12/` (commit 1429f35: claude.md fb064492ef3c, deepseek.md
b7b376ebdb3e, gpt en.md c90578fce88d, gpt sp.md acf2562a9d6e, kimi.md 42e096742af6, Overall
assessment.pdf e7d4b6fe6018, which is Perplexity's answer; perplexity.md is empty) on draft 10 of
`docs/principles.md` (b7a7e23). The questions put to the IAs were: detect redundant or missing
principles; detect contradictions; can we reduce the number of principles; advice for a better
document; and, to Claude, GPT en, Kimi and DeepSeek, whether the G0–G3 layer does any good or the
Ls alone should be listed.

What comes from a critique is cited by the IA's name. What the model proposes is marked
*proposed*. The criterion for ranking the recommendations is the one Luciano set in the session:
not which critique is most reliable in its facts, but which suggestion makes the document more
intelligible to its reader. The reader named in the document's header is the agent that builds the
specification, so the ranking says what that reader gains from each suggestion.

## 1. What the six agree on

**Redundancy.** All six name the same cluster as the largest repetition: L5 (equality has levels),
L7 (a law is verified by one operation), L13 (one function, many paths) and L14 (Luthier
orchestrates other languages) each restate how certification transports along a certified identity
(sum of costs, weakest grade, intersection of domains). After it: G3 and L10 (the demand), G1 and
L2 (type as theory, membership as guarantee), L9 and L11 (pure evaluation, actions). Kimi adds that
the certificate grades are defined in five places (Terms, L2, L6, L7, L14); Claude adds that single
entries repeat themselves (L9 says "a mutable parameter is two variables" twice; L10 says "program
kept, computation redone" three ways) and that decision D-2026-10-11-n is written out five times
instead of referenced.

**Contradictions**, by how many IAs see each and whether they agree on the resolution:

| Contradiction | Seen by | Resolution offered |
|---|---|---|
| L5 lets any link compose into a path; L13 forbids summing a sampled edge | DeepSeek, Kimi, GPT sp, GPT en, Claude | Split. DeepSeek, Kimi, GPT sp keep L13's prohibition. Claude: under G2 a sampled link is a cost with a grade and costs compose, so the path exists at grade `sampled`; refusing it is the planner's default policy, which the demand sets |
| L13 calls the implementations a quotient or class, then says closeness is not transitive and the planner works on a weighted graph | DeepSeek, GPT en, GPT sp, Perplexity, Claude | Unanimous: exact identity gives a class; approximate identity gives a graph. GPT sp's wording: "semantic equivalence forms classes; certified substitutability forms a graph" |
| L14 says an extern without a law is not applied, then lets it run inside a named world | DeepSeek, GPT en, GPT sp | Unanimous: it may execute inside a world; it may not enter the planner's substitution graph nor a certified theory |
| Status mixed inside one entry ("settled by his correction… proposed, candidate" in L14); Terms declare the setoid that "What is open" says is unresolved | Kimi, GPT en, GPT sp, Perplexity, Claude | Unanimous: one status per normative unit; nothing unresolved stated declaratively in Terms |
| Where the cutoff lives: L3 (constructor parameter), L6 (only in the demand), L13 (pulled back per node) | Kimi, GPT en, Claude | GPT en: the demand's. Claude: the demand's, passed down to the constructor; L6 reads "only in the demand, or passed from it" |
| What `a : A` asserts when the certificate is `sampled` or `assumed`; whether an `assumed` value is a model, a hole, or neither | GPT en (its first priority), Perplexity, Claude (as apparent) | GPT en: separate truth from evidence; `a : T [g]` means supported at grade g, not `a ⊨ T` |
| "Type" has two meanings: a kernel structure (Terms) and a theory (G1) | GPT sp, Claude | Kernel types are structures; Luthier types are theories; GPT sp writes Theory(S, L) |
| "Cost" has two meanings: the valuation of a law (G2) and the resources that rank candidates (G0, L13) | Claude | Reserve *cost* for the law, *resources* for time and memory |
| "Model" is overloaded: R13 refuses two models on one type while the planner "chooses among the models certified equivalent" | Claude | *Model* for what a type names; *specimen* for the planner's candidates |
| The grade of a sum: a vector (L6, each at its grade) or a scalar (L13, the weakest) | Claude | Decided by the open item "the grade as a lattice" |
| L6 calls `lift` and `exact` homomorphisms Bool → Cost, but `or` would need `min`, which is not among Cost's operations | GPT en, GPT sp | Do not call it a homomorphism until the algebra is fixed |
| `test` is an action, actions are never served from the memo, yet a test is memoized by its certificate | Claude | Actions on Luthier's own state are idempotent and memoizable; actions on the world never are |
| L9 "statements commute" against binding order inside a block | GPT en, Perplexity | After elaboration, independent nodes commute |
| L11 "an action is verified" against its body, which says external irreversible effects are audited, never verified | GPT en, Perplexity, Kimi | Verified where observable, audited otherwise |
| L12 "no hardcoded constants" against the kernel's 0, ∞, `lift`, `exact` | DeepSeek | "No unrecorded policy constants"; kernel primitives and mathematical constants excluded |

**The G layer.** The four asked agree that the present state is the worst one: a layer that
organizes nothing (no L is listed under a G), carries mechanics (`lift`, `exact`, `within`
copied into L6), has its own statuses and its own renumbering. They split on the remedy. GPT en
and DeepSeek dissolve the Gs into a short unnumbered orientation. Kimi keeps them as "commitments"
with no mechanism, each ≤ 5 sentences, with a test for what is a G and what is an L: can an
implementer violate it? If yes, it is an L. Claude keeps them only if they do a job the Ls cannot,
and names it: precedence. When two Ls conflict, the G they derive from decides; when Gs conflict,
G0 decides. All four send the history of the eurekas to the record.

**Reduction.** All six say yes: DeepSeek 10–12, Kimi 10, GPT sp 10, Perplexity 8–10, GPT en 8
plus a mission and a stance, Claude 11 L plus 3 G. They differ more in the shape than in the
count: Kimi and DeepSeek merge pairs inside the present numbering (L2+L7, L4+L14, L5+L13, L9+L11,
L10+L12); GPT en and Perplexity change the level, separating principles from derived rules and
from specification, so that L10 and L14 stop being principles because they are chapters of the
spec; GPT sp promotes the sentence buried in L10, "meaning, realization, evidence: three objects,
never one", to a principle; Claude adds an entry for the certificate, the object every L leans
on, now scattered over L2, L5, L7, L10, L13, L14. Where the merge maps coincide: L9+L11,
G3+L10+L12, L15 stays, L1 becomes the preamble. Where they do not: where L7 goes, and whether L4
merges with L14.

## 2. Recommendations for an intelligible document, ranked for the agent that reads it

1. **Mark what is fixed and what the specification may refine.** (GPT en, Perplexity: a layer of
   derived rules between the principles and the spec.) Today the memo identity of L10 sits inside a
   settled principle, so the agent treats it as untouchable; as a derived rule under "the demand
   determines the computation" the agent knows the spec can refine it. This tells the reader its
   degree of freedom at every point. No merge of pairs gives that.
2. **One status per sentence.** (All six.) For the agent this decides what is implemented; "settled…
   proposed, candidate" on one line forces a guess. Kimi's numbered clauses (L10.1, L10.2) are the
   mechanism: each clause carries its status and can be cited and tested on its own, without
   splitting an L into ten entries.
3. **A tie-break rule.** (Claude.) A human reader who meets L5 against L13 asks Luciano; the agent
   chooses silently and goes on. Precedence matters more for the agent than for a human reader. It
   does not need numbered Gs to exist: one line suffices, *the statement decides over its clauses;
   between statements, the lower-numbered L*.
4. **Which settled principles rest on something open.** (Kimi: a dependency map; four settled
   principles rest on G2's open cost algebra.) It tells the agent where to leave a parameter in the
   spec instead of fixing a value. Only Kimi proposes it.
5. **Each term in one formal category, defined once.** (GPT sp's list: Structure, Theory, Model,
   Law, Certificate, Plan, Demand, Action, World, with Theory(S, L); Claude's *specimen* and
   *resources*; Kimi and DeepSeek: grades defined once, in Terms; GPT en: nothing unresolved
   appears declaratively in Terms.) The terms pass into the spec as they are; two senses of "type"
   in the principles become two senses in the spec.
6. **One home per mechanism, cross-references elsewhere.** (All six.) Duplication is where the
   contradictions hid: the transport rule in L5, L13 and L14 drifted apart.
7. **Open questions listed with the principle each one blocks** (Kimi), apart from Luciano's
   pending marks and from the changelog (Claude's three-way split; GPT en's four-way). What is open
   tells the agent what not to fix; the changelog is noise for it and belongs in `decisions.md`.
8. **A fixed shape per entry**: statement in one or two sentences, consequences, references,
   status. (Claude, DeepSeek, Kimi, GPT sp, GPT en.) The header of draft 10 already promises it
   (Kimi) and the body does not keep it.
9. **A reference key** for P, R, D ids and spec sections, and no names the agent cannot resolve
   ("Kimi", "the third round"). (Claude.) Mostly solved by taking the provenance out of the
   projection.

Where the model disagrees with the critiques. Claude, DeepSeek and GPT sp move the worked examples
to an appendix. *Proposed:* keep them attached to their entry in a field of their own. For the
agent the example y = 11 after rebinding defines the semantics of `<-` better than the paragraph
does; a short statement with the example at hand reads better than a short statement with the
example three pages away.

What counts little for intelligibility: the old-to-new numbering table (it matters for the record,
not for reading today's document; Claude and Kimi ask for it, DeepSeek asks to freeze ids, GPT sp
to drop the old numbering); the total length (Claude asks for a third fewer words; what harms the
agent is duplication, not volume); diagrams (Kimi's dependency diagram, GPT sp's formal one; a
list of dependencies in text serves the agent as well); and the two lints Claude proposes for
`--check` (every reference resolves; no sentence in two entries), which are process, not
intelligibility, and are weighed separately below.

## 3. The proposed shape

*Proposed*, taking GPT en's single hierarchy as the form, Kimi's two mechanisms inside it, and one
line of precedence. The three sit at different levels (form, addressing, conflict) and do not
compete.

1. **Purpose.** One sentence: Luthier expresses the invariances of the disciplines (today L1).
2. **Orientation.** One short paragraph with what G0–G3 say today, unnumbered, no status, no
   mechanics. The history of the eurekas stays in the record.
3. **Terms.** Only settled definitions, each term in one category, grades defined here and nowhere
   else.
4. **Principles.** Under Luciano's six topics. Each entry: tag and statement (one or two
   sentences, the fixed part); numbered clauses (the derived rules, each with its own status); an
   example field where one exists; references (spec section, D ids); what it derives from and
   what open item it rests on.
5. **Precedence.** One line: the statement decides over its clauses; between statements, the
   lower-numbered L.
6. **What is open.** Only questions whose answer changes the language, each with the principle it
   blocks. Luciano's pending marks in a list of their own. The changelog to `decisions.md`.

The count of principles follows from applying the shape to the six topics and is not chosen in
advance. The merges the critiques agree on (L9+L11; G3's content into L10+L12; L1 to the purpose)
and the certificate entry are expected to fall out of step 4.

## 4. Decisions that are Luciano's

Each touches a settled principle or a term, so one commit does not undo it.

1. The shape of section 3, or a different one. (The alternative with the most support among the
   critiques: Claude's three Gs of two sentences each as the precedence layer, each L listed under
   its G.)
2. Sampled links: compose at grade `sampled` by G2, refusal being a planner policy set by the
   demand (Claude; P11, every criterion is a parameter, supports it), or never summed into a path
   until a probabilistic bound exists as a law (DeepSeek, Kimi, GPT sp, and L13 today). Touches
   L5 and L13, both settled.
3. The cutoff: the demand's, passed down to L3's constructor (Claude), or removed from the
   fundamental subtype construction (GPT en).
4. The grade of a sum: a vector of grades (L6) or the weakest (L13). The open item "the grade as a
   lattice".
5. What `a : A` asserts at grade `sampled` or `assumed`: *proposed*, "supported at grade g", not
   truth; `assumed` permits reasoning and does not make `a` a model. (GPT en.)
6. A law is the proposition; a certifier is a method that produces evidence for it; one law may
   have several certifiers. (GPT en.) Today L3 and L7 read as if every law were executable.
7. Vocabulary: *structure* for a kernel type and *theory* for a Luthier type; *cost* for the law
   and *resources* for time and memory; *model* for what a type names and *specimen* for the
   planner's candidates. (GPT sp, Claude.)
8. Actions on Luthier's own state are idempotent and memoizable; actions on the world never are.
   (Claude.)
9. L12 becomes "no unrecorded policy constants", excluding kernel primitives and mathematical
   constants. (DeepSeek.)
10. The two lints in `--check`, now or after the record is current. The rule in `CLAUDE.md` admits
    a mechanism with a recurring cost only after a real case it would have caught; the cases
    exist (G0 sends the ranking of candidates to G2, which Kimi caught and a reference lint would
    have; D-2026-10-11-n written out five times, which a duplicate-sentence lint would have). The
    cost falls on each commit, not on Luciano's attention.

## 5. Order of execution

The record (`record/principles-language.md`) still carries the old numbering (G1 demand, G2
theory, G3 cost) and the header of draft 10 says the projection was written by hand. Until the
record is the source again, every edit in `docs/` is by hand and the duplication returns. So the
order is fixed by that, not by the critiques:

1. Update the record from draft 10 (renumbering, today's merges, his marks) until `--check`
   passes.
2. Extend the projector for numbered clauses with their own status and for the example field; add
   the two lints if decided.
3. Apply the shape of section 3 in the record: entry format, grades in Terms only, examples into
   their field, provenance out of the projection, "What is open" split, reference key.
4. Apply Luciano's decisions 2–9: the merges, the resolutions of the contradictions, the
   vocabulary. Regenerate; check `docs/principles-for-readers.md` against the new numbering.
5. Tag draft 11.

The plan proper, in its two documents (decisions for Luciano, execution for the sessions), is
written after his marks on this one.

## 6. Decisions the model took on its own

- The ranking criterion of section 2: the agent that builds the specification as the reader.
- Keeping the examples attached to their entry, against three critiques.
- Taking GPT en's hierarchy as the form and importing only what fills a gap in it (Kimi's
  clauses and dependency map, one precedence line), nothing that competes with it.
- Not fixing the count of principles in advance.
- Leaving perplexity.md empty and naming the PDF as Perplexity's answer here instead.
