import math, random, time
from itertools import permutations

def find_z2k4():
    m = 2; k = 4; n = 16; nP = 24
    all_p = list(permutations(range(k)))

    def get_adj(v, c):
        coords = [ (v >> i) & 1 for i in range(4) ]
        coords[c] ^= 1
        return sum(coords[i] << i for i in range(4))

    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    def get_score(sigma):
        tot = 0
        for c in range(k):
            vis = [False]*n; comps = 0
            for start in range(n):
                if not vis[start]:
                    comps += 1; cur = start
                    while not vis[cur]:
                        vis[cur] = True
                        p = all_p[sigma[cur]]
                        cur = adj[cur][p[c]]
            tot += (comps - 1)
        return tot

    for seed in range(50):
        rng = random.Random(seed)
        sigma = [rng.randrange(nP) for _ in range(n)]
        cur_sc = get_score(sigma)

        T = 2.0; alpha = 0.99
        for it in range(1000):
            if cur_sc == 0: break
            idx = rng.randrange(n); old = sigma[idx]; sigma[idx] = rng.randrange(nP)
            sc = get_score(sigma)
            if sc < cur_sc or rng.random() < math.exp((cur_sc - sc)/T):
                cur_sc = sc
            else: sigma[idx] = old
            T *= alpha

        if cur_sc == 0:
            print(f"FOUND: {sigma}")
            return sigma

if __name__ == "__main__":
    find_z2k4()
