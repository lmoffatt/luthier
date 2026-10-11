Ranked by how early they will critically break an implementation of sonolocalización on floats, here are the three worked examples and the structural flaws in the rules that admit them.

**1. L10 (draft 5): The unscaled substitution (Bites on Day 1)**
In sonolocalización, computing a location requires finding the intersection of hyperbolas from Time Difference of Arrival (TDOA) arrays, an operation heavily dependent on subtracting closely spaced floats.

* **The example:** Let native $f(\Delta t)$ be an exact float timestamp reader. Let extern $g(\Delta t)$ be a fast, low-precision Float16 sensor read. An identity certificate (L21) is sampled over typical field values, yielding a cost distance of $d(f, g) \le 10^{-5}$. The program computes the hyperbola asymptote $y := c / (f(\Delta t_1) - f(\Delta t_2))$. The final demand on $y$ carries a spatial tolerance of $1.0$.


* **The rule's verdict step by step:**
1. The demand pushes the tolerance of $1.0$ backward through the DAG to the inputs of $y$ (L19).


2. The planner sees $f$ is demanded and evaluates the database of runs for a cheaper path.


3. The planner finds $g$ joined by a certified equivalence of $10^{-5}$.


4. Because the path's "summed distance" ($10^{-5}$) is $\le 1.0$, L10 validates the swap. The planner substitutes $g$ for $f$.


5. The subtraction of the truncated floats creates a catastrophic cancellation. The local error of $10^{-5}$ is amplified by the condition number of $c / (t_1 - t_2)$, blowing up the output error to $100.0$. The planner returns a wrong result that silently violates the demanded tolerance.


* **The one-line fix:** "A substitution is a path whose summed distance, scaled by the condition number of the dependency cone to the demand, is within the demanded tolerance."

**2. L14 (draft 5, proposed): Acquaintance bypassing description (Bites on first field deployment)**
Early in the project, fast matrix solvers will be imported to handle audio processing before their mathematical boundaries are formally described.

* **The example:** A native Luthier function `S <- Cramer(A, b)` solves the array matrix (slow, but robust; no laws declared yet). An `extern` Python function `E <- LAPACK_sgels(A, b)` is imported for speed. $E$ inherently assumes full rank and crashes on singular matrices.


* **The rule's verdict step by step:**
1. Because $S$ has no laws yet, L14 dictates that $E$ may replace the native strictly via the identity law of L21.


2. The identity verification (L11) samples random matrices $\mathbf{A}$.


3. Random continuous matrices are almost surely full-rank. $E$ and $S$ match on all samples. The identity law passes, and the planner admits $E$.
4. The array is placed in a collinear geometry, producing a singular matrix $\mathbf{A}$. The native $S$ would have failed safely mathematically; the extern $E$ throws a `LinAlgError` and halts the host.
5. G2's mandate—that a function must be known by description (laws) rather than acquaintance (terms)—is entirely bypassed. L14 allowed empirical acquaintance to mask a fundamental domain limitation.




* **The one-line fix:** "An extern with no laws yet runs and may replace the native by the identity law only if the native's domain is exhaustively enumerable; otherwise, it requires at least one bounding law to serve as a description."

**3. L19 (draft 6): The blind memoization (Bites weeks later during data analysis)**
When re-running a script over acoustic data, the host environment (Python, C++ libraries) inevitably drifts over time.

* **The example:** The location solver uses `loc <- extern "Python" "scipy.optimize"`. In week one, the execution runs against SciPy 1.10. The result $L_1$ is generated.
* **The rule's verdict step by step:**
1. L19 caches the result $L_1$ under the exact identity specified: code, inputs, mode, demanded type and tolerance, model, seed, and plan.


2. In week two, the host OS updates to SciPy 1.12, which subtly alters the default Trust-Region step size in the solver.
3. The scientist reruns the exact same Luthier session.
4. L19 computes the hash. The code, inputs, seed, and plan (`call_extern`) are identical.


5. The memo fetches $L_1$ from the cache. The host mutation is silently ignored, rendering the algorithmic divergence undetectable to the scientist and breaking W10 (derived carries how it was derived).




* **The one-line fix:** "A result is identified by code, inputs, mode, the demanded type and tolerance, the model, the seed, the plan, and the platform hash of every extern in its cone."