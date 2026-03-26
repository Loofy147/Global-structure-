import sys; sys.path.insert(0,'.')
from math import gcd

def make_Q_spike(m, r, delta, j0=0):
    Q={}
    for i in range(m):
        for j in range(m):
            b = delta if j==j0 else 0
            Q[(i,j)] = ((i+b)%m, (j+r)%m)
    return Q

def is_single(Q,m):
    n=m*m; vis=set(); cur=(0,0)
    while cur not in vis: vis.add(cur); cur=Q[cur]
    return len(vis)==n

print("Canonical spike Q_c(i,j) = (i + δ·[j==0], j + r_c)\n")
print(f"{'m':>4} {'r-triple':>14} {'all_single':>12}")
print('-'*35)
for m in [3,5,7,9,11,13,15]:
    r_triple=(1,m-2,1); delta=1
    Q0=make_Q_spike(m,r_triple[0],delta)
    Q1=make_Q_spike(m,r_triple[1],delta)
    Q2=make_Q_spike(m,r_triple[2],delta)
    ok=all(is_single(Q,m) for Q in [Q0,Q1,Q2])
    print(f"{m:>4} {str(r_triple):>14} {str(ok):>12}")
