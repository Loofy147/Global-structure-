import itertools, numpy as np
from math import gcd

def score_np(succ, n, k):
    total = 0
    for c in range(k):
        visited = np.zeros(n, dtype=bool)
        comps = 0
        for start in range(n):
            if visited[start]: continue
            comps += 1; v = start
            while not visited[v]:
                visited[v] = True
                v = succ[v, c]
        total += comps - 1
    return total

def spike_rule_v3(m):
    n = m**3
    verts = list(itertools.product(range(m), repeat=3))
    perm_arr = np.zeros((n, 3), dtype=np.int32)
    for idx, (i, j, l) in enumerate(verts):
        X = 1 if (l >= m-2 and j == m-1) else 0
        base_shift = (j + l) % 3
        p = [(c + base_shift) % 3 for c in range(3)]
        if X == 1:
            p = [(p[0]+1) % 3, (p[1]+1) % 3, (p[2]+1) % 3]
        perm_arr[idx] = p
    return perm_arr, verts

def test_spike(m):
    perm_arr, verts = spike_rule_v3(m)
    n = m**3; k = 3
    strides = np.array([m**(k-1-d) for d in range(k)], dtype=np.int32)
    succ = np.zeros((n, k), dtype=np.int32)
    for idx, v in enumerate(verts):
        for c in range(k):
            dim = perm_arr[idx, c]
            nv = list(v); nv[dim] = (nv[dim] + 1) % m
            succ[idx, c] = sum(nv[d] * strides[d] for d in range(k))
    return score_np(succ, n, k)

if __name__ == "__main__":
    for m in [3, 5]:
        s = test_spike(m)
        print(f"m={m} spike_rule_v3 score={s}")
