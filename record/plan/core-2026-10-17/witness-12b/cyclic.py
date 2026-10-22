import sys; sys.argv=sys.argv[:1]
exec(open('search.py').read().split("eps3 = EPS / 3.0")[0])
eps3=EPS/3
best=0
shapes=((2,2),(2,3),(3,2),(1,5),(5,1),(4,4),(3,3))
for it in range(150000):
    r,c=shapes[it%len(shapes)]
    a=np.array([draw(c) for _ in range(r)]); b=np.array([draw(r) for _ in range(c)])
    lhs=A.trace(A.mat_mul(a,b)); rhs=A.trace(A.mat_mul(b,a))
    S=rsum(absSumTo([a[i,j]*b[j,i] for j in range(c)]) for i in range(r))
    ratio=abs(lhs-rhs)/(gammaN(EPS,r+c)*S) if S>0 else 0
    if ratio>best: best=ratio; print(it,(r,c),'ratio to gamma(r+c)',ratio,flush=True)
    if ratio>1.0: print('WITNESS',(r,c),a.tolist(),b.tolist()); break
print('best',best)
