import multiprocessing
import time
import os
import random
import math
import sys
from itertools import permutations

# --- P2: m=6, k=3 (Full 3D) ---
def _build_sa3(m):
    n = m**3; k_ = 3
    arc_s = [[0]*k_ for _ in range(n)]
    for v in range(n):
        i, rem = divmod(v, m*m); j, k = divmod(rem, m)
        arc_s[v][0] = ((i+1)%m)*m*m + j*m + k
        arc_s[v][1] = i*m*m + ((j+1)%m)*m + k
        arc_s[v][2] = i*m*m + j*m + (k+1)%m
    pa = [[None]*k_ for _ in range(6)]
    ALL_P = list(permutations(range(3)))
    for pi, p in enumerate(ALL_P):
        for at, c in enumerate(p): pa[pi][c] = at
    return n, arc_s, pa

def _sa_score3(sigma, arc_s, pa, n):
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
    cs = _sa_score3(sigma, arc_s, pa, n); bs = cs; best = sigma[:]
    T_init = 3.0; T_min = 0.003
    cool = (T_min/T_init)**(1.0/max_iter)
    T = T_init; stall=0; reheats=0; t0=time.perf_counter()
    for it in range(max_iter):
        if cs == 0: break
        if cs <= 2:
            vlist = list(range(n)); rng.shuffle(vlist)
            fixed = False
            for v in vlist:
                old = sigma[v]
                for pi in rng.sample(range(nP), nP):
                    if pi == old: continue
                    sigma[v] = pi
                    ns = _sa_score3(sigma, arc_s, pa, n)
                    if ns < cs:
                        cs = ns; fixed = True
                        if cs < bs: bs=cs; best=sigma[:]
                        break
                    sigma[v] = old
                if fixed: break
            if cs == 0: break
            T *= cool; continue
        v = rng.randrange(n); old = sigma[v]; new = rng.randrange(nP)
        if new == old: T *= cool; continue
        sigma[v] = new
        ns = _sa_score3(sigma, arc_s, pa, n)
        d = ns - cs
        if d < 0 or rng.random() < math.exp(-d/max(T, 1e-9)):
            cs = ns
            if cs < bs: bs=cs; best=sigma[:]; stall=0
            else: stall += 1
        else: sigma[v] = old; stall += 1
        if stall > 80_000:
            T = T_init/(2**reheats); reheats+=1; stall=0
            sigma = best[:]; cs = bs
        T *= cool
        if (it+1) % 1_000_000 == 0:
            result_queue.put(('p2_update', seed, bs, it+1))
    result_queue.put(('p2_final', seed, bs, best if bs==0 else None))

# --- P1: m=4, k=4 (Fiber-Structured) ---
def _build_sa4(m):
    n = m**4; k_ = 4
    arc_s = [[0]*k_ for _ in range(n)]
    for v in range(n):
        i, r1 = divmod(v, m**3); j, r2 = divmod(r1, m**2); k, l = divmod(r2, m)
        arc_s[v][0] = ((i+1)%m)*m**3 + j*m**2 + k*m + l
        arc_s[v][1] = i*m**3 + ((j+1)%m)*m**2 + k*m + l
        arc_s[v][2] = i*m**3 + j*m**2 + ((k+1)%m)*m + l
        arc_s[v][3] = i*m**3 + j*m**2 + k*m + (l+1)%m
    ALL_P4 = list(permutations(range(4)))
    nP = len(ALL_P4)
    pa = [[None]*k_ for _ in range(nP)]
    for pi, p in enumerate(ALL_P4):
        for at, c in enumerate(p): pa[pi][c] = at
    return n, arc_s, pa, ALL_P4

def _sa_score4(sigma, arc_s, pa, n):
    vis = bytearray(n); total = 0
    for c in range(4):
        comps = 0; vis[:] = b'\x00' * n
        for s in range(n):
            if not vis[s]:
                comps += 1; cur = s
                while not vis[cur]: vis[cur] = 1; cur = arc_s[cur][pa[sigma[cur]][c]]
        total += (comps - 1)
    return total

def run_p1_worker(seed, max_iter, result_queue):
    m=4; n, arc_s, pa, ALL_P4 = _build_sa4(m); nP=len(ALL_P4)
    rng = random.Random(seed)
    # Fiber-structured: sigma(i,j,k,l) = tab(i,j,k)
    keys = [(i,j,k) for i in range(m) for j in range(m) for k in range(m)]
    table = {key: rng.randrange(nP) for key in keys}
    def get_sig():
        sig = [0]*n
        for v in range(n):
            i, r1 = divmod(v, m**3); j, r2 = divmod(r1, m**2); k, l = divmod(r2, m)
            sig[v] = table[(i,j,k)]
        return sig
    sigma = get_sig()
    cs = _sa_score4(sigma, arc_s, pa, n); bs = cs; best_tab = dict(table)
    T_init = 100.0; T_min = 0.005
    cool = (T_min/T_init)**(1.0/max_iter)
    T = T_init; stall=0; reheats=0
    for it in range(max_iter):
        if cs == 0: break
        if cs <= 4:
            fixed = False; keys_shuf = list(keys); rng.shuffle(keys_shuf)
            for key in keys_shuf:
                old = table[key]
                for pi in rng.sample(range(nP), nP):
                    if pi == old: continue
                    table[key] = pi; sigma = get_sig(); ns = _sa_score4(sigma, arc_s, pa, n)
                    if ns < cs:
                        cs = ns; fixed = True
                        if cs < bs: bs = cs; best_tab = dict(table)
                        break
                    table[key] = old
                if fixed: break
            if cs == 0: break
            T *= cool; continue
        key = rng.choice(keys); old = table[key]; new = rng.randrange(nP)
        if new == old: T *= cool; continue
        table[key] = new; sigma = get_sig(); ns = _sa_score4(sigma, arc_s, pa, n)
        d = ns - cs
        if d < 0 or rng.random() < math.exp(-d/max(T, 1e-9)):
            cs = ns
            if cs < bs: bs=cs; best_tab=dict(table); stall=0
            else: stall += 1
        else: table[key] = old; stall += 1
        if stall > 50_000:
            T = T_init/(2**reheats); reheats+=1; stall=0
            table = dict(best_tab); sigma = get_sig(); cs = bs
        T *= cool
        if (it+1) % 500_000 == 0:
            result_queue.put(('p1_update', seed, bs, it+1))
    result_queue.put(('p1_final', seed, bs, best_tab if bs==0 else None))

def main():
    result_queue = multiprocessing.Queue()
    processes = []
    # 2 cores for P2, 2 cores for P1
    p2_seeds = [100, 200]
    p1_seeds = [300, 400]
    p2_budget = 100_000_000
    p1_budget = 50_000_000

    for s in p2_seeds:
        p = multiprocessing.Process(target=run_p2_worker, args=(s, p2_budget, result_queue))
        p.start(); processes.append(p)
    for s in p1_seeds:
        p = multiprocessing.Process(target=run_p1_worker, args=(s, p1_budget, result_queue))
        p.start(); processes.append(p)

    best_p2 = 999; best_p1 = 999; start_time = time.time()
    try:
        while any(p.is_alive() for p in processes) and (time.time() - start_time < 11.5 * 3600):
            while not result_queue.empty():
                msg = result_queue.get()
                if msg[0] == 'p2_update':
                    _, s, sc, it = msg
                    if sc < best_p2: best_p2 = sc; print(f"[*] P2 BEST: {sc} (seed={s}, it={it})", flush=True)
                elif msg[0] == 'p1_update':
                    _, s, sc, it = msg
                    if sc < best_p1: best_p1 = sc; print(f"[*] P1 BEST: {sc} (seed={s}, it={it})", flush=True)
                elif msg[0].endswith('_final'):
                    _, s, sc, res = msg
                    if sc == 0: print(f"[!!!] SOLVED {msg[0].split('_')[0].upper()} seed={s}!!! RESULT: {res}", flush=True)
            time.sleep(60)
    except KeyboardInterrupt:
        for p in processes: p.terminate()
    print(f"Kaggle run finished. Best P2: {best_p2}, Best P1: {best_p1}", flush=True)

if __name__ == "__main__":
    main()
