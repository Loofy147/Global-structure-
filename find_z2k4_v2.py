import math, random, time
from itertools import permutations, product

def find_z2k4():
    m = 2; k = 4; n = 16; nP = 24
    all_p = list(permutations(range(k)))

    def get_adj(v, c):
        coords = [ (v >> i) & 1 for i in range(4) ]
        coords[c] ^= 1
        return sum(coords[i] << i for i in range(4))

    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    def check(tab):
        for c in range(k):
            vis = [False]*n; comps = 0
            for start in range(n):
                if not vis[start]:
                    comps += 1; cur = start
                    while not vis[cur]:
                        vis[cur] = True
                        coords = [ (cur >> i) & 1 for i in range(4) ]
                        v1, v2, v3, v4 = coords
                        # Try a different stratification: sigma depends on (v1, v2, v3)
                        # This is a "slice-uniform" approach.
                        p = all_p[tab[v1*4 + v2*2 + v3]]
                        cur = adj[cur][p.index(c)]
            if comps != 1: return False
        return True

    print("Searching Z_2^4 (v1, v2, v3) solutions (table size 8)...")
    best_sc = 999
    for seed in range(20):
        rng = random.Random(seed)
        table = [rng.randrange(nP) for _ in range(8)]
        def get_score(t):
            tot = 0
            for c in range(k):
                vis = [False]*n; comps = 0
                for start in range(n):
                    if not vis[start]:
                        comps += 1; cur = start
                        while not vis[cur]:
                            vis[cur] = True
                            coords = [ (cur >> i) & 1 for i in range(4) ]
                            v1, v2, v3, v4 = coords
                            p = all_p[t[v1*4 + v2*2 + v3]]
                            cur = adj[cur][p.index(c)]
                tot += (comps - 1)
            return tot

        cur_sc = get_score(table)
        if cur_sc == 0:
            print(f"FOUND Z_2^4 slice-uniform solution: {table}")
            return table

        T = 2.0; alpha = 0.999
        for it in range(5000):
            idx = rng.randrange(8); old = table[idx]; table[idx] = rng.randrange(nP)
            sc = get_score(table)
            if sc < cur_sc or rng.random() < math.exp((cur_sc - sc)/T):
                cur_sc = sc
                if cur_sc == 0:
                    print(f"FOUND Z_2^4 slice-uniform solution: {table}")
                    return table
            else: table[idx] = old
            T *= alpha
        if cur_sc < best_sc: best_sc = cur_sc

    print(f"No slice-uniform solution for Z_2^4. Best score: {best_sc}")

if __name__ == "__main__":
    find_z2k4()
