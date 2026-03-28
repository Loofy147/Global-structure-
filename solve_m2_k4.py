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

    def check_sigma(tab):
        for c in range(k):
            vis = [False]*n; comps = 0
            for s in range(n):
                if not vis[s]:
                    comps += 1; cur = s
                    while not vis[cur]:
                        vis[cur] = True
                        coords = [ (cur // (2**i)) % 2 for i in range(4) ]
                        f = sum(coords) % 2
                        p = all_p[tab[f]]
                        cur = adj[cur][p[c]]
                if comps > 1: return False
            if comps != 1: return False
        return True

    print(f"Brute forcing Z_2^4 fiber-uniform sigmas (24^2 = 576)...")
    sols = []
    for tab in product(range(nP), repeat=m):
        if check_sigma(tab):
            sols.append(tab)

    if sols:
        print(f"SUCCESS! Found {len(sols)} fiber-uniform solutions for Z_2^4.")
        print(f"Example solution: {sols[0]}")
        # Let's map it to permutations
        print(f"Fiber 0: {all_p[sols[0][0]]}")
        print(f"Fiber 1: {all_p[sols[0][1]]}")
    else:
        print("NO fiber-uniform solution for Z_2^4.")

if __name__ == "__main__":
    solve_m2_k4()
