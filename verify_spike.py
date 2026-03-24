"""
Geometric Construction for Claude's Cycles (Odd m).
Verifies the 'spike function' hypothesis: for odd m, a valid
3-Hamiltonian decomposition exists where the displacement
function b_c(j) is a spike (v everywhere, v+delta at one point).
"""

import time
import random

def get_sigma(y, m, Sc):
    """Construct sigma(s, j) from binary choices y[s][j]."""
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
            # Arc 0 -> c0, Arc 1 -> c1, Arc 2 -> c2
            p = [0,0,0]
            p[0]=c0; p[1]=c1; p[2]=c2
            # Inverse: sigma[cycle] = arc_type
            inv = [0,0,0]
            for at, color in enumerate(p): inv[color] = at
            sigma[(s, j)] = tuple(inv)
    return sigma

def get_stats(y, m, Sc):
    """Calculate the b_c(j) displacement for each cycle c and column j."""
    def get_path(c, j0):
        path = [0]*m; curr_j = j0
        for s in range(m):
            path[s] = curr_j
            if s in Sc[c]: curr_j = (curr_j + 1) % m
        return path

    A = []; B = []
    for s in range(m):
        c1 = -1
        for c in range(3):
            if s in Sc[c]: c1 = c; break
        others = [c for c in range(3) if c != c1]
        A.append(others[0]); B.append(others[1])

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
                else: # B[s] == c
                    if y[s][js] == 0: count += 1
            Bc.append(count)
        B_stats.append(Bc)
    return B_stats

def verify_hamiltonian(sigma_fiber, m):
    """Rigorous verification of the Hamiltonian property."""
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

def is_spike(vals):
    v = min(vals); spikes = [x for x in vals if x != v]
    return not spikes or len(spikes) == 1

def run_m(m):
    print(f"\n[m={m}] Searching for spike-function construction...")
    start = time.time()
    # Configuration: Cycle 1 uses Arc 1 in most fibers
    r = (1, m-2, 1)
    Sc = [[0], list(range(1, m-1)), [m-1]]

    # We use a randomized approach to find the 'y' configuration
    # that yields the spike b-function.
    for i in range(1000000):
        y = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
        B = get_stats(y, m, Sc)
        if all(is_spike(Bc) for Bc in B):
            if all(sum(Bc) % m != 0 for Bc in B):
                sigma = get_sigma(y, m, Sc)
                if verify_hamiltonian(sigma, m):
                    elapsed = time.time() - start
                    print(f"  SUCCESS! Found spike solution in {elapsed:.2f}s")
                    for c in range(3):
                        print(f"  Cycle {c}: r={r[c]}, b(j)={B[c]} (sum={sum(B[c])})")
                    return True
    print(f"  Failed to find spike solution for m={m}")
    return False

if __name__ == "__main__":
    for m in [3, 5]:
        run_m(m)
