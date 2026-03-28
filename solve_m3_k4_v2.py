import math, random, time
from itertools import permutations, product

def solve_m3_k4():
    m = 3; k = 4; n = m**4; nP = 24
    all_p = list(permutations(range(k)))
    arc_s = [[0]*k for _ in range(n)]
    for v in range(n):
        i, r1 = divmod(v, m**3); j, r2 = divmod(r1, m**2); k_, l = divmod(r2, m)
        # Generators e_1, e_2, e_3, e_4
        arc_s[v][0] = ((i+1)%m)*m**3 + j*m**2 + k_*m + l
        arc_s[v][1] = i*m**3 + ((j+1)%m)*m**2 + k_*m + l
        arc_s[v][2] = i*m**3 + j*m**2 + ((k_+1)%m)*m + l
        arc_s[v][3] = i*m**3 + j*m**2 + k_*m + (l+1)%m

    # Try ALL fiber-uniform sigmas (24^3 = 13,824)
    def check_sigma(tab):
        for c in range(k):
            vis = [False]*n; comps = 0; s = 0
            while s < n:
                if not vis[s]:
                    comps += 1; cur = s
                    while not vis[cur]:
                        vis[cur] = True
                        i, r1 = divmod(cur, m**3); j, r2 = divmod(r1, m**2); k_, l = divmod(r2, m)
                        p = all_p[tab[(i+j+k_+l)%m]]
                        cur = arc_s[cur][p.index(c)]
                s += 1
            if comps != 1: return False
        return True

    print(f"Brute forcing 24^3 = 13,824 fiber-uniform sigmas for m=3, k=4...")
    for tab in product(range(nP), repeat=m):
        if check_sigma(tab):
            print(f"FOUND m=3, k=4 Hamiltonian Decomposition (fiber-uniform)!!!")
            print(f"Tab (fiber -> permutation index): {tab}")
            # Verify one more time with full coordinates
            return tab
    print("No fiber-uniform solution exists for m=3, k=4.")
    return None

if __name__ == "__main__":
    solve_m3_k4()
