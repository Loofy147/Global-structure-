import random
import math
from itertools import permutations

def solve_s3_hamiltonian():
    # S_3 elements
    S3 = list(permutations(range(3)))
    def mul(a, b): return tuple(a[b[i]] for i in range(3))
    def inv(a): return tuple(sorted(range(3), key=lambda x: a[x]))
    id3 = (0,1,2)

    # Generators: (12) and (123)
    # (12) is (1,0,2), (123) is (1,2,0)
    g1 = (1,0,2)
    g2 = (1,2,0)
    gens = [g1, g2]
    k = len(gens)
    n = len(S3)

    # Adjacency
    adj = []
    for p in S3:
        adj.append([S3.index(mul(p, g)) for g in gens])

    # SA to find decomposition into 2 Hamiltonian cycles
    # For S_3 (n=6), k=2. We need a mapping sigma: S3 -> Perm(2)
    # Perm(2) has 2 elements: (0,1) and (1,0)
    perms_k = list(permutations(range(k)))
    nP = len(perms_k)

    best_score = 999
    best_sigma = None

    for seed in range(10):
        rng = random.Random(seed)
        sigma = [rng.randrange(nP) for _ in range(n)]

        def get_score(sig):
            total = 0
            for c in range(k):
                vis = [False]*n
                comps = 0
                for s in range(n):
                    if not vis[s]:
                        comps += 1
                        cur = s
                        while not vis[cur]:
                            vis[cur] = True
                            p_idx = sig[cur]
                            gen_idx = perms_k[p_idx][c]
                            cur = adj[cur][gen_idx]
                total += (comps - 1)
            return total

        cs = get_score(sigma)
        if cs < best_score:
            best_score = cs
            best_sigma = list(sigma)
        if cs == 0: break

    if best_score == 0:
        print("S3 Hamiltonian Decomposition Found!")
        sol = []
        for i, s_idx in enumerate(best_sigma):
            sol.append(perms_k[s_idx])
        print(f"Sigma mapping: {sol}")
        return sol
    else:
        print(f"Failed to find S3 decomposition, best score: {best_score}")
        return None

if __name__ == "__main__":
    solve_s3_hamiltonian()
