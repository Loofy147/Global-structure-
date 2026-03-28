import math, random, time
from itertools import permutations

def solve_m3_k4():
    m = 3; k = 4; n = m**4; nP = 24
    all_p = list(permutations(range(k)))
    arc_s = [[0]*k for _ in range(n)]
    for v in range(n):
        i, r1 = divmod(v, m**3); j, r2 = divmod(r1, m**2); k_, l = divmod(r2, m)
        arc_s[v][0] = ((i+1)%m)*m**3 + j*m**2 + k_*m + l
        arc_s[v][1] = i*m**3 + ((j+1)%m)*m**2 + k_*m + l
        arc_s[v][2] = i*m**3 + j*m**2 + ((k_+1)%m)*m + l
        arc_s[v][3] = i*m**3 + j*m**2 + k_*m + (l+1)%m

    pa = [[None]*k for _ in range(nP)]
    for pi, p in enumerate(all_p):
        for at, c in enumerate(p): pa[pi][c] = at

    def score(sigma):
        total = 0
        for c in range(k):
            vis = bytearray(n); comps = 0
            for s in range(n):
                if not vis[s]:
                    comps += 1; cur = s
                    while not vis[cur]: vis[cur] = 1; cur = arc_s[cur][pa[sigma[cur]][c]]
            total += (comps - 1)
        return total

    # Fiber-uniform search: sigma depends on (i+j+k+l)%m
    # Space: 24^3 = 13,824. Very small.
    for seed in range(5):
        rng = random.Random(seed)
        table = [rng.randrange(nP) for _ in range(m)]
        def get_sig(tab):
            sig = [0]*n
            for v in range(n):
                i, r1 = divmod(v, m**3); j, r2 = divmod(r1, m**2); k_, l = divmod(r2, m)
                sig[v] = tab[(i+j+k_+l)%m]
            return sig

        cur_tab = list(table)
        cur_sig = get_sig(cur_tab)
        cur_sc = score(cur_sig)

        if cur_sc == 0:
            print(f"m=3, k=4 SOLVED (fiber-uniform)!!! Tab: {cur_tab}")
            return cur_tab

        # SA
        T = 10.0; alpha = 0.99
        for _ in range(2000):
            idx = rng.randrange(m); old = cur_tab[idx]
            cur_tab[idx] = rng.randrange(nP)
            sig = get_sig(cur_tab); sc = score(sig)
            if sc < cur_sc or rng.random() < math.exp((cur_sc - sc)/T):
                cur_sc = sc
                if cur_sc == 0:
                    print(f"m=3, k=4 SOLVED (fiber-uniform)!!! Tab: {cur_tab}")
                    return cur_tab
            else:
                cur_tab[idx] = old
            T *= alpha

    print("m=3, k=4 NOT SOLVED locally.")
    return None

if __name__ == "__main__":
    solve_m3_k4()
