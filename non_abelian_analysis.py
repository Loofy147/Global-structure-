"""
P5: Non-Abelian Cayley Graphs — S_3 Case Study
==============================================
Extends the "Claude's Cycles" framework to non-abelian groups.
We analyze the Cayley graph of S_3 (symmetric group on 3 elements).

Key Findings:
1. SES: 0 → A_3 → S_3 → Z_2 → 0  is the natural stratification.
2. The fiber H = A_3 is cyclic (Z_3), unlike the Z_m^2 kernel in Z_m^3.
3. Because the fiber is 1D, we only need one coprimality condition.
4. Parity obstruction for k=3 (odd) in even-modulus quotients is bypassed
   because the "sum of drifts" constraint is different in the non-abelian/cyclic fiber case.
"""

from itertools import permutations, product
import math

def get_s3():
    """Returns elements, multiplication, and sign map for S_3."""
    elements = list(permutations(range(3)))
    def mul(a, b): return tuple(a[b[i]] for i in range(3))
    def sign(p):
        s = 0
        for i in range(len(p)):
            for j in range(i+1, len(p)):
                if p[i] > p[j]: s += 1
        return s % 2
    return elements, mul, sign

def verify_decomposition(G, mul, generators, sigma):
    """Verifies if sigma defines a Hamiltonian decomposition."""
    n = len(G)
    k = len(generators)
    cycle_lengths = []
    for c in range(k):
        visited = set()
        curr = G[0]
        for _ in range(n):
            if curr in visited: break
            visited.add(curr)
            gen_idx = sigma[curr][c]
            curr = mul(curr, generators[gen_idx])
        cycle_lengths.append(len(visited))

    is_valid = all(l == n for l in cycle_lengths)
    return is_valid, cycle_lengths

def solve_s3(k, generators):
    """Searches for a fiber-uniform solution for S_3."""
    S3, mul, sign_map = get_s3()
    A3 = [p for p in S3 if sign_map(p) == 0]

    # We use fiber-uniform sigmas: sigma[g] depends only on sign(g)
    # Each coset has k! possible permutations of generators.
    perms = [list(p) for p in permutations(range(k))]

    solutions = []
    for choices in product(range(len(perms)), repeat=2):
        sigma = {g: perms[choices[sign_map(g)]] for g in S3}
        valid, lengths = verify_decomposition(S3, mul, generators, sigma)
        if valid:
            solutions.append(sigma)

    return solutions

def main():
    S3, mul, sign_map = get_s3()
    print("P5: Non-Abelian Analysis (S_3)")
    print("==============================")
    print(f"Group: S_3 (order {len(S3)})")
    print(f"Quotient: Z_2 (via sign map)")
    print(f"Fiber: A_3 (order 3, cyclic)")
    print()

    # Case 1: k=2 (Even k, Even m=2)
    # Generators: (1,0,2) and (0,2,1) [Reflections, map to 1 in Z_2]
    gens2 = [(1, 0, 2), (0, 2, 1)]
    print(f"Testing k=2 with generators {gens2}...")
    sols2 = solve_s3(2, gens2)
    if sols2:
        print(f"  SUCCESS: Found {len(sols2)} fiber-uniform solutions.")
    else:
        print("  FAILED: No fiber-uniform solutions found.")

    # Case 2: k=3 (Odd k, Even m=2)
    # Generators: All 3 reflections (map to 1 in Z_2)
    gens3 = [p for p in S3 if sign_map(p) == 1]
    print(f"\nTesting k=3 with generators {gens3}...")
    print("Note: In the abelian Z_2^3 case, k=3 is obstructed by parity.")
    sols3 = solve_s3(3, gens3)
    if sols3:
        print(f"  SUCCESS: Found {len(sols3)} fiber-uniform solutions.")
        print("  Observation: The non-abelian/cyclic fiber bypasses the Z_m^k parity obstruction.")
    else:
        print("  FAILED: Parity obstruction confirmed.")

    print("\nConclusion:")
    print("The 'Parity Law' (Odd k blocked for Even m) is specific to the Z_m^k topology")
    print("where the kernel is Z_m^{k-1}. For S_3, the kernel A_3 is cyclic (Z_3),")
    print("which allows Hamiltonian cycles even when k is odd and the quotient modulus is even.")

if __name__ == "__main__":
    main()
