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

def solve_s3_k2():
    S3, mul = get_s3()
    # Use two reflections as generators. Both are odd permutations.
    b = (1, 0, 2)
    c = (0, 2, 1)
    generators = [b, c]

    perms = [list(p) for p in permutations(range(2))] # [[0, 1], [1, 0]]

    # Try fiber-uniform: sigma constant on cosets of A3
    A3 = [(0,1,2), (1,2,0), (2,0,1)]
    def get_coset(g):
        return 0 if g in A3 else 1

    for choices in product(range(2), repeat=2):
        sigma = {g: perms[choices[get_coset(g)]] for g in S3}
        if verify_decomposition(S3, mul, generators, sigma):
            return sigma, generators

    # If fiber-uniform fails, try full search
    for choices in product(range(2), repeat=6):
        sigma = {S3[i]: perms[choices[i]] for i in range(6)}
        if verify_decomposition(S3, mul, generators, sigma):
            return sigma, generators

    return None, None

if __name__ == "__main__":
    sigma, gens = solve_s3_k2()
    if sigma:
        print(f"SUCCESS: Found k=2 decomposition for S_3!")
        print(f"Generators: {gens}")
        for g, p in sigma.items():
            print(f"  sigma({g}) = {p}")
    else:
        print("FAILED to find k=2 decomposition for S_3")
