import math, random, time
from itertools import permutations, product

def solve_k4(m, budget=10000, seed=42):
    k = 4; n = m**4; nP = 24; all_p = list(permutations(range(k)))
    def get_adj(v, c):
        coords = [ (v // (m**i)) % m for i in range(4) ]
        coords[c] = (coords[c] + 1) % m
        return sum(coords[i] * (m**i) for i in range(4))
    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    def score(tab):
        total = 0
        for c in range(k):
            vis = bytearray(n); comps = 0
            for start in range(n):
                if not vis[start]:
                    comps += 1; cur = start
                    while not vis[cur]:
                        vis[cur] = 1
                        i, j, k_, l = (cur // (m**3)) % m, (cur // (m**2)) % m, (cur // m) % m, cur % m
                        tab_idx = i*(m*m) + j*m + k_
                        p = all_p[tab[tab_idx]]
                        cur = adj[cur][p.index(c)]
            total += (comps - 1)
        return total

    print(f"Stratified search for Z_{m}^4 (k=4) - table size {m*m*m}")
    rng = random.Random(seed)
    table = [rng.randrange(nP) for _ in range(m*m*m)]
    cur_sc = score(table); bs = cur_sc; best_tab = list(table)
    T = 0.5; alpha = 0.99999

    for it in range(budget):
        idx = rng.randrange(m*m*m); old = table[idx]; table[idx] = rng.randrange(nP)
        sc = score(table)
        if sc < cur_sc or (T > 1e-6 and rng.random() < math.exp((cur_sc - sc)/T)):
            cur_sc = sc
            if cur_sc < bs: bs = cur_sc; best_tab = list(table)
            if cur_sc == 0:
                print(f"SOLVED Z_{m}^4! It: {it}, Seed: {seed}")
                sys.stdout.flush()
                return best_tab
        else: table[idx] = old
        T *= alpha
        if it % 10000 == 0 and it > 0:
            print(f"  it={it} score={cur_sc} best={bs} T={T:.6f}", flush=True)
    return None

if __name__ == "__main__":
    import sys
    print("Searching for Z_2^4 stratified solution (size 8)...", flush=True)
    sol2 = solve_k4(2, budget=100000, seed=42)
    if sol2: print(f"Z_2^4 SOL: {sol2}", flush=True)

    print("\nSearching for Z_4^4 stratified solution (size 64)...", flush=True)
    sol4 = solve_k4(4, budget=2000000, seed=123)
    if sol4: print(f"Z_4^4 SOL: {sol4}", flush=True)
