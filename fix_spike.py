import math, random, time
from math import gcd
from itertools import permutations, product as iprod
from core import _build_sa3, _sa_score, _ALL_P3

def construct_spike_robust(m, seed=42):
    if m % 2 == 0: return None
    n, arc_s, pa = _build_sa3(m); nP = 6; rng = random.Random(seed)
    # The 'spike' rule: B = 1 for color 0 at j = m-1?
    # Actually, let's use a simpler heuristic for odd m: constant sigma(s, j) = p_s.
    # Total space 6^m. Exhaustive for small m.

    for combo in iprod(range(nP), repeat=m):
        sigma = [combo[ ( (idx // (m*m)) + (idx % (m*m) // m) + (idx % m) ) % m ] for idx in range(n)]
        if _sa_score(sigma, arc_s, pa, n) == 0:
            res = {}
            for v in range(n):
                i, rem = divmod(v, m*m); j, k = divmod(rem, m)
                res[(i, j, k)] = _ALL_P3[sigma[v]]
            return res
    return None

# Let's see if we can just update construct_spike_sigma in core.py with a more reliable version.
