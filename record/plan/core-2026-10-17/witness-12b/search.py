# Search for witnesses refuting arrays.lth's six summing laws with gamma n in place of 3 gamma n
# (a Doubles model whose epsilon is a third of the machine's). Seed 20261022. Mirrors the laws'
# float arithmetic: native sums are right folds f0 + (f1 + (... + (f_{n-1} + 0.0))).
import numpy as np, sys
sys.path.insert(0, '/home/lmoffatt/Projects/luthier/src')
from luthier import arrays as A
EPS = 2.220446049250313e-16
def gammaN(eps, n): return (float(n) * eps / 2.0) / (1.0 - float(n) * eps / 2.0)
def rsum(xs):
    acc = 0.0
    for v in reversed(list(xs)): acc = v + acc
    return acc
def absSumTo(xs): return rsum(abs(v) for v in xs)
def radius(eps, n, terms): return 3.0 * gammaN(eps, n) * absSumTo(terms)
rng = np.random.default_rng(20261022)
def draw(n):
    # integers scaled: products with partial sums near powers of two give the largest roundings
    return [float(v) for v in rng.uniform(-10, 10, n)]
def dot_case(n, eps):
    x = draw(n); y = draw(n)
    terms = [x[k]*y[k] for k in range(n)]
    d = abs(A.dot(x, y) - rsum(terms))
    return d > radius(eps, n, terms), (x, y), d / max(radius(EPS, n, terms)/3, 1e-300)
def trace_case(n, eps):
    a = np.array([draw(n) for _ in range(n)])
    terms = [a[i, i] for i in range(n)]
    d = abs(A.trace(a) - rsum(terms))
    return d > radius(eps, n, terms), a.tolist(), d / max(radius(EPS, n, terms)/3, 1e-300)
def matvec_case(r, c, eps):
    a = np.array([draw(c) for _ in range(r)]); x = draw(c)
    got = A.mat_vec(a, x)
    for i in range(r):
        terms = [a[i, j]*x[j] for j in range(c)]
        if abs(got[i] - rsum(terms)) > radius(eps, c, terms): return True, (a.tolist(), x), 0
    return False, None, 0
def matmul_case(r, k, c, eps):
    a = np.array([draw(k) for _ in range(r)]); b = np.array([draw(c) for _ in range(k)])
    got = A.mat_mul(a, b)
    for i in range(r):
        for j in range(c):
            terms = [a[i, l]*b[l, j] for l in range(k)]
            if abs(got[i, j] - rsum(terms)) > radius(eps, k, terms): return True, (a.tolist(), b.tolist()), 0
    return False, None, 0
def transposes_case(r, k, c, eps):
    a = np.array([draw(k) for _ in range(r)]); b = np.array([draw(c) for _ in range(k)])
    lhs = A.transpose(A.mat_mul(a, b)); rhs = A.mat_mul(A.transpose(b), A.transpose(a))
    for e in range(r*c):
        i, j = e % r, e // r   # entry e of the transposed (c x r) read row-major... law's own index
    # law: matBall over Fin (m*n) with the (c x r) result; entry e = (e / r, e mod r); terms a (e mod r) l * b l (e / r)
    m = lhs.shape[0]; nn = lhs.shape[1]
    for e in range(m*nn):
        p, q = e // nn, e % nn
        terms = [a[e % r, l]*b[l, e // r] for l in range(k)]
        if abs(lhs[p, q] - rhs[p, q]) > radius(eps, k, terms): return True, (a.tolist(), b.tolist()), 0
    return False, None, 0
def cyclic_case(r, c, eps):
    a = np.array([draw(c) for _ in range(r)]); b = np.array([draw(r) for _ in range(c)])
    lhs = A.trace(A.mat_mul(a, b)); rhs = A.trace(A.mat_mul(b, a))
    S = rsum(absSumTo([a[i, j]*b[j, i] for j in range(c)]) for i in range(r))
    rad = 3.0 * gammaN(eps, r + c) * S
    return abs(lhs - rhs) > rad, (a.tolist(), b.tolist()), 0
eps3 = EPS / 3.0
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
found = {}
for it in range(N):
    for name, f in (('DotAgrees', lambda: dot_case(3, eps3)), ('TraceAgrees', lambda: trace_case(3, eps3)),
                    ('MatVecAgrees', lambda: matvec_case(1, 3, eps3)), ('MatMulAgrees', lambda: matmul_case(1, 3, 1, eps3)),
                    ('MatMulTransposes', lambda: transposes_case(1, 3, 1, eps3)), ('TraceCyclic', lambda: cyclic_case(1, 2, eps3))):
        if name in found: continue
        ok, w, _ = f()
        if ok:
            found[name] = (it, w); print(name, it, repr(w), flush=True)
    if len(found) == 6: break
print('done', N, sorted(found))
