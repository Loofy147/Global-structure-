import random, math, time, sys
from core import _build_sa3, _sa_score, verify_sigma

def solve_P2(max_iter=5_000_000, seed=0, verbose=True):
    m=6; n, arc_s, pa = _build_sa3(m); nP=6
    rng = random.Random(seed)
    sigma = [rng.randrange(nP) for _ in range(n)]
    cs = _sa_score(sigma, arc_s, pa, n); bs = cs; best = sigma[:]
    T = 2.0; t0 = time.perf_counter()
    for it in range(max_iter):
        if cs == 0: break
        if cs <= 16:
            fixed = False
            for _ in range(500):
                mode = rng.random(); v1, v2 = rng.sample(range(n), 2); o1, o2 = sigma[v1], sigma[v2]
                if mode < 0.7: sigma[v1], sigma[v2] = rng.randrange(nP), rng.randrange(nP)
                else: sigma[v1], sigma[v2] = o2, o1
                ns = _sa_score(sigma, arc_s, pa, n)
                if ns < cs or (ns == cs and rng.random() < 0.4): cs = ns; fixed = True; break
                sigma[v1], sigma[v2] = o1, o2
            if fixed:
                if cs < bs: bs = cs; best = sigma[:]
                continue
        v = rng.randrange(n); old = sigma[v]; new = rng.randrange(nP)
        sigma[v] = new; ns = _sa_score(sigma, arc_s, pa, n); d = ns - cs
        if d < 0 or rng.random() < math.exp(-d/max(T, 1e-9)):
            cs = ns
            if cs < bs: bs = cs; best = sigma[:]
        else: sigma[v] = old
        if it % 10000 == 0:
            T = max(T*0.995, 0.001)
            if verbose:
                print(f"it={it} best={bs} cs={cs} T={T:.4f}")
                sys.stdout.flush()
    elapsed = time.perf_counter() - t0
    print(f"FINISHED: best={bs} time={elapsed:.1f}s")
    sys.stdout.flush()
    return best if bs == 0 else None

if __name__ == "__main__":
    solve_P2(max_iter=5000000)
