1. **Rows of 2.S12 without a law:** `translation.lth` translates `{ x := a, y := b }` to `RecordValue` via `Records`, and `e.y` to `Proj`. This directly contradicts the 2.S12 table, which states `{ x := a, y := b }` translates to `(a, b)` and `e.y` to a one-branch `match`. Furthermore, `translation.lth` lacks a translation law for `m.f` (imported module definitions) and the `Float64` case for `-x`.


2. **Rules of chapter 4 misstated:**
* Rule 4.R2 allows declared names in term position, noting that "a hole of a defined type is a parameter". However, `violatesR2Exists` in `program.lth` checks `anyUnknown p (concat (dOf p a) (bOf p a))`, incorrectly rejecting declared names in term position.


* Rule 4.R3 states a predicate over an unlabeled base must touch its parameter. The `predicateUntouched` function in `program.lth` only checks `record` and `subtype`, returning `false` for everything else (`_ -> false`), which incorrectly accepts untouched parameters on unlabeled bases.




3. **The approximations:** Reading a law only as a definition at `Bool` is unsound because it misses laws returning `Failures E` or `Cost` (or `Law T`). Reporting rather than rejecting loose functions is currently sound, as it aligns with `check -v` behavior until local definitions are fully supported per 4.S17. `ReportsExactly` can indeed be vacuous if a random generator rarely produces names that violate rules, allowing a checker that reports nothing to pass. Its domain must strictly be the accept and reject programs in `tests/spec/r*_*.lut` specified in 4.S21.


4. **Typing:** The `Typing` laws are insufficient for 4.R11. The `BranchRefines` law hardcodes the negated branch type as `App (Var "not") (App (Var q) (Var x))`. This assumes a specific AST structure for negation and only models the exact application `q x`, failing to cover arbitrary condition shapes.


5. **Names:** `namesIn` computes D(n) and B(n), but its use of `removeAll` (e.g., in `pi`, `sigma`, and `lambda`) removes all occurrences of the bound string from the inner scope's free variable list. If an inner scope rebinds the exact same name, `removeAll` could inadvertently erase valid free variables.


6. **What you would change first:** I would immediately change the domain of `ReportsExactly` from a random generator to the specific `tests/spec/` suite. Reason: A checker law that vacuously passes on random noise provides zero actual verification, making `program.lth` entirely useless until it is forced to evaluate the known boundary cases.