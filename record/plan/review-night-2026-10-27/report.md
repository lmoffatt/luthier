**Read-only review of the night of 2026-10-26 to 27**

Reviewed branch `numbers`, from `b21f2da` through `e0f3a9629443653b5d8d9aa006e84762119a9b10`. I also reviewed `65f0672` and `ba5dcf4`, which are ancestors of the requested baseline.

I read `CLAUDE.md`, the five night reports, the fixes report, the relevant decisions and principles, and the implementation, theory, specification and test diffs. `report-queue-kl.md` was absent.

**Assessment:** the changes contain useful fixes, but the convergence contract still admits a maximizer that makes no progress, and the kernel changes can alter results without invalidating their identities. Those are the highest priority findings.

No files were changed. The checkout contained uncommitted changes, and another store became modified during the review. I left those changes untouched and used committed `HEAD` contents when validating the changed stores.

**Findings, ordered by severity**

**1. High: a maximizer can avoid convergence indefinitely by making its bound depend on the caller’s budget**

Location: [belief.lth:195](/home/lmoffatt/Projects/luthier/src/luthier/lib/belief.lth:195), especially the exhausted branch at line 201.

`quadraticSteps` receives all of `Settings`, including `maxIter`. A model can define its bound as `s.maxIter + 1`, return the starting point, and report exhaustion after `s.maxIter` steps. Every budget then remains below its declared bound.

A concrete model is:

```luthier
{
  maximize := fn s n f g m x {
    { x := x,
      reason := (if decrement n s g m x < s.tol
                 then converged unit else exhausted unit),
      steps := s.maxIter }
  },
  quadraticSteps := fn s dec { s.maxIter + 1 }
}
```

For dimension 1, maximum at `b = [1]`, curvature 1, start `[0]`, tolerance `1e-12`, and budget 100, direct evaluation returned:

```text
QuadraticConverges   true
MaximizerStationary  true
MaximizerAscends     true
```

The dimension is also preserved. The result remains half a unit of objective decrement from the maximum. Burning 100 ineffective iterations would make the reported count truthful without fixing the problem.

This defeats D-2026-10-16-m (an iterative algorithm must converge within a bound derived from its theory). `LMStepsOnQuadratic` tests a separate `LMStep` parameter and does not establish that an arbitrary `Maximizer` declares that method’s bound.

Smallest fix: make the bound independent of `maxIter`, either by its argument type or by an explicit budget-independence law. Add this model as a control and connect each maximizer’s declared bound to its method’s convergence evidence.

**2. High: changed kernel behavior retains the same cone identity**

Locations: [kernel.py:824](/home/lmoffatt/Projects/luthier/src/luthier/kernel.py:824), [certify.py:199](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:199), [tester.py:2999](/home/lmoffatt/Projects/luthier/src/luthier/tester.py:2999).

The new matching rule changes the result of an unchanged kernel program:

```luthier
match stop { stop u -> 1 ; _ -> 2 }
```

With `stop` a bare Unit label, the kernel at `b21f2da` returns 2; the current kernel returns 1. I loaded the old kernel source into memory and verified both results on the same terms.

Both revisions identify the interpreter as `v0.3`. The program’s cone contains no changed host route, and the kernel source is absent from `drawing_revision`. Its cone identity therefore does not distinguish those executions. Existing certificate lookups and result memo keys can reuse evidence or values produced under the old behavior.

This exposes a concrete conflict between L10.4 (a certificate identifies its dependency cone and frozen derivation) and D-2026-10-15-i (the interim interpreter revision is the last reachable tag). The agents followed the existing tag rule; the new semantic change shows its cost.

Smallest immediate fix: give these semantics a distinct interpreter revision before reusing certificates or memoized results. A targeted semantic fingerprint is an alternative if the tag policy remains.

The report’s statement that re-certification will reveal changed outcomes needs qualification: ordinary certification can reuse an unchanged identity without evaluating it.

**3. High: interrupted runs discard output that has already reached the world**

Locations: [run.py:3354](/home/lmoffatt/Projects/luthier/src/luthier/run.py:3354), [run.py:3628](/home/lmoffatt/Projects/luthier/src/luthier/run.py:3628).

`RefusedAfterActing` preserves output, but `ActionFailed` and ordinary resource cuts do not. `record` deletes `output` whenever the exception lacks an `output` attribute.

Concrete scenario: the first print succeeds, and the second print fails or the run exhausts its fuel. The accepted first line has already reached stdout. The run record retains an accepted-byte count, but loses the text.

An in-memory probe replaced `write_checked` with a collector and called `record` with an `ActionFailed`. The serialized record contained the failure and step count, but omitted the supplied text `"accepted before failure\n"`.

This conflicts with P3 (keep the original evidence and its corrections) and the coordinator’s answer that output which reached the world is evidence. Immediate printing makes the older “no output on a cut” convention materially different.

Smallest fix: capture accepted output for every interrupted run, including failed actions and resource cuts. Keep it explicitly marked as partial output; do not admit the run to the result store.

**4. Medium: integer-only arithmetic now attempts an unnecessary Float64 conversion**

Location: [elaborate.py:1847](/home/lmoffatt/Projects/luthier/src/luthier/elaborate.py:1847).

`numeric_literals` converts a literal left operand before determining whether the right operand is Float64.

For the integer expression consisting of the decimal representation of `10**400`, followed by `+ 1`:

```text
b21f2da: elaboration succeeds
HEAD:    OverflowError: int too large to convert to float
```

There is no Float64 operand. This contradicts the implementation’s stated behavior that two Int operands remain Int, and exceeds D-2026-10-26-a (an integer literal takes the other operand’s numeric type).

A minimal reproducer is:

```python
from luthier.parse import parse
from luthier.elaborate import elaborate_program

source = "x : Int := " + "1" + "0" * 400 + " + 1"
elaborate_program(parse(source).program)
```

Smallest fix: infer the right operand’s type before calling `_float_literal(a)`. When conversion is required but impossible, raise a normal typing diagnostic instead of leaking `OverflowError`.

**5. Medium: stdout’s accepted-byte evidence can overstate or corrupt what was written**

Locations: [host.py:231](/home/lmoffatt/Projects/luthier/src/luthier/host.py:231), [host.py:258](/home/lmoffatt/Projects/luthier/src/luthier/host.py:258).

There are two verified cases.

- For a stream without a descriptor, `_write` ignores `stream.write`’s return value. A stream accepting one character from `"abc\n"` received `"a"`, while `stdout()` reported `"abc\n"` and `place()` reported four accepted bytes.
- If a descriptor accepts only the first byte of UTF-8 `"é\n"` and then fails, the accepted byte `c3` becomes the replacement character `�`. Re-encoding that character makes `place()` report three accepted bytes although the system accepted one.

Both undermine D-2026-10-16-n (print checks what writes accept and records that evidence). The report’s claim that every write result is checked is too broad for the descriptor-free branch.

Smallest fix: handle short text-stream writes using their character counts, and retain descriptor output as bytes. Record the actual byte count independently of a display decoding, with a lossless representation for incomplete UTF-8.

**6. Medium: the new joint-distribution rectangle law refutes the supplied product model because of rounding**

Location: [equality.lth:129](/home/lmoffatt/Projects/luthier/src/luthier/lib/core/structures/equality.lth:129).

`JointRectangle` requires the result of four floating-point operations to be exactly nonnegative.

Using the saved C3 scratch program’s `productJoint`, this ordered rectangle is refuted:

```luthier
{ s1 := 0.1, s2 := 0.5, u1 := 1.0, u2 := 1.0 }
```

The rectangle has zero height, so its exact probability mass is zero. The computed expression is approximately:

```text
-6.938893903907228e-18
```

Direct evaluation of `JointRectangle productJoint` returned `false`.

The law therefore rejects the natural independent exponential model for numerical cancellation, rather than a probability defect. This matters under L9.14 (a control must expose the property the law claims to check) and L13.3 (rounding contributes an additive defect).

Smallest fix for this case: return true for degenerate rectangles. The general fix also needs an explicit numerical defect bound, or an exact carrier, for nondegenerate rectangles. Do not hide the issue behind an unrecorded epsilon.

**7. Medium: `DistanceSum` permits an overconfident distribution unrelated to the actual sum**

Location: [equality.lth:142](/home/lmoffatt/Projects/luthier/src/luthier/lib/core/structures/equality.lth:142).

Rectangle domination is necessary for a sum distribution, but it does not establish that the declared distribution is the sum.

Consider two distances both deterministically equal to 1. Their joint is valid. An alleged sum deterministically equal to zero satisfies the rectangle inequality: whenever the joint rectangle has probability 1, `s > 1` and `u > 1`, so the alleged zero-sum CDF at `s + u` is also 1.

I verified that `SumDominatesRectangle` accepts this construction at `s = u = 1.5`. Yet at threshold 1, the alleged sum assigns probability 1 below the threshold, while the actual sum, 2, assigns probability 0.

The C3 report acknowledges that it declares only rectangle domination. That limitation is accurately reported, but the resulting interface must not be consumed as certification of a sum distribution. There is no production consumer yet, so this is a theory gap rather than an observed runtime failure.

Smallest containment: name and document the interface as a rectangle-domination condition. Before using it to transport uncertainty, add a contract tying the distribution to the joint’s sum pushforward. Marginal upper bounds would exclude this example but would not establish the full sum contract.

**8. Medium: the derived LM step count can fail to terminate for a valid damping schedule**

Location: [optimization.lth:198](/home/lmoffatt/Projects/luthier/src/luthier/lib/optimization.lth:198).

This schedule satisfies the declared `Damping` refinement:

```luthier
{ init := 1.0e16, factor := 3.0,
  least := 1.0e16, most := 1.0e17 }
```

At that magnitude, Float64 evaluates `1.0 + mu` as `mu`, so:

```text
mu / (1.0 + mu) = 1
```

`lowered` also remains at `least`. Thus a decrement of 1 never approaches tolerance `1e-12` in `lmQuadraticSteps`.

The direct probe exhausted 10,000 fuel without returning a count. The actual driver still has a finite iteration budget, but computing its supposedly finite bound can prevent the law from reaching the run.

Smallest fix: constrain the schedule’s convergence domain to ensure a representable contraction, or make the bound calculation return an explicit inability to establish a finite count. Include the schedule in the controls.

The reported stress test supports the damping schedules it exercised, not every inhabitant of `Damping`.

**9. Medium: bisection’s declared domain includes finite brackets whose width overflows**

Locations: [bisection.lut:31](/home/lmoffatt/Projects/luthier/examples/bisection.lut:31), [bisection.lut:39](/home/lmoffatt/Projects/luthier/examples/bisection.lut:39), [bisection.lut:68](/home/lmoffatt/Projects/luthier/examples/bisection.lut:68).

Concrete problem:

```luthier
{ f := fn x { x },
  lo := -1.0e308, hi := 1.0e308,
  root := 0.0, blur := 0.0 }
```

It has finite endpoints, opposite signs and an exact root. `featuresOf` reports `brackets = true`. A bound of `1e300` is above the declared rounding floor.

Nevertheless, `hi - lo` overflows. The kernel leaves that arithmetic unreduced, and direct evaluation of `bisect` fails with `RunError: stuck match`. The modulus also depends on that width.

Smallest containment: exclude brackets with unrepresentable width or required intermediates from the domain. Supporting them requires overflow-safe midpoint, width and modulus calculations together.

The listed moderate brackets support the report’s measured results. They do not establish sufficiency throughout the declared domain.

**10. Medium: the scaling law accepts lists that do not describe paired observations**

Location: [resources.lth:162](/home/lmoffatt/Projects/luthier/src/luthier/lib/resources.lth:162).

`spent` and `rates` are independent lists. The premise does not require equal lengths. `crossDeviations` silently stops when either list ends, while means and squared deviations use their respective full lists.

This malformed experiment was accepted by the numerical-law evaluator:

```luthier
ScalesAs elementary doubles 0.0 1.0 [100.0] [1.0, 2.0]
```

There is only one measured cost for two rates. The single `y` has zero deviation from its own mean, producing slope zero and a passing comparison, despite the missing observation.

Smallest fix: require aligned lists with at least two observations, positive rates and counts, and a valid grain. A list of `(rate, spent)` pairs would prevent unequal lengths structurally.

This does not refute the reported bisection scaling experiment, whose lists are aligned. It is a defect in the exported general law.

**11. Low: C3’s saved Gamma distribution has an invalid continuity witness**

Location: [c3-scratch-joint.test.lut.txt:21](/home/lmoffatt/Projects/luthier/record/plan/after-core-2026-10-23/c3-scratch-joint.test.lut.txt:21).

For `gamma2`, choose `t = 2` and `p = 0.5`:

```text
gammaCdf(2)       = 0.5939941502901619
gamma2.below 2 .5 = 2.227947177299516
```

The premise `p < cdf t` holds, but `below t p < t` fails. Direct evaluation of `DistributionLeftContinuous gamma2 2.0 0.5` returned `false`.

The formula averages an upper quantile bound with `t`; that upper bound can already exceed `t`.

Smallest fix: construct the witness by searching below `t` until the CDF remains above `p`, with a suitable numerical domain. Add the distribution’s own laws to the scratch tests. The existing rectangle test does not validate `gamma2` as a `DistanceDistribution`.

**12. Low: the later cutoff change leaves an existing demand-record test stale**

Locations: [tests/test_run.py:1457](/home/lmoffatt/Projects/luthier/tests/test_run.py:1457), [run.py:2131](/home/lmoffatt/Projects/luthier/src/luthier/run.py:2131).

`Demand.record` now always includes `"cutoffs": []` by default. The test compares the complete record against a dictionary without that field.

I evaluated the expected dictionary from the test’s AST and compared it with an in-memory `Demand.record`. They differ by exactly the additional `cutoffs` key.

Smallest fix: update the default-record expectation and add a nonempty-cutoff assertion.

The fixes report’s passing-suite claim is explicitly for `f0e259b`, before this change. It should not be read as a passing-suite claim for current `HEAD`.

**Parts that looked right**

- **Tester fixes `65f0672` and `ba5dcf4`:** I found no defect in the reviewed handling of reused conjunct evidence or the conservative rejection of visibly mistyped censuses. The latter explicitly leaves unresolved dependent cases unchecked; it does not claim complete dependent type validation.
- **Prune grouping:** preserving separate fingerprint sets addresses the reported cross-program eviction. An in-memory probe retained both sets and retained negative evidence beyond the ordinary limit. The report correctly discloses that the number of fingerprint sets is unbounded.
- **Typing and substitution:** the comparison checks and simultaneous substitution fix passed the selected existing tests, including the swapped `A`/`B` case.
- **Unit labels and the eval probe:** the intended bare/applied equivalence and matching behavior passed their existing tests. The identity problem in finding 2 is separate from the correctness of that behavior.
- **Resource algebra:** the model matches the stated work, span and memory compositions. I found no mismatch in those definitions.
- **First-action caching:** moving arguments from the binding to evidence follows D-2026-10-16-k item 9 (validate once per model-cone hash while retaining the arguments as evidence). Reuse across arguments is an explicit decision.
- **Binding precedence and boxed coverage:** the reviewed definitions agree with the recorded specificity rule and with confirmation on a fully checked box. The host’s box adapter operates on Boolean point results; it does not promote statistical `Tested` evidence through that path.
- **Consumer result records:** `lm.py` returns reasons and step counts consistently with the revised result type. The experiment summary now distinguishes exhaustion from stalling.

**Verification and limits**

All Python probes used `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=src`. Probes used direct parsing, elaboration, pure evaluation, in-memory historical modules, or mocked record output. I did not execute `luthier certify`, `luthier test` or `luthier run`.

Seven existing kernel, elaboration and checker tests were called directly without filesystem fixtures. All passed under Python 3.12.9 and NumPy 1.26.4. The main exploratory probes used Python 3.14.8 and NumPy 2.4.6; environment-sensitive store freshness was not treated as a new defect.

All 23 changed committed certificate stores passed `certify.store_errors`. That establishes schema consistency, not correctness or freshness of their evidence.

The numerical probes are deterministic counterexamples. I did not repeat the reported large stress tests or full suite.

**Decisions taken during this review:** no implementation or repository-policy decisions. The fixes above are proposals for the coordinator and Luciano; none was applied.


