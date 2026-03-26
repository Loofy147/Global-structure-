import math
from itertools import product, permutations

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def get_hamiltonian_cost(m, generators, weights, sigma_table):
    """
    Computes cost of a Hamiltonian cycle defined by fiber-uniform sigma.
    sigma_table[s] maps fiber s to generator index.
    """
    n = m * m
    visited = set()
    curr = (0, 0)
    total_cost = 0
    for _ in range(n):
        if curr in visited: break
        visited.add(curr)
        s = (curr[0] + curr[1]) % m
        gen_idx = sigma_table[s]
        gen = generators[gen_idx]
        total_cost += weights[gen_idx]
        curr = ((curr[0] + gen[0]) % m, (curr[1] + gen[1]) % n)

    if len(visited) == n:
        return total_cost
    return None

def solve_tsp_fiber_uniform(m, generators, weights):
    """
    Exhaustively searches for the lowest-cost fiber-uniform Hamiltonian cycle.
    """
    k = len(generators)
    best_cost = float('inf')
    best_sigma = None

    # Space: k^m
    for sigma in product(range(k), repeat=m):
        cost = get_hamiltonian_cost(m, generators, weights, sigma)
        if cost is not None and cost < best_cost:
            best_cost = cost
            best_sigma = sigma

    return best_sigma, best_cost

def main():
    print("P7: TSP on Stratified Cayley Graphs")
    print("====================================")
    m = 5
    generators = [(1, 0), (0, 1), (1, 1)] # Arc moves
    weights = [10, 15, 12] # Cost of each arc move

    print(f"Graph: Z_{m} x Z_{m}")
    print(f"Generators: {generators}")
    print(f"Weights: {weights}")

    sigma, cost = solve_tsp_fiber_uniform(m, generators, weights)

    if sigma:
        print(f"\nOptimal Fiber-Uniform Hamiltonian Cycle Found!")
        print(f"  Sigma (fiber -> gen_idx): {sigma}")
        print(f"  Minimum Cost: {cost}")

        # Verify
        n = m*m
        dist = [sigma.count(i) for i in range(len(generators))]
        # Note: Each fiber is visited m times. Total m^2 steps.
        # sigma[s] is used for all (i,j) in fiber s.
        # But wait, the path moves through fibers.
        # In one full cycle, how many times is each generator used?
        # If gen = (1,0) it maps s -> s+1.
        # If gen = (0,1) it maps s -> s+1.
        # If gen = (1,1) it maps s -> s+2.

        actual_uses = [0] * len(generators)
        curr_s = 0
        for _ in range(n):
            idx = sigma[curr_s]
            actual_uses[idx] += 1
            step = sum(generators[idx]) % m
            curr_s = (curr_s + step) % m
        print(f"  Generator usage distribution: {actual_uses}")
        calc_cost = sum(actual_uses[i] * weights[i] for i in range(len(weights)))
        print(f"  Calculated cost: {calc_cost}")
    else:
        print("\nNo fiber-uniform Hamiltonian cycle exists for these generators.")

if __name__ == "__main__":
    main()
