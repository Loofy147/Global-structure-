import time
import random
from math import gcd

def get_sigma(y, m, Sc):
    A = []; B = []
    for s in range(m):
        c1 = -1
        for c in range(3):
            if s in Sc[c]: c1 = c; break
        others = [c for c in range(3) if c != c1]
        A.append(others[0]); B.append(others[1])
    sigma = {}
    for s in range(m):
        c1 = -1
        for c in range(3):
            if s in Sc[c]: c1 = c; break
        for j in range(m):
            y_val = y[s][j]
            c0 = A[s] if y_val == 1 else B[s]
            c2 = [c for c in range(3) if c not in [c0, c1]][0]
            p = [0,0,0]; p[0]=c0; p[1]=c1; p[2]=c2
            inv = [0,0,0]
            for at, color in enumerate(p): inv[color] = at
            sigma[(s, j)] = tuple(inv)
    return sigma

def get_stats(y, m, Sc):
    def get_path(c, j0):
        path = [0]*m; curr_j = j0
        for s in range(m):
            path[s] = curr_j
            if s in Sc[c]: curr_j = (curr_j + 1) % m
        return path
    A = []; B_choices = []
    for s in range(m):
        c1 = -1
        for c in range(3):
            if s in Sc[c]: c1 = c; break
        others = [c for c in range(3) if c != c1]
        A.append(others[0]); B_choices.append(others[1])
    B_stats = []
    for c in range(3):
        Bc = []
        for j0 in range(m):
            path = get_path(c, j0); count = 0
            for s in range(m):
                if s in Sc[c]: continue
                js = path[s]
                if A[s] == c:
                    if y[s][js] == 1: count += 1
                else: # B_choices[s] == c
                    if y[s][js] == 0: count += 1
            Bc.append(count)
        B_stats.append(Bc)
    return B_stats

def verify_hamiltonian(sigma_fiber, m):
    n = m**3
    ARC_SHIFTS = ((1,0,0),(0,1,0),(0,0,1))
    for c in range(3):
        curr = (0, 0, 0); visited = set()
        for _ in range(n):
            if curr in visited: break
            visited.add(curr)
            s = (curr[0] + curr[1] + curr[2]) % m
            at = sigma_fiber[(s, curr[1])][c]
            curr = tuple((curr[d] + ARC_SHIFTS[at][d]) % m for d in range(3))
        if len(visited) != n: return False
    return True

def score_y(y, m, Sc):
    B = get_stats(y, m, Sc)
    s = 0
    for Bc in B:
        vmin = min(Bc)
        # We want EXACTLY one spike or zero (flat)
        spikes = [x for x in Bc if x != vmin]
        if len(spikes) > 1: s += (len(spikes) - 1) * 3
        # Coprimality is strictly required
        if gcd(sum(Bc), m) != 1: s += 10
    return s

def run_m(m, max_iter=1000000):
    print(f"\n[m={m}] Searching for spike-function construction...")
    Sc = [[0], list(range(1, m-1)), [m-1]]
    r = (1, m-2, 1)

    t0 = time.time()
    for rest in range(10):
        y = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
        curr_s = score_y(y, m, Sc); T = 1.0
        for it in range(max_iter):
            if curr_s == 0:
                B = get_stats(y, m, Sc)
                sigma = get_sigma(y, m, Sc)
                if verify_hamiltonian(sigma, m):
                    print(f"  SUCCESS! rest={rest} it={it} time={time.time()-t0:.2f}s")
                    for c in range(3):
                        print(f"  Cycle {c}: r={r[c]}, b(j)={B[c]} (sum={sum(B[c])})")
                    return True
                else: curr_s = 20

            s_idx, j_idx = random.randrange(m), random.randrange(m)
            y[s_idx][j_idx] = 1 - y[s_idx][j_idx]
            new_s = score_y(y, m, Sc)

            import math
            if new_s <= curr_s or random.random() < math.exp((curr_s - new_s) / T):
                curr_s = new_s
            else:
                y[s_idx][j_idx] = 1 - y[s_idx][j_idx]

            if it % 1000 == 0: T *= 0.98
        print(f"  Restart {rest} best={curr_s}")
    return False

if __name__ == "__main__":
    for m in [3, 5, 7]:
        run_m(m)
