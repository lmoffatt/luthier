import sys; sys.argv=sys.argv[:1]
exec(open('search.py').read().split("eps3 = EPS / 3.0")[0])
x=[-2.6048498622458123, 7.066966961177535, -0.9288140062739014]; y=[-2.706528571909139, 9.865350779571646, 3.1412839090302036]
eps3=EPS/3
for eps,label in ((eps3,'eps/3'),(EPS,'eps')):
    t=[x[k]*y[k] for k in range(3)]
    print(label,'dot', abs(A.dot(x,y)-rsum(t)) > radius(eps,3,t))
    a=np.array([x]); got=A.mat_vec(a,y)
    print(label,'matvec', abs(got[0]-rsum(t)) > radius(eps,3,t))
    b=np.array([y]).T; got=A.mat_mul(a,b)
    print(label,'matmul', abs(got[0,0]-rsum(t)) > radius(eps,3,t))
    d=np.diag(t); print(label,'trace', abs(A.trace(d)-rsum(t)) > radius(eps,3,t), t)
