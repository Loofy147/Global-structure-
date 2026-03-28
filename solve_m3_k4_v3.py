import math, random, time
from itertools import permutations, product

def solve_m3_k4():
    m = 3; k = 4; n = m**4; nP = 24
    all_p = list(permutations(range(k)))

    # Adjacency for Z_3^4 with generators e_1, e_2, e_3, e_4
    def get_adj(v, c):
        coords = [ (v // (3**i)) % 3 for i in range(4) ]
        coords[c] = (coords[c] + 1) % 3
        return sum(coords[i] * (3**i) for i in range(4))

    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    def check_sigma(tab):
        for c in range(k):
            vis = [False]*n; comps = 0
            for s in range(n):
                if not vis[s]:
                    comps += 1; cur = s
                    while not vis[cur]:
                        vis[cur] = True
                        coords = [ (cur // (3**i)) % 3 for i in range(4) ]
                        # Fiber map: sum(coords) mod 3
                        f = sum(coords) % 3
                        p = all_p[tab[f]]
                        gen_idx = p[c]
                        cur = adj[cur][gen_idx]
                if comps > 1: return False
            if comps != 1: return False
        return True

    print(f"Brute forcing Z_3^4 fiber-uniform sigmas (24^3 = 13,824)...")
    for tab in product(range(nP), repeat=m):
        if check_sigma(tab):
            print(f"FOUND FOUND FOUND Z_3^4 solution: {tab}")
            return tab
    print("NO fiber-uniform solution for Z_3^4.")
    return None

if __name__ == "__main__":
    solve_m3_k4()
