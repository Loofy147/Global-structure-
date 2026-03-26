import math, random, time
from math import gcd, log2
from itertools import permutations, product as iprod
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass

def time_now(): return time.perf_counter()

@dataclass(frozen=True)
class Weights:
    m: int; k: int; h2_blocks: bool; r_count: int; canonical: tuple
    h1_exact: int; search_exp: float; compression: float; sol_lb: int; orbit_size: int
    coprime_elems: tuple
    def summary(self) -> str:
        s = "✓ OK" if not self.h2_blocks else "✗ BLOCKED"
        return f"({self.m},{self.k}) {s} W2={self.r_count} W4={self.h1_exact} W7={self.sol_lb:,}"

def extract_weights(m: int, k: int) -> Weights:
    cp = tuple(r for r in range(1, m) if gcd(r, m) == 1); phi_m = len(cp)
    h2_uni = (phi_m > 0 and all(r % 2 == 1 for r in cp)) and (k % 2 == 1) and (m % 2 == 0)
    r_tuples = [] if h2_uni else [t for t in iprod(cp, repeat=k) if sum(t) == m]
    r_count = len(r_tuples)
    mid = m - (k - 1)
    canon = ((1,)*(k-1) + (mid,)) if (mid > 0 and gcd(mid,m)==1) else (r_tuples[0] if r_count>0 else None)
    search_exp = m * log2(phi_m * 6) if phi_m > 0 else 0
    full_exp = (m**k) * log2(math.factorial(k))
    compression = search_exp / full_exp if full_exp > 0 else 1.0
    cb = (m**(m-1)) * phi_m
    sol_lb = phi_m * (cb**(k-1)) if (not h2_uni and r_count > 0) else 0
    return Weights(m=m, k=k, h2_blocks=h2_uni, r_count=r_count, canonical=canon,
                   h1_exact=phi_m, search_exp=round(search_exp,3),
                   compression=round(compression,6), sol_lb=sol_lb, orbit_size=m**(m-1),
                   coprime_elems=cp)

def verify_sigma(sigma, m):
    if not sigma: return False
    n = m**3; k_ = 3
    arc_s = [[0]*k_ for _ in range(n)]
    for v in range(n):
        i, rem = divmod(v, m*m); j, k = divmod(rem, m)
        arc_s[v][0] = ((i+1)%m)*m*m + j*m + k
        arc_s[v][1] = i*m*m + ((j+1)%m)*m + k
        arc_s[v][2] = i*m*m + j*m + (k+1)%m
    pa = [[None]*k_ for _ in range(6)]; ALL_P = list(permutations(range(3)))
    for pi, p in enumerate(ALL_P):
        for at, c in enumerate(p): pa[pi][c] = at
    if isinstance(sigma, dict):
        sigma_list = [0] * n
        for v in range(n):
            i, rem = divmod(v, m*m); j, k = divmod(rem, m)
            p = sigma.get((i, j, k))
            if p is None: p = sigma.get(( (i+j+k)%m, j ))
            if p is None: return False
            sigma_list[v] = ALL_P.index(p) if not isinstance(p, int) else p
        sigma = sigma_list
    vis = bytearray(n)
    for c in range(3):
        comps = 0; vis[:] = b'\x00' * n
        for s in range(n):
            if not vis[s]:
                comps += 1; cur = s
                while not vis[cur]: vis[cur] = 1; cur = arc_s[cur][pa[sigma[cur]][c]]
        if comps != 1: return False
    return True

def _build_sa3(m):
    n = m**3; k_ = 3; arc_s = [[0]*k_ for _ in range(n)]
    for v in range(n):
        i, rem = divmod(v, m*m); j, k = divmod(rem, m)
        arc_s[v][0] = ((i+1)%m)*m*m + j*m + k
        arc_s[v][1] = i*m*m + ((j+1)%m)*m + k
        arc_s[v][2] = i*m*m + j*m + (k+1)%m
    pa = [[None]*k_ for _ in range(6)]; ALL_P = list(permutations(range(3)))
    for pi, p in enumerate(ALL_P):
        for at, c in enumerate(p): pa[pi][c] = at
    return n, arc_s, pa

def _sa_score(sigma, arc_s, pa, n):
    vis = bytearray(n); total = 0
    for c in range(3):
        comps = 0; vis[:] = b'\x00' * n
        for s in range(n):
            if not vis[s]:
                comps += 1; cur = s
                while not vis[cur]: vis[cur] = 1; cur = arc_s[cur][pa[sigma[cur]][c]]
        total += (comps - 1)
    return total

def construct_spike_sigma(m, seed=42):
    if m % 2 == 0: return None
    n, arc_s, pa = _build_sa3(m); nP = 6; ALL_P = list(permutations(range(3))); rng = random.Random(seed)
    state = [[rng.randrange(nP) for _ in range(m)] for _ in range(m)]
    def get_sigma(st):
        sig = [0]*n
        for v in range(n):
            i, rem = divmod(v, m*m); j, k = divmod(rem, m)
            sig[v] = st[(i+j+k)%m][j]
        return sig
    cur_sig = get_sigma(state); cur_score = _sa_score(cur_sig, arc_s, pa, n); T = 1.0
    for it in range(100000 if m < 10 else 200000):
        if cur_score == 0: break
        si, ji = rng.randrange(m), rng.randrange(m); old = state[si][ji]; state[si][ji] = rng.randrange(nP)
        nsig = get_sigma(state); nscore = _sa_score(nsig, arc_s, pa, n)
        if nscore <= cur_score or rng.random() < math.exp((cur_score-nscore)/T): cur_score = nscore
        else: state[si][ji] = old
        if it % 1000 == 0: T *= 0.98
    if cur_score == 0:
        res = {}
        for s in range(m):
            for j in range(m): res[(s, j)] = ALL_P[state[s][j]]
        return res
    return None

def solve_spike(m, max_iter=200000): return construct_spike_sigma(m)

PRECOMPUTED = { (m,3): construct_spike_sigma(m) for m in [3, 5] }
SOLUTION_M4 = [1, 1, 5, 5, 1, 0, 0, 5, 2, 3, 3, 4, 3, 4, 4, 1, 1, 5, 1, 0, 2, 4, 3, 4, 2, 5, 4, 0, 5, 1, 0, 2, 1, 2, 2, 4, 1, 0, 4, 5, 5, 1, 0, 3, 1, 2, 5, 5, 3, 5, 4, 2, 2, 1, 1, 1, 1, 1, 5, 4, 5, 3, 1, 4]

def valid_levels(m):
    levels = []; ALL_P = list(permutations(range(3)))
    for c1 in range(3):
        others = [c for c in range(3) if c != c1]
        for y in iprod([0, 1], repeat=m):
            perms = []
            for j in range(m):
                c0 = others[0] if y[j] == 1 else others[1]
                c2 = [c for c in range(3) if c not in [c0, c1]][0]
                p = [0,0,0]; p[c0] = 0; p[c1] = 1; p[c2] = 2
                perms.append(tuple(p))
            levels.append(tuple(perms))
    return levels

def compose_Q(table, m):
    Qs = []
    for c in range(3):
        Q = {}
        for i in range(m):
            for j in range(m):
                curr_i, curr_j = i, j
                for s in range(m):
                    p = table[s][curr_j]; arc = p[c]
                    if arc == 0: curr_i = (curr_i + 1) % m
                    elif arc == 1: curr_j = (curr_j + 1) % m
                Q[(i, j)] = (curr_i, curr_j)
        Qs.append(Q)
    return Qs

def is_single_cycle(Q, m):
    if not Q: return False
    n = m*m; visited = set(); curr = (0, 0); count = 0
    while curr not in visited:
        visited.add(curr); count += 1; curr = Q[curr]
    return count == n

_ALL_P3 = list(permutations(range(3)))
_FIBER_SHIFTS = [(1,0,0), (0,1,0), (0,0,1)]

def table_to_sigma(table, m):
    sigma = {}
    for s in range(m):
        for j in range(m):
            sigma[(s, j)] = table[s][j]
    return sigma

def solve(m, k=3, seed=42):
    if m % 2 != 0 and k == 3: return construct_spike_sigma(m)
    sol, _ = run_sa(m, seed=seed)
    return sol

def run_sa(m, seed=0, max_iter=1000000):
    random.seed(seed); n, arc_s, pa = _build_sa3(m); nP = 6
    sigma = [random.randrange(nP) for _ in range(n)]; cs = _sa_score(sigma, arc_s, pa, n); bs = cs; best = sigma[:]
    T = 1.0; t0 = time_now()
    for it in range(max_iter):
        if cs == 0: break
        v = random.randrange(n); old = sigma[v]; new = random.randrange(nP); sigma[v] = new
        ns = _sa_score(sigma, arc_s, pa, n); d = ns - cs
        if d < 0 or random.random() < math.exp(-d/max(T, 1e-9)):
            cs = ns
            if cs < bs: bs = cs; best = sigma[:]
        else: sigma[v] = old
        if it % 10000 == 0: T *= 0.99
    return best if bs == 0 else None, {'best': bs, 'iters': it+1, 'elapsed': time_now()-t0}
