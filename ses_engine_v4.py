import itertools, random, math, time, sys
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

def run_basin_escape_sa(m, k, max_iter=1000000, T_start=1.0, T_end=0.001, seed=42, strat_type=None):
    random.seed(seed); np.random.seed(seed)
    n = m**k; perms = list(itertools.permutations(range(k))); nP = len(perms)
    strides = np.array([m**(k-1-d) for d in range(k)], dtype=np.int32)
    verts = np.array(list(itertools.product(range(m), repeat=k)), dtype=np.int32)

    if strat_type == 'periodic2':
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
        p = perms[table[t_idx]]
        vl = tab_to_v[t_idx]
        for c in range(k):
            at = p[c]
            nv_coords = verts[vl].copy()
            nv_coords[:, at] = (nv_coords[:, at] + 1) % m
            succ[vl, c] = np.sum(nv_coords * strides, axis=1)

    for tid in range(table_size): update_succ(tid)
    cs = score_fast(succ, n, k); bs = cs; best_table = table.copy()
    T = T_init = T_start; alpha = (T_end/T_start)**(1.0/max_iter)
    stall = 0; reheats = 0; t0 = time.perf_counter()

    for it in range(max_iter):
        if cs == 0: break
        tid = random.randrange(table_size); old_p_idx = table[tid]
        table[tid] = random.randrange(nP)
        if table[tid] == old_p_idx: continue
        old_rows = succ[tab_to_v[tid]].copy(); update_succ(tid)
        ns = score_fast(succ, n, k); d = ns - cs
        if d < 0 or (T > 1e-9 and random.random() < math.exp(-d/T)):
            cs = ns
            if cs < bs:
                bs = cs; best_table = table.copy(); stall = 0
                if bs < 74:
                    sys.stdout.write(f"\n  [it {it}] NEW RECORD FOR P1-k4: {bs} (seed {seed})\n")
                    sys.stdout.flush()
            else: stall += 1
        else:
            table[tid] = old_p_idx; succ[tab_to_v[tid]] = old_rows; stall += 1
        if stall > 50000:
            reheats += 1; T = T_init / (1.5**reheats); stall = 0
            table = best_table.copy(); cs = bs
            for tid_sync in range(table_size): update_succ(tid_sync)
        T *= alpha
    return best_table, bs, time.perf_counter()-t0

if __name__ == "__main__":
    for s in range(50):
        best_tab, score, elapsed = run_basin_escape_sa(4, 4, max_iter=100000, strat_type='periodic2', seed=s)
        if score < 74: print(f"FINAL Seed {s} Score: {score}")
