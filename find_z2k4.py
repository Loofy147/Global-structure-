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
                        s = sum(coords) % 2
                        j = coords[0]
                        # Stratification: sigma depends on (s, j)
                        # For m=2, s in {0,1}, j in {0,1}. Table size 4.
                        p = all_p[tab[s*2 + j]]
                        cur = adj[cur][p.index(c)]
            if comps != 1: return False
        return True

    print("Searching Z_2^4 (s, j) solutions...")
    for tab in product(range(nP), repeat=4):
        if check(tab):
            print(f"FOUND Z_2^4 solution: {tab}")
            return tab
    print("No (s, j) solution for Z_2^4.")

    def check_full_fiber(tab):
        for c in range(k):
            vis = [False]*n; comps = 0
            for start in range(n):
                if not vis[start]:
                    comps += 1; cur = start
                    while not vis[cur]:
                        vis[cur] = True
                        coords = [ (cur >> i) & 1 for i in range(4) ]
                        s = sum(coords) % 2
                        # Stratification: sigma depends only on s
                        p = all_p[tab[s]]
                        cur = adj[cur][p.index(c)]
            if comps != 1: return False
        return True

    print("Searching Z_2^4 fiber-only solutions...")
    for tab in product(range(nP), repeat=2):
        if check_full_fiber(tab):
            print(f"FOUND Z_2^4 fiber-only solution: {tab}")
            return tab
    print("No fiber-only solution for Z_2^4.")

if __name__ == "__main__":
    find_z2k4()
