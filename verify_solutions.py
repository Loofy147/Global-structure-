import math
from itertools import permutations, product
from solutions import get_z4x6_solution, get_s3_solutions

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
        gens = sol['generators']
        sigma_fibers = sol['sigma']
        k = len(gens)
        n = len(S3)
        for c in range(k):
            vis = set()
            curr = S3[0]
            for _ in range(n):
                if curr in vis: break
                vis.add(curr)
                f = sign(curr)
                gen_idx = sigma_fibers[f'fiber{f}'][c]
                curr = mul(curr, gens[gen_idx])
            if len(vis) != n:
                print(f"S3 {key} color {c} failed.")
                return False
    print("S3 solutions verified!")
    return True

def verify_z4x6():
    sol = get_z4x6_solution()
    m, n = 4, 6
    gens = [(1, 0), (0, 1)]
    k = len(gens)
    order = m * n
    for c in range(k):
        vis = set()
        curr = (0, 0)
        for _ in range(order):
            if curr in vis: break
            vis.add(curr)
            gen_idx = sol[curr][c]
            gen = gens[gen_idx]
            curr = ((curr[0] + gen[0]) % m, (curr[1] + gen[1]) % n)
        if len(vis) != order:
            print(f"Z4xZ6 color {c} failed.")
            return False
    print("Z4xZ6 solution verified!")
    return True

if __name__ == "__main__":
    s3_ok = verify_s3()
    z4x6_ok = verify_z4x6()
    if s3_ok and z4x6_ok:
        print("All additional solutions verified!")
