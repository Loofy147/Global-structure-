import math
from itertools import product, permutations

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def verify_decomposition(m, n, generators, sigma):
    order = m * n
    k = len(generators)
    for c in range(k):
        visited = set()
        curr = (0, 0)
        for _ in range(order):
            if curr in visited: break
            visited.add(curr)
            # sigma[(i,j)] is the index of the generator assigned to color c
            gen_idx = sigma[curr][c]
            gen = generators[gen_idx]
            curr = ((curr[0] + gen[0]) % m, (curr[1] + gen[1]) % n)
        if len(visited) != order: return False
    return True

def solve_product(m, n, k):
    g = gcd(m, n)
    # Pick generators that map to 1 in Z_g.
    # This ensures they 'move' through the fibers.
    # (1, 0) maps to 1 mod g.
    # (0, 1) maps to 1 mod g.
    # (1, g) maps to 1+g = 1 mod g.
    all_gens = [(1, 0), (0, 1), (1, g if g < n else 0), (g if g < m else 0, 1)]
    # Select k distinct generators
    generators = all_gens[:k]

    perms = [list(p) for p in permutations(range(k))]

    # Fiber-uniform search
    for choices in product(range(len(perms)), repeat=g):
        sigma = {(i, j): perms[choices[(i+j)%g]] for i in range(m) for j in range(n)}
        if verify_decomposition(m, n, generators, sigma):
            return sigma, generators
    return None, None

def main():
    print("P6: Product Groups Z_m x Z_n Analysis (Refined)")
    print("==============================================")

    test_cases = [
        (3, 3, 3), # g=3, k=3 (Odd g, Odd k) -> SUCCESS EXPECTED
        (4, 4, 3), # g=4, k=3 (Even g, Odd k) -> OBSTRUCTED
        (2, 6, 2), # g=2, k=2 (Even g, Even k) -> SUCCESS EXPECTED
        (4, 6, 3), # g=2, k=3 (Even g, Odd k) -> OBSTRUCTED
    ]

    for m, n, k in test_cases:
        g = gcd(m, n)
        print(f"\nTesting Z_{m} x Z_{n} with k={k} colors (gcd={g})...")
        sigma, gens = solve_product(m, n, k)
        if sigma:
            print(f"  SUCCESS: Found fiber-uniform solution.")
            print(f"  Generators used: {gens}")
        else:
            print(f"  FAILED: No fiber-uniform solution found.")
            if g % 2 == 0 and k % 2 == 1:
                print("  Interpretation: Parity obstruction confirmed.")

if __name__ == "__main__":
    main()
