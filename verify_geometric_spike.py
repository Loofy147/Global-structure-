import math
from itertools import permutations

def verify_sigma_v2(sigma_table, m):
    n = m**3; k = 3
    for c in range(k):
        vis = bytearray(n)
        curr = (0, 0, 0); count = 0
        while True:
            idx = curr[0]*m*m + curr[1]*m + curr[2]
            if vis[idx]: break
            vis[idx] = 1; count += 1
            i, j, k_ = curr
            s = (i + j + k_) % m
            p = sigma_table[s][j]
            gen_idx = p[c]
            ni, nj, nk = i, j, k_
            if gen_idx == 0: ni = (ni + 1) % m
            elif gen_idx == 1: nj = (nj + 1) % m
            else: nk = (nk + 1) % m
            curr = (ni, nj, nk)
        if count != n: return False, c, count
    return True, None, n

def build_table(m):
    identity = (0, 1, 2); swap12 = (0, 2, 1); swap01 = (1, 0, 2)
    def swap02(p): return (p[2], p[1], p[0])
    P = [identity] * (m - 2) + [swap12, swap01]
    table = []
    for s in range(m):
        row = {}
        for j in range(m):
            if j == 0 and s != m - 2: row[j] = swap02(P[s])
            else: row[j] = P[s]
        table.append(row)
    return table

if __name__ == "__main__":
    for m in range(3, 11, 2):
        tab = build_table(m)
        ok, col, count = verify_sigma_v2(tab, m)
        print(f"m={m}: {ok} (Color {col} count {count})")
