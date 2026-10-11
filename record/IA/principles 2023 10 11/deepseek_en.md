The draft is unusually self-aware and labels many tensions as open. But several of them are not merely open questions: they are incompatible design commitments that will block a coherent implementation unless one side is weakened or the core calculus is changed.

## Main contradictions that will hamper implementation

1. **G0’s propositional type theory vs G3’s cost-valued laws.**  
   G0 says a type is a proposition and a value is its proof; laws define mathematical objects and quotients by exact equality. G3 says laws are valued in `[0,∞)`, truth is graded, tolerance comes from the demand, and evidence composes Bayesianly.  
   Consequences: L2’s “membership is a guarantee” becomes “membership has a cost”; L4’s certified subtype from a predicate cannot be a simple `Maybe` subtype; L10’s quotient by a law’s equality depends on the demanded tolerance; L15’s `Real → Float64` only works if `Float64` is an approximate model, not a model in the ordinary sense.  
   Implementation impact: you cannot implement a standard dependent type checker. You need a graded/quantitative type theory with a cost semiring, approximate equality, and coherence conditions for substitution under tolerance.

2. **G2’s “function type is its laws” vs L5’s “laws need not determine.”**  
   G2’s source says laws must determine the function uniquely. L5 retouches this: laws accumulate, and determination is “the limit, not what it must reach.”  
   Consequences: if laws underdetermine a function, then L10’s “one class per mathematical function” is false: two implementations can satisfy the same laws but compute different functions outside the tested domain. L14’s external validation against laws becomes unsound. L21’s certificate of the law certifies only a description, not the function.  
   Implementation impact: either laws must be strong enough to determine function identity, or L10’s quotient/path-optimization must be weakened. As written, replacing one representative by another is not justified.

3. **Static/declarative universality vs demand-driven certification and elaboration.**  
   G1 says the declarative face is universal and minimally processed. L19 says the demand determines computation, the plan runs backward from actions, tests are actions, and “what never reaches an output needs no certificate.” L13 says the demanded return type selects which law to derive and what to forget. L20 says modules are instantiated on demand with the parameter threaded from the action.  
   Consequences: type checking, certification, and even which law a function derives can depend on use. A function’s type/behavior can vary by context. L8’s “no value inhabits an undefined type” becomes demand-relative: an undemanded function may never be certified.  
   Implementation impact: this requires whole-program demand analysis, bidirectional elaboration, and probably dynamic certification. Separate compilation, libraries, and dead-code checking become much harder. It contradicts the usual static guarantee in L2.

4. **L18’s pure definitions vs G3’s evidence kept across runs and L12/L19’s actions.**  
   L18 says a definition has no effects; its result depends only on inputs. G3 says evidence is kept across runs and composes as Bayes. L12 says execution is an action on the world. L19 says tests are actions, so verifying is demanding.  
   Consequences: if kept evidence affects law values or path choice, it is a hidden input or an effect. L19’s memoization key is “hash of code, inputs and mode” and does not include the evidence database.  
   Implementation impact: purity and memoization become unsound unless evidence is an explicit parameter/effect and is included in the cache key. The test framework also needs graded pass/fail, which contradicts W6’s Boolean “must fail when wrong.”

5. **Module/theory/model terminology is inconsistent.**  
   The terminology says a module is “a file as a namespace, until modules are values.” L20 says “modules are values” and a parametrized module is a function from models to definitions. L8 says a theoretical module has types, functions, laws, and no values.  
   Consequences: it is unclear whether modules are namespaces, first-class values, functions, or collections of holes. L20 also mixes “function universal over models” with “a carrier with two models is two types,” plus implicit model resolution, on-demand instantiation, and bridges by cost.  
   Implementation impact: the module calculus, model resolution, and instantiation strategy are underspecified. This is a major implementation blocker for separate compilation and type checking.

6. **L16’s rebinding vs L9’s DAG and commuting statements.**  
   L16 says `:=` is once and `<-` is rebinding: after `<-`, the name equals the term “until the next `<-`.” L9 says the program is a DAG, dependencies give the only order, and statements commute.  
   Consequences: `<-` introduces sequencing/state unless it is pure shadowing encoded as SSA. The open item about session blocks admits this is unresolved.  
   Implementation impact: the parser/elaborator/runtime need a clear semantics for blocks, shadowing, and DAG construction. Without it, “statements commute” and `<-` rebinding cannot both be true.

7. **Certification, memoization, and forgetting conflict.**  
   L11 says a certificate is hashed over its dependency cone. L19 says results are memoized by code/inputs/mode, and “computation is the expansion and is redone.” L13 says runtime forgetting frees nodes after their last consumer. L21 distinguishes identity certificates from law certificates.  
   Consequences: if dependencies are forgotten, certificate verification may require recomputation. If evidence changes, the hash must include evidence. If a law certificate travels by an identity certificate, identity must include evidence or the law certificate becomes stale.  
   Implementation impact: cache invalidation and certificate composition are unspecified. This can produce unsound reuse of results or certificates.

8. **L7’s minimal core vs load-bearing features.**  
   L7 wants a minimal core executable by hand. But G3’s cost-valued laws are load-bearing for G0 and G2. L6 wants code-as-data and an interpreter in the language. L14 wants FFI to Python. L20 wants first-class modules, theories, models, and bridges.  
   Consequences: a minimal core cannot support all of this unless the core includes graded truth, cost composition, reflection, and approximate equality. If G3 is relegated to a library, G0/G2 break.  
   Implementation impact: the trusted kernel boundary is undefined. This is an architectural contradiction, not just an open item.

9. **Governance contradiction: candidate G3 is load-bearing.**  
   The P13 check shows G3 guides only one decision and is marked candidate. Yet §1 says G3 is load-bearing for G0 and G2.  
   Consequences: a not-yet-approved principle is central to the language’s semantics. If G3 is rejected or changed, many L principles collapse.  
   Implementation impact: do not commit to an implementation architecture until G3 is formally settled.

10. **Open items are prerequisites, not side issues.**  
   G3’s articulation, composition of invariances, session blocks, and the kernel theory (`eta` not statable, `Fin n` not enumerable) are all open. These are not minor; they block core type checking, module instantiation, and verification.

## Bottom line

The deepest implementation blockers are:

- **What is a law?** Boolean proposition or cost-valued evidence?
- **Does a function type determine the function?** If not, L10’s quotient and L14’s validation are unsound.
- **Is typing static or demand-driven?** G1/L19 pull toward runtime demand; L2/L8/W1 pull toward static guarantees.
- **Is evidence pure or stateful?** G3 says it is kept; L18 says definitions have no effects.
- **What is a module/model?** The terminology and L20 disagree.

Until these are resolved, an implementation will either be a standard type checker that ignores G3/L19, or a demand-driven runtime that cannot support L2/L10. The draft cannot be both.