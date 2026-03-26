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

m = 3
r_triple = (1, 1, 1)
delta = 1
Q0 = make_Q_spike(m, r_triple[0], 0, 0, delta)
Q1 = make_Q_spike(m, r_triple[1], 0, 0, delta)
Q2 = make_Q_spike(m, r_triple[2], 0, 0, delta)

levels = valid_levels(m)
print(f"Number of levels: {len(levels)}")
import random; rng = random.Random(42)
for _ in range(20000):
    table = [rng.choice(levels) for _ in range(m)]
    Qs = compose_Q(table, m)
    if Qs[0] == Q0 and Qs[1] == Q1 and Qs[2] == Q2:
        sigma_found = table_to_sigma(table, m)
        if verify_sigma(sigma_found, m):
            print("m=3: SIGMA FOUND AND VERIFIED ✓")
            break
else:
    print("m=3: NOT FOUND")
