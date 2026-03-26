import sys; sys.path.insert(0,'.')
from math import gcd
from itertools import product as iprod, permutations as perms
from core import verify_sigma, valid_levels, compose_Q, table_to_sigma, is_single_cycle

def make_Q_spike(m, r, v, j0, delta):
    Q={}
    for i in range(m):
        for j in range(m):
            b = (v + delta) if j==j0 else v
            Q[(i,j)] = ((i+b)%m, (j+r)%m)
    return Q

print("=== CANONICAL SPIKE CONSTRUCTION ===")
print("b_c(j) = δ if j==0, else 0  (v=0, j₀=0)")
print("Sum_b = δ, gcd(δ,m)=1 ✓")
print("Q_c(i,j) = (i + δ·[j==0], j + r_c)\n")

for m in [3,5,7,9,11,13]:
    cp=[r for r in range(1,m) if gcd(r,m)==1]
    # Use canonical r-triple (1,m-2,1)
    r_triple=(1,m-2,1)
    # Use delta=1 for all colours (smallest coprime to m)
    delta=1

    Q0=make_Q_spike(m,r_triple[0],0,0,delta)
    Q1=make_Q_spike(m,r_triple[1],0,0,delta)
    Q2=make_Q_spike(m,r_triple[2],0,0,delta)

    cycles=[is_single_cycle(Q0,m),is_single_cycle(Q1,m),is_single_cycle(Q2,m)]

    print(f"m={m} r={r_triple} δ=1: single_cycles={cycles}", end="")

    if all(cycles):
        # Try to find sigma
        levels=valid_levels(m)
        sigma_found=None
        import random; rng=random.Random(42)
        # Search for a table of levels that produces exactly these Qs
        for _ in range(200_000):
            table=[rng.choice(levels) for _ in range(m)]
            Qs=compose_Q(table,m)
            if Qs[0]==Q0 and Qs[1]==Q1 and Qs[2]==Q2:
                sigma_found=table_to_sigma(table,m)
                break
        if sigma_found and verify_sigma(sigma_found,m):
            print(f" → SIGMA FOUND AND VERIFIED ✓")
        else:
            print(f" → cycles ok but no compatible level table found")
    else:
        print(f" → not all single cycles")
