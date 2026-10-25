"""c1-ulps.py: the worst error, in units in the last place, of Python's math.exp, log, erf and sqrt
against mpmath at 200 bits, on drawn points (seed 1): exp on [-300, 300], log and sqrt on 10^u with u
uniform on [-150, 150] plus 5000 points near one, erf on [-6, 6]. Wave C bite C1, 2026-10-25, Claude
Opus 5.5 (record/plan/audit-algebras-2026-10-22/prompt-wave-bc.md), for the accuracy numbers_model.lut
declares for `elementary`. Run with: python -I c1-ulps.py. Inputs: Python 3 math over Debian GLIBC
2.43-7, mpmath 1.3.0. Output on 2026-10-25: exp 0.5020355409020946, log 0.4999868251644428,
erf 0.4999724634901481, sqrt 0.4999923854048978."""
import math, random, mpmath
mpmath.mp.prec = 200
rng = random.Random(1)
def ulp_err(f, F, xs):
    worst = 0.0
    for x in xs:
        y = f(x); Y = F(mpmath.mpf(x))
        if Y == 0: continue
        e = abs(mpmath.mpf(y) - Y) / mpmath.mpf(math.ulp(float(Y)))
        worst = max(worst, float(e))
    return worst
xs = [rng.uniform(-300, 300) for _ in range(20000)]
print("exp", ulp_err(math.exp, mpmath.exp, xs))
ps = [10 ** rng.uniform(-150, 150) for _ in range(20000)] + [1 + rng.uniform(-1e-3, 1e-3) for _ in range(5000)]
print("log", ulp_err(math.log, mpmath.log, ps))
es = [rng.uniform(-6, 6) for _ in range(20000)]
print("erf", ulp_err(math.erf, mpmath.erf, es))
print("sqrt", ulp_err(math.sqrt, mpmath.sqrt, ps))
