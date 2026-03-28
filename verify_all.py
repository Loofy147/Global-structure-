import math
from itertools import permutations, product
from solutions import get_z4x6_solution, get_s3_solutions, get_z2k4_solution

def verify_s3():
    sols = get_s3_solutions()
    S3 = list(permutations(range(3)))
    def mul(a, b): return tuple(a[b[i]] for i in range(3))
    def sign(p):
        s = 0
        for i in range(len(p)):
            for j in range(i+1, len(p)):
                if p[i] > p[j]: s += 1
        return s % 2
    for key, sol in sols.items():
        gens = sol['generators']; sigma_fibers = sol['sigma']
        k = len(gens); n = len(S3)
        for c in range(k):
            vis = set(); curr = S3[0]
            for _ in range(n):
                if curr in vis: break
                vis.add(curr)
                f = sign(curr); p = sigma_fibers[f'fiber{f}']; gen_idx = p[c]
                curr = mul(curr, gens[gen_idx])
            if len(vis) != n:
                print(f"S3 {key} color {c} FAILED. Length: {len(vis)}")
                return False
    print("S3 solutions verified!")
    return True

def verify_z4x6():
    sol = get_z4x6_solution(); m, n = 4, 6
    gens = [(1, 0), (0, 1)]; k = len(gens); order = m * n
    for c in range(k):
        vis = set(); curr = (0, 0)
        for _ in range(order):
            if curr in vis: break
            vis.add(curr)
            p = sol[curr]; gen_idx = p[c]; gen = gens[gen_idx]
            curr = ((curr[0] + gen[0]) % m, (curr[1] + gen[1]) % n)
        if len(vis) != order:
            print(f"Z4xZ6 color {c} FAILED. Length: {len(vis)}")
            return False
    print("Z4xZ6 solution verified!")
    return True

def verify_z2k4():
    m, k, n = 2, 4, 16
    sigma = get_z2k4_solution()
    all_p = list(permutations(range(k)))
    def get_adj(v, c):
        coords = [ (v >> i) & 1 for i in range(4) ]
        coords[c] ^= 1
        return sum(coords[i] << i for i in range(4))
    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]
    for c in range(k):
        vis = set(); curr = 0
        for _ in range(n):
            if curr in vis: break
            vis.add(curr)
            p_idx = sigma[curr]; p = all_p[p_idx]; gen_idx = p[c]
            curr = adj[curr][gen_idx]
        if len(vis) != n:
            print(f"Z2k4 color {c} FAILED. Length: {len(vis)}")
            return False
    print("Z2k4 solution verified!")
    return True

if __name__ == "__main__":
    s3 = verify_s3()
    z4x6 = verify_z4x6()
    z2k4 = verify_z2k4()
    if s3 and z4x6 and z2k4:
        print("\nALL NEW SOLUTIONS VERIFIED!")
    else:
        print("\nSOME SOLUTIONS FAILED!")
