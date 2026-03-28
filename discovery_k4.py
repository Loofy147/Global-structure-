import math, random, time
from itertools import permutations, product

def solve_k4(m, budget=10000, seed=42):
    k = 4; n = m**4; nP = 24
    all_p = list(permutations(range(k)))

    def get_adj(v, c):
        coords = [ (v // (m**i)) % m for i in range(4) ]
        coords[c] = (coords[c] + 1) % m
        return sum(coords[i] * (m**i) for i in range(4))

    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    def score(tab):
        total = 0
        for c in range(k):
            vis = bytearray(n); comps = 0
            for s in range(n):
                if not vis[s]:
                    comps += 1; cur = s
                    while not vis[cur]:
                        vis[cur] = 1
                        coords = [ (cur // (m**i)) % m for i in range(4) ]
                        # Fiber-uniform sigma(s, j): s=sum(coords)%m, j=coords[0]
                        f = sum(coords) % m
                        j = coords[0]
                        tab_idx = f*m + j
                        p = all_p[tab[tab_idx]]
                        cur = adj[cur][p.index(c)]
            total += (comps - 1)
        return total

    print(f"Stratified search for Z_{m}^4 (k=4) - table size {m*m}")
    rng = random.Random(seed)
    table = [rng.randrange(nP) for _ in range(m*m)]
    cur_sc = score(table)
    if cur_sc == 0: return table

    bs = cur_sc; best_tab = list(table)
    T = 5.0; alpha = 0.9999

    for it in range(budget):
        idx = rng.randrange(m*m); old = table[idx]; table[idx] = rng.randrange(nP)
        sc = score(table)
        if sc < cur_sc or rng.random() < math.exp((cur_sc - sc)/max(T, 1e-9)):
            cur_sc = sc
            if cur_sc < bs: bs = cur_sc; best_tab = list(table)
            if cur_sc == 0:
                print(f"SOLVED Z_{m}^4! It: {it}, Score: 0")
                return best_tab
        else: table[idx] = old
        T *= alpha
        if it % 5000 == 0 and it > 0:
            print(f"  it={it} score={cur_sc} best={bs} T={T:.4f}")

    return None

if __name__ == "__main__":
    print("Searching for Z_2^4 stratified solution...")
    # Brute force Z_2^4 (24^4 = 331,776)
    k = 4; m = 2; n = 16; nP = 24; all_p = list(permutations(range(k)))
    def get_adj(v, c):
        coords = [ (v // (2**i)) % 2 for i in range(4) ]
        coords[c] = (coords[c] + 1) % 2
        return sum(coords[i] * (2**i) for i in range(4))
    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    def check(tab):
        for c in range(k):
            vis = [False]*n; comps = 0
            for start in range(n):
                if not vis[start]:
                    comps += 1; cur = start
                    while not vis[cur]:
                        vis[cur] = True
                        coords = [ (cur // (2**i)) % 2 for i in range(4) ]
                        f = sum(coords) % 2; j = coords[0]
                        p = all_p[tab[f*2 + j]]
                        cur = adj[cur][p.index(c)]
            if comps != 1: return False
        return True

    found = False
    for tab in product(range(nP), repeat=4):
        if check(tab):
            print(f"SUCCESS! Z_2^4 stratified solution: {tab}")
            found = True; break
    if not found: print("Z_2^4: No stratified solution (s,j).")

    print("\nSearching for Z_4^4 stratified solution...")
    solve_k4(4, budget=100000, seed=42)
