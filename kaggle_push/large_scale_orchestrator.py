import itertools, random, math, time, sys
import multiprocessing
import numpy as np

def score_fast(succ, n, k):
    total = 0
    for c in range(k):
        vis = np.zeros(n, dtype=bool)
        comps = 0
        for s in range(n):
            if vis[s]: continue
            comps += 1; v = s
            while not vis[v]:
                vis[v] = True
                v = succ[v, c]
        total += comps - 1
    return total

def run_sa_worker(m, k, max_iter, strat_type, seed, result_queue):
    random.seed(seed); np.random.seed(seed)
    n = m**k; perms = list(itertools.permutations(range(k))); nP = len(perms)
    strides = np.array([m**(k-1-d) for d in range(k)], dtype=np.int32)
    verts = np.array(list(itertools.product(range(m), repeat=k)), dtype=np.int32)

    if strat_type == 'fiber':
        table_size = m
        v_to_tab = np.sum(verts, axis=1) % m
    elif isinstance(strat_type, int):
        table_size = m**strat_type
        v_to_tab = np.zeros(n, dtype=np.int32)
        for i in range(n):
            tid = 0
            for d in range(strat_type): tid += verts[i, d] * (m**d)
            v_to_tab[i] = tid
    elif strat_type == 'periodic2':
        table_size = 2**k
        v_to_tab = np.zeros(n, dtype=np.int32)
        for i in range(n):
            tid = 0
            for d in range(k): tid += (verts[i, d] % 2) * (2**d)
            v_to_tab[i] = tid
    else:
        table_size = n
        v_to_tab = np.arange(n, dtype=np.int32)

    tab_to_v = [[] for _ in range(table_size)]
    for i in range(n): tab_to_v[v_to_tab[i]].append(i)
    tab_to_v = [np.array(vlist, dtype=np.int32) for vlist in tab_to_v]

    table = np.random.randint(0, nP, size=table_size, dtype=np.int32)
    succ = np.zeros((n, k), dtype=np.int32)
    def update_succ(t_idx):
        p = perms[table[t_idx]]; vl = tab_to_v[t_idx]
        for c in range(k):
            at = p[c]
            nv_coords = verts[vl].copy(); nv_coords[:, at] = (nv_coords[:, at] + 1) % m
            succ[vl, c] = np.sum(nv_coords * strides, axis=1)

    for tid in range(table_size): update_succ(tid)
    cs = score_fast(succ, n, k); bs = cs; best_table = table.copy()
    T = T_init = 1.0; alpha = (0.001/T_init)**(1.0/max_iter)
    stall = 0; reheats = 0; t0 = time.perf_counter()

    for it in range(max_iter):
        if cs == 0: break
        tid = random.randrange(table_size); old_p_idx = table[tid]; table[tid] = random.randrange(nP)
        if table[tid] == old_p_idx: continue
        old_rows = succ[tab_to_v[tid]].copy(); update_succ(tid)
        ns = score_fast(succ, n, k); d = ns - cs
        if d < 0 or (T > 1e-9 and random.random() < math.exp(-d/T)):
            cs = ns
            if cs < bs:
                bs = cs; best_table = table.copy(); stall = 0
                result_queue.put(('update', m, k, bs, strat_type, seed, it))
            else: stall += 1
        else:
            table[tid] = old_p_idx; succ[tab_to_v[tid]] = old_rows; stall += 1
        if stall > 50000:
            reheats = min(reheats + 1, 100); T = T_init / (1.5**reheats); stall = 0
            table = best_table.copy(); cs = bs
            for tid_sync in range(table_size): update_succ(tid_sync)
        T *= alpha
    result_queue.put(('final', m, k, bs, best_table if bs==0 else None))

def main():
    result_queue = multiprocessing.Queue()
    # Configuration for Kaggle (4 cores)
    tasks = [
        (6, 3, 100_000_000, 2, 100),       # P2 seed 100
        (6, 3, 100_000_000, None, 200),    # P2 unrestricted
        (4, 4, 50_000_000, 'periodic2', 300), # P1 periodic
        (4, 4, 50_000_000, 2, 400),        # P1 slice-uniform
    ]
    processes = []
    for m, k, iters, strat, seed in tasks:
        p = multiprocessing.Process(target=run_sa_worker, args=(m, k, iters, strat, seed, result_queue))
        p.start(); processes.append(p)

    start_time = time.time()
    try:
        while any(p.is_alive() for p in processes) and (time.time() - start_time < 11.5 * 3600):
            while not result_queue.empty():
                msg = result_queue.get()
                if msg[0] == 'update':
                    _, m, k, sc, strat, seed, it = msg
                    print(f"[*] NEW BEST: m={m} k={k} score={sc} (strat={strat}, seed={seed}, it={it})", flush=True)
                elif msg[0] == 'final' and msg[3] == 0:
                    print(f"[!!!] SOLVED m={msg[1]} k={msg[2]} RESULT: {msg[4].tolist()}", flush=True)
            time.sleep(30)
    except KeyboardInterrupt:
        for p in processes: p.terminate()
    print("Kaggle run finished.")

if __name__ == "__main__":
    main()
