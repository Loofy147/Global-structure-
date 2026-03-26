import random
from itertools import permutations, product

def get_s3():
    elements = list(permutations(range(3)))
    def mul(a, b): return tuple(a[b[i]] for i in range(3))
    return elements, mul

def verify_decomposition(G, mul, generators, sigma):
    n = len(G)
    k = len(generators)
    for c in range(k):
        visited = set()
        curr = G[0]
        for _ in range(n):
            if curr in visited: break
            visited.add(curr)
            gen_idx = sigma[curr][c]
            curr = mul(curr, generators[gen_idx])
        if len(visited) != n: return False
    return True

def sign(p):
    s = 1
    for i in range(len(p)):
        for j in range(i+1, len(p)):
            if p[i] > p[j]: s *= -1
    return s

def solve_s3_k3_fiber_uniform():
    S3, mul = get_s3()
    gens = [p for p in S3 if sign(p) == -1]
    A3 = [p for p in S3 if sign(p) == 1]

    perms = [list(p) for p in permutations(range(3))] # 6 perms

    # Fiber-uniform: sigma[g] depends only on coset
    # Cosets are A3 and S3\A3. So 2 choices.
    # Total space 6^2 = 36.
    for choices in product(range(6), repeat=2):
        sigma = {g: perms[choices[0 if g in A3 else 1]] for g in S3}
        if verify_decomposition(S3, mul, gens, sigma):
            return sigma, gens

    return None, None

if __name__ == "__main__":
    sigma, gens = solve_s3_k3_fiber_uniform()
    if sigma:
        print("SUCCESS: Found fiber-uniform k=3 decomposition for S_3!")
    else:
        print("FAILED: No fiber-uniform k=3 decomposition found for S_3. Parity obstruction confirmed for fiber-uniform case.")
