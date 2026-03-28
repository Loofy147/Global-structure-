import math, random, time
from itertools import permutations

def solve_m4_k4():
    m = 4; k = 4; n = 256; nP = 24
    all_p = list(permutations(range(k)))

    def get_adj(v, c):
        coords = [ (v // (4**i)) % 4 for i in range(4) ]
        coords[c] = (coords[c] + 1) % 4
        return sum(coords[i] * (4**i) for i in range(4))

    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    def get_score(tab):
        tot = 0
        for c in range(k):
            vis = bytearray(n); comps = 0
            for start in range(n):
                if not vis[start]:
                    comps += 1; cur = start
                    while not vis[cur]:
                        vis[cur] = 1
                        coords = [ (cur // (4**i)) % 4 for i in range(4) ]
                        s = sum(coords) % 4
                        j = coords[0]
                        # Table size 16
                        p = all_p[tab[s*4 + j]]
                        cur = adj[cur][p.index(c)]
            tot += (comps - 1)
        return tot

    print("Searching Z_4^4 (s, j) solutions (table size 16)...")
    for seed in range(10):
        rng = random.Random(seed)
        table = [rng.randrange(nP) for _ in range(16)]
        cur_sc = get_score(table)

        T = 2.0; alpha = 0.9999
        for it in range(50000):
            if cur_sc == 0: break
            idx = rng.randrange(16); old = table[idx]; table[idx] = rng.randrange(nP)
            sc = get_score(table)
            if sc < cur_sc or (T > 1e-6 and rng.random() < math.exp((cur_sc - sc)/T)):
                cur_sc = sc
            else: table[idx] = old
            T *= alpha

        if cur_sc == 0:
            print(f"FOUND Z_4^4 stratified solution: {table} (seed {seed})")
            return table
        print(f"  Seed {seed} finished, best score {cur_sc}")

if __name__ == "__main__":
    solve_m4_k4()
