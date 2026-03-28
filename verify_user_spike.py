from math import gcd

identity = (0, 1, 2); swap12 = (0, 2, 1); swap01 = (1, 0, 2)
def swap02(p): return (p[2], p[1], p[0])

def build_table(m):
    P = [identity] * (m - 2) + [swap12, swap01]
    table = []
    for s in range(m):
        row = [None]*m
        for j in range(m):
            if j == 0 and s != m - 2:
                row[j] = swap02(P[s])
            else:
                row[j] = P[s]
        table.append(row)
    return table

def verify_sigma(sigma_table, m):
    n = m**3; k = 3
    for c in range(k):
        vis = set()
        curr = (0, 0, 0)
        for _ in range(n):
            if curr in vis: break
            vis.add(curr)
            i, j, k_ = curr
            s = (i + j + k_) % m
            p = sigma_table[s][j]
            ni, nj, nk = i, j, k_
            if p[c] == 0: ni = (ni + 1) % m
            elif p[c] == 1: nj = (nj + 1) % m
            else: nk = (nk + 1) % m
            curr = (ni, nj, nk)
        if len(vis) != n: return False, c, len(vis)
    return True, None, n

if __name__ == "__main__":
    for m in range(3, 11, 2):
        tab = build_table(m)
        ok, col, count = verify_sigma(tab, m)
        print(f"m={m}: {ok} (Color {col} count {count})")
