import sys
from math import gcd
from itertools import permutations

_ALL_P3 = list(permutations(range(3)))

def compose_Q(table, m):
    Qs = []
    for c in range(3):
        Q = {}
        for i in range(m):
            for j in range(m):
                curr_i, curr_j = i, j
                # Traverse the fiber sequence
                for s_val in range(m):
                    # We need the permutation at fiber s_val and current coordinate j
                    # But s_val is defined as (i+j+k)%m.
                    # If we fix k=0 and increment i or j, s_val changes.
                    # This compose_Q logic from core.py might be assuming s is an independent coordinate?
                    # No, core.py says sigma[(s, j)] is the fiber-uniform map.
                    p = table[s_val][curr_j]
                    gen_idx = p[c]
                    if gen_idx == 0: curr_i = (curr_i + 1) % m
                    elif gen_idx == 1: curr_j = (curr_j + 1) % m
                Q[(i, j)] = (curr_i, curr_j)
        Qs.append(Q)
    return Qs

def verify_sigma(sigma, m):
    n = m**3; k_ = 3
    arc_s = [[0]*k_ for _ in range(n)]
    for v in range(n):
        i, rem = divmod(v, m*m); j, k = divmod(rem, m)
        arc_s[v][0] = ((i+1)%m)*m*m + j*m + k
        arc_s[v][1] = i*m*m + ((j+1)%m)*m + k
        arc_s[v][2] = i*m*m + j*m + (k+1)%m
    pa = [[None]*k_ for _ in range(6)]
    for pi, p in enumerate(_ALL_P3):
        for at, c in enumerate(p): pa[pi][c] = at

    sigma_list = [0] * n
    for v in range(n):
        i, rem = divmod(v, m*m); j, k = divmod(rem, m)
        s_val = (i+j+k)%m
        p = sigma[s_val][j]
        sigma_list[v] = _ALL_P3.index(tuple(p))

    import numpy as np
    vis = np.zeros(n, dtype=bool)
    for c in range(3):
        vis[:] = False
        comps = 0
        for s in range(n):
            if not vis[s]:
                comps += 1; cur = s
                while not vis[cur]:
                    vis[cur] = True
                    cur = arc_s[cur][pa[sigma_list[cur]][c]]
        if comps != 1: return False
    return True

identity=(0,1,2); swap12=(0,2,1); swap01=(1,0,2)
def swap02(p): return (p[2], p[1], p[0])

def build_table(m):
    P = [identity]*(m-2) + [swap12, swap01]
    table = [[None]*m for _ in range(m)]
    for s in range(m):
        for j in range(m):
            if j==0 and s!=m-2: table[s][j] = swap02(P[s])
            else: table[s][j] = P[s]
    return table

if __name__ == "__main__":
    for m in range(3, 11, 2):
        tab = build_table(m)
        ok = verify_sigma(tab, m)
        print(f"m={m}: {ok}")
