import sys; sys.argv = sys.argv[:1]
exec(open('search.py').read().split("eps3 = EPS / 3.0")[0])
eps3 = EPS / 3.0
import itertools
N = 40000
found = {}
shapes = {
 'TraceAgrees': [lambda n=n: trace_case(n, eps3) for n in (3, 4, 5, 8)],
 'MatMulAgrees': [lambda s=s: matmul_case(*s, eps3) for s in ((2,3,2), (1,4,1), (3,3,3), (2,8,2))],
 'MatMulTransposes': [lambda s=s: transposes_case(*s, eps3) for s in ((2,3,2), (3,3,3), (2,8,2), (4,5,3))],
 'TraceCyclic': [lambda s=s: cyclic_case(*s, eps3) for s in ((1,3), (2,2), (2,3), (3,3))],
}
for it in range(N):
    for name, fs in shapes.items():
        if name in found: continue
        f = fs[it % len(fs)]
        ok, w, _ = f()
        if ok:
            found[name] = (it, w); print(name, it, repr(w), flush=True)
    if len(found) == len(shapes): break
print('done', sorted(found))
