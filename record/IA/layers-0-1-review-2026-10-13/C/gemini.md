1. **Laws that are wrong or unsatisfiable together.**
In `laws.lth`, `ThenIsMaterial` uses the `Evaluated` constructor to provide evidence for the `Then` form of a law: `m.settles (Then (Case a) (Case b)) (Evaluated (material a b)) == ...`. However, `Evaluated` is the exact evidence form for a `Case` (as established by `CaseIsEvaluated`). A connective applied to sub-laws cannot be settled by a simple boolean evaluation case unless the language implicitly collapses `Then` into a `Case` before testing, which contradicts the premise that evidence follows the form of the law.


2. **Evidence**:
* **Does it say what D-2026-10-13-l says?** Mostly. It covers that a `forall` is refuted by a counterexample (`ForallRefutedByCounterexample`), an `exists` is confirmed by a witness (`ExistsConfirmedByWitness`), `then` is material (`ThenIsMaterial`), and a citation models it whole (`CitedWhole`).


* **What is missing?** The exhaustive confirmation of a `forall` (e.g., a law over `Listed` evidence yielding `Confirmed`) is missing. Additionally, the decision states an `exists` witness has a cost ("whose cost is determinate... not zero"), but the `At` evidence and `Verdict` data type carry no cost field or evaluation of it in `Settling`.




3. **Checks**:
Yes, the projections and composition models capture 5.S9 and 5.S11. `Projections` isolates the poorer forms (`failures`, `holds`, `first`, `reason`, `refine`) chosen by the demand, and `Composition` correctly states that `both` concatenates all failures unconditionally (`m.both c d x == concatFailures E (c x) (d x)`) and `either` concatenates them only if both fail (`if isEmpty E (c x) or isEmpty E (d x) then nil else concatFailures E (c x) (d x)`).


4. **The library**:
* **Do the laws state 12.S21 to 12.S23 and L6.12?** Yes. `NothingWithoutDemand` and `DemandReadsItsFile` model 12.S21. `TheoryFileNoExtern` and `ModelFileAdmits` model 12.S23. `SeesModelThroughTheory` ensures privacy by ascription by verifying the model's inner names (`"helper"`, `"Numpy"`) are not visible (L6.12, 12.S22).


* **What a loader could do wrong and still pass:** The laws only assert necessary inclusions, not exhaustive exclusions. `allIn xs ys` checks if all `xs` are in `ys` (`member x ys and allIn rest ys`), and `DemandReadsItsFile` checks `member "la_numpy.lut" (l.reads ...)`. A loader could blindly load every file on the disk or leak unimported modules into the visible namespace and still pass these laws, because the theories never assert that *only* the expected files are read or *only* the expected names are visible.




5. **Roles (L2.7)**:
Principle L2.7 states that every constructor of a `data` must have a law stating its role, otherwise it is just a collection and should be an alias. In the provided files, `Law`, `Evidence`, `Verdict`, `Reason`, and `FileKind` are declared as `data` with multiple constructors, but their roles are not defined within their own theories. Instead, the authors rely on downstream theories (`Settling`, `Projections`, `Loader`) to implicitly enforce their meaning. Under L2.7, these standalone data types are unlawful collections.


6. **What you would change first**:
I would change the `allIn` logic in `library.lth` (or add an `exactElements` check) to verify the *absence* of unintended side-effects. Reason: The entire premise of Luthier's lazy, demand-driven architecture relies on strictly bounding what is read and what is visible (L5.13, 12.S21). A test that passes a greedy loader defeats the language's core constraint.