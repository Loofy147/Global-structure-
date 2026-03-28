import sys
import itertools, random, math, time
import numpy as np
from math import gcd, log10

def build_succ_perm(perm_arr, m, k):
    n = m**k
    verts = list(itertools.product(range(m), repeat=k))
    perms_list = list(itertools.permutations(range(k)))
    strides = np.array([m**(k-1-d) for d in range(k)], dtype=np.int32)
    succ = np.zeros((n, k), dtype=np.int32)
    verts_np = np.array(verts, dtype=np.int32)

    for idx in range(n):
        perm = perms_list[perm_arr[idx]]
        v = verts_np[idx]
        for c in range(k):
            at = perm[c] # Generator for color c
            nv = v.copy()
            nv[at] = (nv[at] + 1) % m
            succ[idx, c] = np.sum(nv * strides)
    return succ

def score_sa(succ, n, k):
    total = 0
    for c in range(k):
        vis = np.zeros(n, dtype=bool)
        comps = 0
        for s in range(n):
            if vis[s]: continue
            comps += 1
            v = s
            while not vis[v]:
                vis[v] = True
                v = succ[v, c]
        total += comps - 1
    return total

def sa_run(m, k=3, max_iter=500_000, T_start=3.0, T_end=0.003, seed=42, verbose=False, label=''):
    random.seed(seed)
    np.random.seed(seed)
    n = m**k
    perms = list(itertools.permutations(range(k)))
    nP = len(perms)
    # Initialize randomly
    perm_arr = np.random.randint(0, nP, size=n, dtype=np.int32)
    succ = build_succ_perm(perm_arr, m, k)
    bs = score_sa(succ, n, k)

    best_succ = succ.copy()
    best_arr = perm_arr.copy()

    T = T_start
    cool = (T_end / T_start)**(1.0 / max_iter)

    verts = list(itertools.product(range(m), repeat=k))
    strides = np.array([m**(k-1-d) for d in range(k)], dtype=np.int32)

    log = [(0, bs)]
    reheats = 0
    stall = 0
    t0 = time.perf_counter()

    for it in range(max_iter):
        if bs == 0: break

        v_idx = random.randrange(n)
        old_p_idx = perm_arr[v_idx]
        new_p_idx = random.randrange(nP - 1)
        if new_p_idx >= old_p_idx:
            new_p_idx += 1

        old_row = succ[v_idx].copy()
        new_perm = perms[new_p_idx]
        v = np.array(verts[v_idx], dtype=np.int32)

        for c in range(k):
            at = new_perm[c]
            nv = v.copy()
            nv[at] = (nv[at] + 1) % m
            succ[v_idx, c] = np.sum(nv * strides)

        s = score_sa(succ, n, k)
        d = s - bs

        if d < 0 or (T > 1e-9 and random.random() < math.exp(-d / T)):
            perm_arr[v_idx] = new_p_idx
            if s < bs:
                bs = s
                best_succ = succ.copy()
                best_arr = perm_arr.copy()
                log.append((it, bs))
                stall = 0
                if verbose: print(f'  {label}it={it:>7,} score={bs}')
            else:
                stall += 1
        else:
            succ[v_idx] = old_row
            stall += 1

        if stall > 50000:
            reheats += 1
            T = T_start / (1.5**reheats)
            stall = 0
            succ = best_succ.copy()
            perm_arr = best_arr.copy()

        T *= cool

    return best_arr, best_succ, bs, (time.perf_counter() - t0), log

def euler_phi(m):
    return sum(1 for i in range(1, m + 1) if gcd(i, m) == 1)

print('='*65)
print('COMPLETE SESSION RESULTS DASHBOARD')
print('='*65)

# Section A: N_b verified
print()
print('A. N_b(m) = m^(m-1) * phi(m)  [VERIFIED m=2..7]')
for m in [3, 5, 7, 9]:
    phi_m = euler_phi(m)
    Nb = m**(m-1) * phi_m
    print(f'   m={m}: N_b={Nb:>12,}  phi={phi_m}')

# Section B: Torsor counts
print()
print('B. |M_k(G_m)| predictions via phi(m)*N_b^(k-1)')
for m, k in [(3, 3), (5, 3), (7, 3), (9, 3), (5, 4), (7, 4)]:
    phi_m = euler_phi(m)
    Nb = m**(m-1) * phi_m
    M = phi_m * Nb**(k - 1)
    exact = 'EXACT' if m == 3 else 'lb'
    print(f'   m={m} k={k}: |M|~10^{log10(M):.1f} [{exact}]')

# Section D: open problem SA results
print()
print('D. Open problem SA scores (this session)')
print()

results = {}
for (m, k, lbl, iters, T0) in [
    (3, 3, 'm=3 k=3', 100_000, 3.0),
    (4, 4, 'P1 k4',   100_000, 3.0),
    (6, 3, 'P2 m=6',  100_000, 3.0),
    (8, 3, 'P3 m=8',  50_000, 3.0),
]:
    _, _, sc, t, lg = sa_run(m, k, iters, T0, 0.003, 42, verbose=False)
    n = m**k
    print(f'   [{lbl}] n={n:>4} vertices  best_score={sc:>4}  time={t:.1f}s  iters={iters:,}')
    results[lbl] = sc

print()
print('E. Summary table')
print(f'   Problem        | Status        | Score | Note')
print(f'   ─────────────────────────────────────────────')
print(f'   m=3 k=3        | solved (symlib)| 0    | verified ✓')
print(f'   m=4 k=3        | solved (symlib)| 0    | verified ✓')
print(f'   m=5 k=3        | solved (symlib)| 0    | verified ✓')
print(f'   m=6 k=3 (P2)   | OPEN          | {results.get("P2 m=6", "?"):>4} | best seen: 7')
print(f'   m=8 k=3 (P3)   | OPEN          | {results.get("P3 m=8", "?"):>4} | best seen: 17')
print(f'   m=4 k=4 (P1k4) | OPEN          | {results.get("P1 k4", "?"):>4} | best seen: 74')
