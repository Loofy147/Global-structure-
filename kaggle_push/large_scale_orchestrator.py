import multiprocessing
import time
import os
import random
import math
import sys

# Inlined core functions to avoid dependency issues in Kaggle environment
def _build_sa3(m):
    n = m**3; k_ = 3
    arc_s = [[0]*k_ for _ in range(n)]
    for v in range(n):
        i, rem = divmod(v, m*m); j, k = divmod(rem, m)
        arc_s[v][0] = ((i+1)%m)*m*m + j*m + k
        arc_s[v][1] = i*m*m + ((j+1)%m)*m + k
        arc_s[v][2] = i*m*m + j*m + (k+1)%m
    pa = [[None]*k_ for _ in range(6)]
    from itertools import permutations
    ALL_P = list(permutations(range(3)))
    for pi, p in enumerate(ALL_P):
        for at, c in enumerate(p): pa[pi][c] = at
    return n, arc_s, pa

def _sa_score(sigma, arc_s, pa, n):
    vis = bytearray(n); total = 0
    for c in range(3):
        comps = 0; vis[:] = b'\x00' * n
        for s in range(n):
            if not vis[s]:
                comps += 1; cur = s
                while not vis[cur]: vis[cur] = 1; cur = arc_s[cur][pa[sigma[cur]][c]]
        total += (comps - 1)
    return total

def run_p2_worker(seed, max_iter, result_queue):
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
                if rng.random() < 0.7: sigma[v1], sigma[v2] = rng.randrange(nP), rng.randrange(nP)
                else: sigma[v1], sigma[v2] = o2, o1
                ns = _sa_score(sigma, arc_s, pa, n)
                if ns < cs or (ns == cs and rng.random() < 0.4): cs = ns; fixed = True; break
                sigma[v1], sigma[v2] = o1, o2
            if fixed:
                if cs < bs:
                    bs = cs; best = sigma[:]
                    result_queue.put(('p2_update', seed, bs, it))
                continue
        v = rng.randrange(n); old = sigma[v]; new = rng.randrange(nP)
        sigma[v] = new; ns = _sa_score(sigma, arc_s, pa, n); d = ns - cs
        if d < 0 or rng.random() < math.exp(-d/max(T, 1e-9)):
            cs = ns
            if cs < bs:
                bs = cs; best = sigma[:]
                result_queue.put(('p2_update', seed, bs, it))
        else: sigma[v] = old
        if it % 50000 == 0: T = max(T*0.99, 0.001)
    result_queue.put(('p2_final', seed, bs))

def main():
    result_queue = multiprocessing.Queue()
    processes = []
    # Kaggle kernels typically have 4 CPU cores
    n_procs = 4
    # Set a very large budget for 12 hours run
    p2_budget = 100_000_000

    for i in range(n_procs):
        p = multiprocessing.Process(target=run_p2_worker, args=(i, p2_budget, result_queue))
        p.start(); processes.append(p)

    best_p2 = 999; start_time = time.time()
    try:
        # Run for up to 11.5 hours
        while any(p.is_alive() for p in processes) and (time.time() - start_time < 11.5 * 3600):
            while not result_queue.empty():
                msg = result_queue.get()
                if msg[0] == 'p2_update':
                    _, seed, score, it = msg
                    if score < best_p2:
                        best_p2 = score
                        print(f"[*] NEW GLOBAL BEST P2: score={score} (seed={seed}, it={it})", flush=True)
            time.sleep(60)
    except KeyboardInterrupt:
        for p in processes: p.terminate()
    print(f"Kaggle run finished. Best P2: {best_p2}", flush=True)

if __name__ == "__main__":
    main()
