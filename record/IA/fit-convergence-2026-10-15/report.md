# The fit's convergence: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on `prompt.md`; saved by the coordinator.
No factor of two, no bug in lm.py. The fit takes 39 iterations on graph_noA2 (35 at tol 1e-6)
and 59 on the full graph because of the problem: a Gauss-Newton step matrix on the profiled
likelihood, and parlante_A5 starting about 17 m (5.6 prior sds) from where its distances put
it. v0.1's own Python (`prototipo-cero/src/positions_from_distances.py`, 3D distances, same LM
schedule) on the same data: 35 iterations on graph_noA2 at tol 1e-9 (36 at 1e-12), 69 and 87 on
the full graph. "No more than 10" does not hold for v0.1 on these data.

Measured on the port's run (LUTHIER_LM_TRACE=1) and on a Python replica reproducing it to 1e-9
in phi: iterations 1 to 30 a long climb with steps of 1 to 6 m in a region where minus the
Hessian is indefinite; 31 to 39 a linear tail, |step| shrinking by 0.20 per iteration, the
decrement by 0.04. Every step accepted; mu from 0.001 divided by 3 per step to its least 1e-15
at iteration 27, then the full Gauss-Newton step: the damping is not the cause. Score against
the finite-difference gradient of logp: ratio 1.0000 at the start, 1.001 at the mode. The
prior's precision and K/RSS enter the score and the information the same way (as v0.1). The
information is the Gauss-Newton matrix, not minus the Hessian: the profiled likelihood drops
the residual curvature w Σ r_k ∇²h_k and a rank-one term (2K/RSS²)(Jᵀr)(Jᵀr)ᵀ; at the mode the
eigenvalues of minus the Hessian against the information run 0.80 to 1.00 on noA2, 0.93 to 1.71
on the full graph; the predicted tail rate (spectral radius of I − M⁺H) 0.203 on noA2 against
0.203 observed, 0.71 on the full graph, whose decrement therefore halves per iteration (0.71²):
that was the "halving", not a halved Newton step. Tried in the replica: tol 1e-6 (35 and 39
iterations); exact-Hessian Newton when positive definite (52 and 47: no help, the climb
dominates). What would cut iterations is a better start for A5 (the method's or the port's,
Luciano's). At tol 1e-6 sigma agrees with 1e-12 to 4e-7 m.

Side observation: the port fits horizontal distances (D-2026-10-06-sa) and gives sigma 2.2 cm
on noA2; v0.1's Python fits 3D distances and gives 4.9 cm (25.0 cm on the full graph).

Changes: `src/luthier/lm.py` a trace behind `LUTHIER_LM_TRACE` (reads what the method computes,
changes nothing); `tests/test_lm.py` two tests (the quadratic family converges in at most 3
steps; the trace changes nothing to the bit). The edit of lm.py makes the four lm laws' entries
stale (the host hash), re-certification of belief_laws and fit_laws needed (4 min).
