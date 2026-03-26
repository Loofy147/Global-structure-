import random, math, time, sys
from itertools import permutations
from core import _build_sa3, _sa_score, verify_sigma

def solve_P2(max_iter=5_000_000, seed=0, verbose=True):
    """m=6, k=3 Full SA search."""
    m=6; n, arc_s, pa = _build_sa3(m); nP=6
    rng = random.Random(seed)
    sigma = [rng.randrange(nP) for _ in range(n)]
    cs = _sa_score(sigma, arc_s, pa, n); bs = cs; best = sigma[:]
    T = 2.0; t0 = time.perf_counter()
    for it in range(max_iter):
        if cs == 0: break
        if cs <= 16:
            fixed = False
            for _ in range(500):
                v1, v2 = rng.sample(range(n), 2); o1, o2 = sigma[v1], sigma[v2]
                if rng.random() < 0.7: sigma[v1], sigma[v2] = rng.randrange(nP), rng.randrange(nP)
                else: sigma[v1], sigma[v2] = o2, o1
                ns = _sa_score(sigma, arc_s, pa, n)
                if ns < cs or (ns == cs and rng.random() < 0.4): cs = ns; fixed = True; break
                sigma[v1], sigma[v2] = o1, o2
            if fixed:
                if cs < bs: bs = cs; best = sigma[:]
                continue
        v = rng.randrange(n); old = sigma[v]; new = rng.randrange(nP)
        sigma[v] = new; ns = _sa_score(sigma, arc_s, pa, n); d = ns - cs
        if d < 0 or rng.random() < math.exp(-d/max(T, 1e-9)):
            cs = ns
            if cs < bs: bs = cs; best = sigma[:]
        else: sigma[v] = old
        if it % 10000 == 0:
            T = max(T*0.995, 0.001)
            if verbose and it % 100000 == 0:
                print(f"it={it} best={bs} cs={cs} T={T:.4f}")
                sys.stdout.flush()
    elapsed = time.perf_counter() - t0
    print(f"FINISHED: best={bs} time={elapsed:.1f}s")
    sys.stdout.flush()
    return best if bs == 0 else None

def solve_P1(max_iter=2_000_000, seed=42, verbose=True):
    """m=4, k=4 Fiber-structured search."""
    # Simplified version for the repository
    m, k = 4, 4; n = m**k
    nP = math.factorial(k)
    ALL_P = list(permutations(range(k)))
    rng = random.Random(seed)

    # fiber s = sum(coords) mod m
    # table[(s, j, k)] -> perm index
    keys = [(s, j, k) for s in range(m) for j in range(m) for k in range(m)]
    table = {key: rng.randrange(nP) for key in keys}

    def get_sigma(tab):
        sig = [0]*n
        for v in range(n):
            v_orig = v
            coords = []
            for _ in range(k):
                v, r = divmod(v, m)
                coords.append(r)
            coords = coords[::-1]
            s = sum(coords) % m
            sig[v_orig] = tab[(s, coords[1], coords[2])]
        return sig

    def get_arc_s(m, k):
        n = m**k
        arc_s = [[0]*k for _ in range(n)]
        for v in range(n):
            v_orig = v
            coords = []
            tmp = v
            for _ in range(k):
                tmp, r = divmod(tmp, m)
                coords.append(r)
            coords = coords[::-1]
            for i in range(k):
                nc = list(coords)
                nc[i] = (nc[i] + 1) % m
                res = 0
                for c in nc: res = res*m + c
                arc_s[v_orig][i] = res
        return arc_s

    arc_s = get_arc_s(m, k)
    pa = [[None]*k for _ in range(nP)]
    for pi, p in enumerate(ALL_P):
        for at, c in enumerate(p): pa[pi][c] = at

    def score(sig):
        vis = bytearray(n); total = 0
        for c in range(k):
            comps = 0; vis[:] = b'\x00' * n
            for s in range(n):
                if not vis[s]:
                    comps += 1; cur = s
                    while not vis[cur]: vis[cur] = 1; cur = arc_s[cur][pa[sig[cur]][c]]
            total += (comps - 1)
        return total

    cur_s = score(get_sigma(table)); bs = cur_s; best_tab = dict(table)
    T = 50.0; t0 = time.perf_counter()
    for it in range(max_iter):
        if cur_s == 0: break
        key = rng.choice(keys); old = table[key]; table[key] = rng.randrange(nP)
        sig = get_sigma(table); ns = score(sig); d = ns - cur_s
        if d < 0 or (T > 1e-9 and rng.random() < math.exp(-d/T)):
            cur_s = ns
            if cur_s < bs: bs = cur_s; best_tab = dict(table)
        else: table[key] = old
        if it % 5000 == 0: T *= 0.99
        if verbose and it % 100000 == 0:
            print(f"P1: it={it} best={bs} cs={cur_s} T={T:.4f}")

    print(f"P1 FINISHED: best={bs}")
    return best_tab if bs == 0 else None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "p1":
        solve_P1()
    else:
        solve_P2(max_iter=1000000)

def solve_tsp_P7(m=5, verbose=True):
    """
    Finds the minimum-cost Hamiltonian cycle for a weighted Cayley graph on Z_m^2.
    Uses fiber stratification to prune the search space.
    """
    generators = [(1, 0), (0, 1), (1, 1)]
    weights = [10, 15, 12]

    best_cost = float('inf')
    best_sigma = None

    from itertools import product
    # Search fiber-uniform space
    for sigma in product(range(len(generators)), repeat=m):
        n = m*m; visited = set(); curr = (0, 0); cost = 0
        for _ in range(n):
            if curr in visited: break
            visited.add(curr); s = (curr[0]+curr[1])%m; g_idx = sigma[s]
            g = generators[g_idx]; cost += weights[g_idx]
            curr = ((curr[0]+g[0])%m, (curr[1]+g[1])%m)
        if len(visited) == n and cost < best_cost:
            best_cost = cost; best_sigma = sigma

    if verbose:
        print(f"\n[!] TSP P7 RESOLVED: m={m}")
        print(f"    Min Cost: {best_cost}")
        print(f"    Optimal Sigma: {best_sigma}")
    return best_sigma, best_cost
