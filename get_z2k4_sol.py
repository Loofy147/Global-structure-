import math, random, time
from itertools import permutations

def solve_k4(m, budget=200000, seed=42):
    k = 4; n = m**4; nP = 24; all_p = list(permutations(range(k)))
    def get_adj(v, c):
        coords = [ (v >> i) & 1 for i in range(4) ]
        coords[c] ^= 1
        return sum(coords[i] << i for i in range(4))
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
                        i, j, k_, l = (cur >> 3) & 1, (cur >> 2) & 1, (cur >> 1) & 1, cur & 1
                        tab_idx = i*4 + j*2 + k_
                        p = all_p[tab[tab_idx]]
                        cur = adj[cur][p.index(c)]
            total += (comps - 1)
        return total

    rng = random.Random(seed)
    table = [rng.randrange(nP) for _ in range(8)]
    cur_sc = score(table); bs = cur_sc; best_tab = list(table)
    T = 0.5; alpha = 0.99999

    for it in range(budget):
        idx = rng.randrange(8); old = table[idx]; table[idx] = rng.randrange(nP)
        sc = score(table)
        if sc < cur_sc or (T > 1e-6 and rng.random() < math.exp((cur_sc - sc)/T)):
            cur_sc = sc
            if cur_sc < bs: bs = cur_sc; best_tab = list(table)
            if cur_sc == 0:
                print(f"Z_2^4 SOL: {table}")
                return table
        else: table[idx] = old
        T *= alpha
        if it % 50000 == 0: print(f"it={it} sc={cur_sc} best={bs}", flush=True)
    return None

if __name__ == "__main__":
    solve_k4(2)
