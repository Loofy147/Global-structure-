import math, random, time
from itertools import permutations, product

def solve_m2_k4():
    m = 2; k = 4; n = m**4; nP = 24
    all_p = list(permutations(range(k)))

    def get_adj(v, c):
        coords = [ (v // (2**i)) % 2 for i in range(4) ]
        coords[c] = (coords[c] + 1) % 2
        return sum(coords[i] * (2**i) for i in range(4))

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
                        i, j, k_, l = (cur >> 3) & 1, (cur >> 2) & 1, (cur >> 1) & 1, cur & 1
                        tab_idx = i*4 + j*2 + k_
                        p = all_p[tab[tab_idx]]
                        cur = adj[cur][p[c]]
            total += (comps - 1)
        return total

    print(f"Fiber-structured search for Z_2^4 (k=4) - table size 8")
    for seed in range(5):
        rng = random.Random(seed)
        table = [rng.randrange(nP) for _ in range(8)]
        cur_sc = score(table)
        if cur_sc == 0: return table

        T = 5.0; alpha = 0.99
        for it in range(10000):
            idx = rng.randrange(8); old = table[idx]; table[idx] = rng.randrange(nP)
            sc = score(table)
            if sc < cur_sc or rng.random() < math.exp((cur_sc - sc)/max(T, 1e-9)):
                cur_sc = sc
                if cur_sc == 0:
                    print(f"SOLVED Z_2^4 fiber-structured!!! Tab: {table}")
                    return table
            else: table[idx] = old
            T *= alpha

    print(f"NOT SOLVED Z_2^4 locally.")
    return None

if __name__ == "__main__":
    solve_m2_k4()
