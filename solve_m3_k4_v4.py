import math, random, time
from itertools import permutations, product

def solve_m3_k4():
    m = 3; k = 4; n = m**4; nP = 24
    all_p = list(permutations(range(k)))

    def get_adj(v, c):
        coords = [ (v // (3**i)) % 3 for i in range(4) ]
        coords[c] = (coords[c] + 1) % 3
        return sum(coords[i] * (3**i) for i in range(4))

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
                        # Sigma(i,j,k,l) = sigma(i,j,k) fiber-structured
                        i, j, k_, l = (cur // 27) % 3, (cur // 9) % 3, (cur // 3) % 3, cur % 3
                        # We use a table of size 27
                        tab_idx = i*9 + j*3 + k_
                        p = all_p[tab[tab_idx]]
                        cur = adj[cur][p[c]]
            total += (comps - 1)
        return total

    print(f"Fiber-structured search for Z_3^4 (k=4) - table size 27")
    best_score = 999
    for seed in range(5):
        rng = random.Random(seed)
        table = [rng.randrange(nP) for _ in range(27)]
        cur_sc = score(table)
        if cur_sc == 0: return table

        T = 5.0; alpha = 0.999
        for it in range(5000):
            idx = rng.randrange(27); old = table[idx]; table[idx] = rng.randrange(nP)
            sc = score(table)
            if sc < cur_sc or rng.random() < math.exp((cur_sc - sc)/max(T, 1e-9)):
                cur_sc = sc
                if cur_sc < best_score: best_score = cur_sc
                if cur_sc == 0:
                    print(f"SOLVED Z_3^4 fiber-structured!!! Seed {seed}, it {it}")
                    return table
            else: table[idx] = old
            T *= alpha

    print(f"NOT SOLVED Z_3^4, best score: {best_score}")
    return None

if __name__ == "__main__":
    solve_m3_k4()
