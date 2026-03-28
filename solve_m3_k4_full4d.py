import math, random, time
from itertools import permutations

def solve_m3_k4_full4d():
    m = 3; k = 4; n = m**4; nP = 24
    all_p = list(permutations(range(k)))

    def get_adj(v, c):
        coords = [ (v // (3**i)) % 3 for i in range(4) ]
        coords[c] = (coords[c] + 1) % 3
        return sum(coords[i] * (3**i) for i in range(4))

    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]
    pa = [[p.index(c) for c in range(k)] for p in all_p]

    def get_score(sigma):
        total = 0
        for c in range(k):
            vis = bytearray(n); comps = 0
            for s in range(n):
                if not vis[s]:
                    comps += 1; cur = s
                    while not vis[cur]:
                        vis[cur] = 1
                        cur = adj[cur][pa[sigma[cur]][c]]
            total += (comps - 1)
        return total

    print(f"Full 4D SA for Z_3^4 (81 nodes, k=4)...")
    for seed in range(3):
        rng = random.Random(seed)
        sigma = [rng.randrange(nP) for _ in range(n)]
        cur_sc = get_score(sigma)
        bs = cur_sc; best = list(sigma)

        T = 2.0; alpha = 0.99999
        t0 = time.perf_counter()

        for it in range(500000):
            if cur_sc == 0: break

            # Repair mode
            if cur_sc <= 2:
                vlist = list(range(n)); rng.shuffle(vlist)
                fixed = False
                for v in vlist:
                    old = sigma[v]
                    for pi in rng.sample(range(nP), nP):
                        if pi == old: continue
                        sigma[v] = pi
                        sc = get_score(sigma)
                        if sc < cur_sc:
                            cur_sc = sc; fixed = True
                            if cur_sc < bs: bs = cur_sc; best = list(sigma)
                            break
                        sigma[v] = old
                    if fixed: break
                if fixed: continue

            v = rng.randrange(n); old = sigma[v]; new = rng.randrange(nP)
            if new == old: continue
            sigma[v] = new; sc = get_score(sigma); d = sc - cur_sc
            if d < 0 or rng.random() < math.exp(-d/max(T, 1e-9)):
                cur_sc = sc
                if cur_sc < bs: bs = cur_sc; best = list(sigma)
            else:
                sigma[v] = old

            T *= alpha
            if (it+1) % 50000 == 0:
                print(f"  seed={seed} it={it+1} score={cur_sc} best={bs} T={T:.4f}")

        if bs == 0:
            print(f"SOLVED Z_3^4 full 4D!!! Seed {seed}, it {it}, time {time.perf_counter()-t0:.1f}s")
            return best

    print(f"NOT SOLVED Z_3^4 full 4D, best score: {bs}")
    return None

if __name__ == "__main__":
    solve_m3_k4_full4d()
