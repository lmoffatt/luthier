import sys; sys.argv=sys.argv[:1]
exec(open('search.py').read().split("eps3 = EPS / 3.0")[0])
x=[-2.6048498622458123, 7.066966961177535, -0.9288140062739014]; y=[-2.706528571909139, 9.865350779571646, 3.1412839090302036]
t=[x[k]*y[k] for k in range(3)]
eps3=EPS/3
print('dot', A.dot(x,y), rsum(t), (t[0]+t[1])+t[2])
a=np.diag(t); print('trace', A.trace(a), rsum(t), abs(A.trace(a)-rsum(t)) > radius(eps3,3,t))
for perm in ([0,1,2],[2,1,0],[1,0,2],[0,2,1],[1,2,0],[2,0,1]):
    tt=[t[p] for p in perm]; a=np.diag(tt)
    if abs(A.trace(a)-rsum(tt)) > radius(eps3,3,tt): print('trace witness', perm, tt)
A1=np.array([x]); B1=np.array([y]).T
lhs=A.trace(A.mat_mul(A1,B1)); rhs=A.trace(A.mat_mul(B1,A1))
S=rsum(absSumTo([A1[i,j]*B1[j,i] for j in range(3)]) for i in range(1))
print('cyclic', lhs, rhs, abs(lhs-rhs), 3*gammaN(eps3,4)*S)
# transposes: does it ever differ?
diff=0
for it in range(3000):
    a=np.array([draw(5) for _ in range(3)]); b=np.array([draw(4) for _ in range(5)])
    if not np.array_equal(A.transpose(A.mat_mul(a,b)), A.mat_mul(A.transpose(b),A.transpose(a))): diff+=1
print('transposes differ in', diff, 'of 3000')
