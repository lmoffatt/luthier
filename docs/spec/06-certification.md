# 6. Certification

Chapter 6 of the specification, draft 0, 2026-10-12. Sources: `docs/spec/05-static-semantics.md` §7 and `docs/spec/03-libraries.md` §4 at bd4537e; `docs/principles.md` L9 and L10 at 2b79c02; the decisions D-2026-10-11-f, D-2026-10-11-n, D-2026-10-12-h, -k, -m, -q, -r, -t, -y, -ag, -ak and -al; `src/luthier/testing.py`, `certify.py` and `cli.py`, read only. Written by Claude Opus 5.5, the session integrating the specification, as wave 2 was reshaped by D-2026-10-12-al: `Cost` is a library, and this chapter states certification over a cost type it takes as a parameter, fixing only what it asks of that type. It realizes L9 and L10, in Luthier where the kernel can say it (L14). How a test draws, counts and records its cases is spec 7; what the files hold and what an importer accepts is spec 12.

## §1 Notation

Notation shared by every chapter is `spec 1`. Here: `C` is a type of costs, the parameter of the chapter (§3), and `c`, `c′` are values of it. `≤` is the order of `C`, `0` its least element, `⊤` its greatest, `⊕` the composition of two costs along a path, and `lift : Bool -> C` the reading of a Boolean verdict as a cost. `X`, `Y` are domains: a subtype, a list of cases, or a distribution sampled. A *cutoff* is what a demand requires of a certificate (D-2026-10-12-h): a largest bound and a largest evidence cost, both values of `C`. `h` is the hash of a dependency cone (`spec 3.S34` gives the canonical form it is computed over).

## §2 What is certified

**6.S1. A law over a domain, never a name.** [implemented] The thing certified is a law of a name's type, applied to the values that law quantifies over, on some domain. A definition counts as certified when each law its type states has a passing entry; `check -v` summarizes the entries of a name, and that summary is not a state the name keeps once and for all. The obligations a type raises, and which of them are laws and which coercions, are `spec 4`.

**6.S2. Law, certifier, certificate.** [decided D-2026-10-12-k] The law states; the certifier is how evidence for it is obtained, and a law can have more than one: citing a theorem, running every case, running listed cases, sampling, or assuming. A certificate is the record of what one certifier established (§4). When a law quantifies over infinitely many values, no run reaches all of them: such a law is cited, sampled or assumed, and its certificate says which.

**6.S3. Three outcomes.** [implemented] A law run by `test` passes; fails, by a counterexample, by an error while evaluating a case, or by a generator giving a value outside its type; or is not run, when a parameter has no generator, no case could be drawn, the reduction ran out of fuel, or a hole without a value blocks it. A definition passes when all its laws pass, fails when one fails, and is not run otherwise. Only a pass certifies.

## §3 What certification asks of costs

**6.S4. Certification takes its cost type as a parameter.** [decided D-2026-10-12-al] The theory of this chapter is written over a type `C` and the operations of §1, not over a fixed `Cost`. A library of costs supplies models of `C`; which algebra it uses, how a sample's statistics become a cost and what its operations are called are decided when that library is implemented. This chapter fixes only what it uses.

**6.S5. Five operations and their laws.** [proposed] Certification uses exactly these, and asks of them these laws, so that a library of costs is a model of them:

| operation | used for | laws |
|---|---|---|
| `≤` | comparing a certificate with a cutoff (§7) | a preorder |
| `0` | a check with no error and no doubt: exhaustive, proved | least element |
| `⊤` | a failed check, refused by every cutoff | greatest element, absorbing for `⊕` |
| `⊕` | composing bounds and evidence along a path (§6) | associative, unit `0`, monotone in each argument |
| `lift` | a law valued in `Bool` | `lift true = 0`, `lift false = ⊤` |

No subtraction, product or inverse is asked: nothing in certification takes evidence away (6.S13). Turning what a sample observed into a cost (L10.3) belongs to the library, with the shape D-2026-10-12-r gives it. Of the two algebras of D-2026-10-12-p, max and the plain sum satisfy the laws asked of `⊕`; the averaged forms with 1/n do not, since an average of averages is not associative, so a library that takes them needs another `⊕` along a path. That choice is the library's. The names D-2026-10-12-n listed as primitives (0, ∞, lift, exact) are the table's `0`, `⊤` and `lift`. The bound of a certificate and its evidence cost are both values of `C`; whether they should be two cost types is left to the library.

## §4 The certificate

**6.S6. What a certificate holds.** [proposed] As a value of a record type `Certificate C`: the law; the domain it covered; the bound observed (for a law into `C`, the worst cost seen; for a Boolean law, `lift` of its verdict); the evidence, an evidence cost in `C` (D-2026-10-12-r) with the grade derived from it (6.S7); and the identity, the hash `h` of the cone with the binding of spec 7.S9. [implemented] Today an entry of `x.cert.json` (spec 12.S10) holds the law's label, its outcome, the mode and count it ran with, the generators and their fingerprints, the seed, the first cases, the time each law took, and `h`; the bound and the evidence cost are not recorded.

**6.S7. The grade is a view of domain and evidence.** [decided D-2026-10-12-r] The grade is computed, not stored apart. A proof or a run of every case gives evidence `0` over the whole domain. A run of listed cases gives `0` at those cases and `⊤` at every other value. A sample gives the cost the library converts its statistics to. An assumption gives the cost the demand assigns to assumptions (6.S10). A person reads the five names; the planner reads the costs. [proposed] The correspondence of the older names (point, census of k, bounded, witnessed) to these five is a function of `lib/certification.lut` (6.S16), so that spec 1.S12 cites it; D-2026-10-12-ag left its place to be settled when these laws are written, and this is the proposal.

**6.S8. A certificate is identified by its cone and frozen.** [implemented] The hash covers the code of the cone in canonical form, the host code behind each extern it calls (the source files of the module's directory, or the installed package and its version) and the interpreter; any change to one of them makes the entry stale (spec 12.S11). An entry is kept per filling of the holes its cone depends on, up to four. [proposed] A new check never edits an entry: it writes a new one, and both are kept, the latest in front (L10.4). Today the new entry replaces the old one with the same hash in the file, and the chain exists only in the history of the repository.

## §5 Certifiers that run nothing

**6.R1. Proved by citation.** [implemented] `cite name ref checked who` records a certificate of grade proved for the laws of `name`: `ref` must be a value of `Reference`, read from a `.bib` file (spec 12.R1), and `who` says who checked that the theorem cited matches the laws, `human`, `ai+human` or `none` (D-2026-10-11-f). It is allowed in user code. The certificate holds the reference and who checked; `test` runs no case for a cited name. In the language designed `cite` is a function of core with named arguments (spec 2.S21), and its syntax is O10.
Files: cite_proved.accept.lut, cite_not_reference.reject.lut.

**6.S9. Proved by delegation.** [proposed] A host library's documented guarantee is cited as the theorem, with its hypotheses (a condition number, the library's version and the platform) carried by the certificate: LAPACK's backward-error bound for a solve, say. This is citation with a theorem outside Luthier, and adds no grade (L9.7).

**6.S10. Assumed.** [decided D-2026-10-12-t] Nothing is checked; the certificate records the assertion itself. For a Boolean law the assertion is that it holds, and the bound is `0`. For a law into `C` it is a formula of the inputs, and the bound is that formula's value at the input. The demand sets the evidence cost of assumptions, with no default, so a demand that names none refuses every assumed value. A formula that some source guarantees, cited with the conditions it needs, makes the certificate 6.S9 instead. [implemented] The laws of an `axiom` (spec 11.R3) are assumed: stated, never tested, and `check -v` says so (spec 4.S19).

## §6 Transport and composition

**6.S11. Along an identity.** [decided D-2026-10-11-f] Let B be certified on X with bound `c` and evidence `e`, and the identity of A and B certified on Y with distance `c′` and evidence `e′`. Then A is certified on the intersection of X and Y, with bound `c ⊕ c′`, evidence `e ⊕ e′`, and the weaker of the two grades; on nothing outside that intersection. When the identity law is valued in `Bool` (structural `==`, spec 4.R8), `c′` is `lift true = 0` and the certificate of B transports exactly; when it is valued in `C`, the distance observed is added. This is the only operation of §3 that transport uses. The example of L10 is a lookup table that agrees with the native definition at the points of a grid: the intersection, and so its certificate, is that grid.

**6.S12. Along a path, and sampled links.** [decided D-2026-10-12-q] A path of identities composes link by link with `⊕`. Two links sampled over one distribution compose by the union bound, their failure fractions and their δ summed; two links sampled from different distributions need a law that relates those distributions before they compose. A demand that refuses sampled paths says so by its evidence cutoff.

**6.S13. No evidence for free.** [proposed] As a law of the theory of 6.S16: every operation on certificates is monotone, so a better grade, a smaller evidence cost or a wider domain comes only from a new check (L10.9). It is the reason 6.S5 asks `⊕` to be monotone and asks for nothing that subtracts.

## §7 The demand

**6.S14. Demanding a value demands its certificates.** [decided D-2026-10-11-n] Every name in the dependency cone of a demanded value must be certified, each certificate paid once through the memo. What no demand reaches needs none. `test` demands certificates without values, and `test` of a module demands every name it defines (D-2026-10-12-ad). There is no opt-out (D-2026-10-12-y): if any name of the cone lacks a certificate, or is provisional (spec 4.R5), the demand is refused, and `run`'s refusal is spec 12.S17.

**6.S15. A certificate serves a demand when it meets the cutoff.** [decided D-2026-10-12-h] The demand states the cutoff; the certificate meets it when its bound is `≤` the cutoff's bound and its evidence `≤` the cutoff's evidence, in the order of `C`. A certificate taken from the memo is compared with the demand that hits it, at the hit. A certificate issued for one cutoff serves every demand it meets. Writing a certificate is an action on Luthier's own state, idempotent and memoizable (D-2026-10-12-m).

## §8 Certification in Luthier

**6.S16. `lib/certification.lut`.** [proposed] The theory of this chapter, written over a parameter `C`: the theory `CostAlgebra C` with the operations and laws of 6.S5; the record `Certificate C` of 6.S6; the function `grade` of 6.S7; `transport` of 6.S11 and `compose` of 6.S12; `serves` of 6.S15; and their laws, among them monotonicity (6.S13) and that `serves` is monotone in the cutoff. The file is not written. The host's `certify.py` and `testing.py` are its specimen, certified against it (L14.3), and each library of costs gives a model of `CostAlgebra`. Once its laws are written, L9 and L10 are read back from them (D-2026-10-12-ag).

## Open

- O1, the algebra of costs, now the library's (6.S5).
- O3, for 6.S14.
- O10, the syntax of citation (6.R1).
