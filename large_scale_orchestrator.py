import multiprocessing
import time
import os
import random
import math
import sys
from core import _build_sa3, _sa_score, verify_sigma, solve_spike

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

def run_spike_worker(m, max_iter, result_queue):
    sol = solve_spike(m, max_iter=max_iter)
    if sol: result_queue.put(('spike_found', m))
    else: result_queue.put(('spike_failed', m))

def main():
    result_queue = multiprocessing.Queue()
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=run_p2_worker, args=(i, 1000000, result_queue))
        p.start(); processes.append(p)
    for i in range(1):
        p = multiprocessing.Process(target=run_spike_worker, args=(7, 200000, result_queue))
        p.start(); processes.append(p)
    best_p2 = 999; start_time = time.time()
    try:
        while any(p.is_alive() for p in processes):
            while not result_queue.empty():
                msg = result_queue.get()
                if msg[0] == 'p2_update':
                    _, seed, score, it = msg
                    if score < best_p2:
                        best_p2 = score
                        print(f"[*] NEW GLOBAL BEST P2: score={score} (seed={seed}, it={it})", flush=True)
                elif msg[0] == 'spike_found':
                    print(f"[!] BREAKTHROUGH: m={msg[1]} Spike Found!", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        for p in processes: p.terminate()
    print(f"Large-scale run finished in {time.time()-start_time:.1f}s. Best P2: {best_p2}", flush=True)

if __name__ == "__main__":
    main()
