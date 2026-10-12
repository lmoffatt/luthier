# 9. Specimens and the planner

Chapter 9 of the specification, draft 0, 2026-10-13. Sources: `docs/principles.md` L6, L9.8, L9.9, L10.7, L10.8, L11.1 to L11.3, L14.3, O1 and O4; `record/decisions.md` D-2026-10-11-m, D-2026-10-12-q, -u, -al and -am; `docs/spec/03-kernel.md` 3.S21 to 3.S28, `docs/spec/04-static-semantics.md` 4.R10 and `docs/spec/06-certification.md` §6, all at e8409ef; `src/luthier/` read only. Written by Claude Sonnet 5.5. It realizes L6, with L14.3 for the host as a specimen. What demands are and how a plan is run is spec 8; what an action may change is spec 10.

## §1 Notation

The common notation is `spec 1`. In this chapter: `f` is a function, `A`, `B`, `S` are specimens of one function, `C` is the type of costs and `⊕`, `≤`, `0`, `⊤`, `lift` are its five operations (spec 6.S5). `X`, `Y` are domains. A *distance* is the value of `C` that an identity certificate reports between two specimens, and an *edge* is a certified identity between two specimens. `r` is a measured resources record (time and memory, §4), `q` a ranking value, and `w` the weight the demand gives to resources.

## §2 Specimens

**9.S1. A specimen is a model of the function's type.** [decided D-2026-10-12-l] A function has a type with laws; each implementation of it is a specimen, a model of that theory certified against those laws like any other (spec 4.R10, spec 6.S1). A specimen may be written in Luthier, be an extern (spec 10), or come from another library; it has its own precision, speed, memory and place of execution (L6.1). The word specimen is only for the planner's candidates; what the type names is a model.

**9.S2. Today nothing chooses.** [implemented] The interpreter holds several implementations of some functions, for instance the declarations of `array.lut` and the numpy externs of `array_python.lut`, but a name is bound once and evaluation uses that binding. No code looks for a second specimen of a name, ranks two, or substitutes one for another. Everything below that selects is `[decided]` or `[proposed]`.

**9.S3. The host is a specimen.** [proposed] Where Luthier states a theory and the host implements it, the host's code is a specimen of the statement, certified against it (L14.3, spec 6.S16). The extern of L11.1 is declared over a type with laws and validated against them before it is applied (L11.2); one that cannot be validated (spec 10.S10) is no specimen, and the planner never offers it. The bridges between a native representation and the host's are spec 3.S22 to 3.S28.

**9.S4. A law is the characterization, agreement is a corollary.** [decided D-2026-10-05-a] Two specimens are not made equivalent by being compared with each other alone; each is certified against the laws (spec 4.R10), and their agreement is a separate certificate (§3). Rerunning to get identical bits shows only that the code is unchanged, a certificate kept apart from the one against the laws (L9.8).

## §3 The class of a function

**9.S5. An edge is a certified identity.** [decided D-2026-10-11-m] Two specimens `A` and `B` are joined by an edge when the identity law of their function type, with result `Bool` or `C`, has a certificate (spec 4.R8, spec 6.S2). The certificate holds the domain `Y` on which it was obtained, the distance and the evidence (spec 6.S6).

**9.S6. The class is the connected component.** [decided D-2026-10-11-m] The class of a specimen is the set reachable from it along edges; it is not the set of everything that passes the laws. Closeness of values with a distance is not transitive, so a class has no single representative: if A and B are both joined to S, each may replace S while neither replaces the other (L6.5, L6.6).

**9.S7. A lone specimen is never replaced.** [decided D-2026-10-11-m] A specimen with no edge has a class of one, and the planner offers only it. What the author freely chose where a function was under-determined stays (L6.10, D-2026-10-11-d); the planner chooses only among what has been compared.

**9.S8. Two regimes.** [proposed] On a decidable carrier the identity is `Bool`, the distance of an edge is `lift true`, which is `0`, and the quotient is exact. On a carrier with a distance the identity is valued in `C`, and precision can be exchanged for resources up to what the demand tolerates (L6.4).

## §4 Substitution

**9.S9. Substituting A by B is transport along a path.** [decided D-2026-10-12-q] The planner runs `B` in place of `A` when there is a path of edges from `A` to `B` whose certificates are all valid at the input. What the result then carries is spec 6.S11 and 6.S12: the certificate of `B` composed link by link with `⊕`, on the intersection of the domains of its links, at the weakest grade among them. The planner adds nothing to those rules. A link has a domain, so a path exists at an input only where every one of its links does (L6.9).

**9.S10. The demand decides whether the path is enough.** [decided D-2026-10-12-h] A substitution is accepted when the composed certificate meets the demand's cutoff (spec 6.S15). Sampled links from a single distribution compose with the union bound; links from unlike distributions need a law that ties those distributions together first (spec 6.S12, L10.8). To refuse sampled paths, a demand sets its evidence cutoff accordingly; that cutoff is the demand's parameter, never the planner's (L6.2).

**9.S11. The tolerance charged at a specimen.** [proposed] The tolerance a specimen may use comes from the demand's, carried back through the cone's sensitivity between that specimen and the demand (L6.8). With no known sensitivity the planner does not substitute; the specimen demanded is the specimen run.

**9.S12. A path is memoized by its links.** [proposed] A path found for a demand is a value of the plan (spec 8). Writing an identity certificate is idempotent and memoizable, by D-2026-10-12-m; the planner does not repeat a comparison whose certificate is in the store and still valid for the same hash (spec 6.S8). In-place mutation of a parameter is a choice of the plan, allowed when the before value has no other consumer (D-2026-10-10-e).

## §5 What is ranked

**9.S13. Resources are measured and recorded.** [proposed] A run of a specimen records its resources: time and memory, with the machine and the host library versions that bind them (L11.4). The record is kept apart from the certificate, in the store Luthier owns, keyed by the specimen's hash and the shape of the input, since resources are not a law of the function (L6.2). The estimate the planner uses is read from these records (L6.1); how it extrapolates to an input never measured is the library's.

**9.S14. The ranking is a library's.** [decided D-2026-10-12-al] The planner ranks the specimens of a class that the demand admits. Which function ranks, and how a measured sample becomes an estimate, is decided when the library is implemented (O1). The core asks of the library:

| operation | used for | laws |
|---|---|---|
| `rank : C -> R -> W -> Q` | the value of a specimen from the cost its path carries, its resources `r` and the demand's weight `w` | monotone in the cost and in the resources: a worse cost or more resources never ranks better |
| `≤` on `Q` | choosing the best specimen | a total preorder |
| `0` of `C` | a specimen whose path carries no cost | at equal resources it ranks no worse than any specimen whose cost is above `0` |

[proposed] `W` is the type of the demand's weight and `R` of the resources; the core uses nothing else of them. No subtraction, normalization or particular scale is asked. Nothing here fixes whether the weight multiplies, adds or is an exponent.

**9.S15. First candidate model.** [proposed] D-2026-10-12-u offers, as a candidate and not as the rule, ranking by `cost + w · log resources`, minimized, which equals maximizing `exp(−cost) / resources^w` (L6.3). A specimen of cost `0` then ranks by its resources alone and not at zero. It satisfies the table of 9.S14 where `⊕`, the order of `C` and the logarithm are those of the reals; a library of costs that takes another algebra (spec 6.S5) provides its own model of `rank`.

**9.S16. The weight and the cutoff are the demand's.** [decided D-2026-10-12-h] `w`, the cutoff and the confidence δ belong to the demand (D-2026-10-12-r); the planner has no defaults of its own and reads them from the demand, so that the same program under two demands may run two specimens (L6.2, P11).

## §6 The planner in Luthier

**9.S17. `lib/planner.lut`.** [proposed] The theory of this chapter, to be written over the parameter `C` of spec 6.S4: the record of an edge, with the two specimens and their certificate; the relation "reachable along valid edges at an input" and its law that it is reflexive and transitive; `substitute`, whose law is that the result's certificate is the transport of spec 6.S11 and nothing stronger (spec 6.S13); the theory `Ranking` of 9.S14 with the candidate model of 9.S15; and `choose`, whose law is that it returns a specimen of the class that the demand admits and ranks first. The file does not exist. `src/luthier/lib/plan.lut` is a different object, the schedule of a dataflow and its confluence law, and is cited by spec 8. The Python that chooses, once written, is a specimen of this file (L14.3, 9.S3).

## Open

- O1, the algebra of costs and so of ranking (9.S14, 9.S15).
- O4, the composition of invariances: which identities compose along a path (9.S6, 9.S9).
