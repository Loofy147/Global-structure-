import random
import copy
from typing import List, Tuple, Dict, Any
from tsp_global_engine import CayleyTSP, EdgeMetrics, Constraints

def calculate_stability(tsp: CayleyTSP, solver_class, weights_vector: List[float], constraints: Constraints = None, iterations: int = 5) -> float:
    """
    Measures stability by adding noise to weights and seeing how much the solution changes.
    Returns the average Hamming distance between the original path and the noisy ones.
    """
    orig_path, _, _, _ = solver_class(tsp, weights_vector, constraints).solve()
    if not orig_path: return 0.0

    total_dist = 0
    for _ in range(iterations):
        noisy_weights = {g: copy.deepcopy(m) for g, m in tsp.weights.items()}
        for g in noisy_weights:
            # Add up to 10% noise to each metric
            noisy_weights[g].distance *= (1 + random.uniform(-0.1, 0.1))
            noisy_weights[g].time *= (1 + random.uniform(-0.1, 0.1))
            noisy_weights[g].risk *= (1 + random.uniform(-0.1, 0.1))
            noisy_weights[g].fuel *= (1 + random.uniform(-0.1, 0.1))
            noisy_weights[g].cost *= (1 + random.uniform(-0.1, 0.1))

        noisy_tsp = CayleyTSP(tsp.m, tsp.generators, noisy_weights)
        noisy_path, _, _, _ = solver_class(noisy_tsp, weights_vector, constraints).solve()

        if noisy_path:
            # Hamming distance
            dist = sum(1 for a, b in zip(orig_path, noisy_path) if a != b)
            total_dist += dist / len(orig_path)
        else:
            total_dist += 1.0 # Max instability

    return total_dist / iterations

def calculate_diversity(path1: List[int], path2: List[int]) -> float:
    """
    Measures diversity as the Hamming distance between two paths.
    """
    if not path1 or not path2: return 1.0
    if len(path1) != len(path2): return 1.0
    return sum(1 for a, b in zip(path1, path2) if a != b) / len(path1)

if __name__ == "__main__":
    from tsp_benchmarks import NearestNeighborSolver, RandomizedSolver
    m = 3
    gens = [(1, 0), (0, 1), (1, 1)]
    weights = {
        (1, 0): EdgeMetrics(10, 2, 0.1, 5, 10),
        (0, 1): EdgeMetrics(15, 3, 0.05, 7, 15),
        (1, 1): EdgeMetrics(12, 2.5, 0.2, 6, 12)
    }
    tsp = CayleyTSP(m, gens, weights)
    sw = [1., 1., 10., 1., 1.]

    nn_path, _, _, _ = NearestNeighborSolver(tsp, sw).solve()
    rnd_path, _, _, _ = RandomizedSolver(tsp, sw).solve()

    stab = calculate_stability(tsp, NearestNeighborSolver, sw)
    div = calculate_diversity(nn_path, rnd_path)

    print(f"Metrics test (m=3):")
    print(f"  NN Stability: {stab:.2f}")
    print(f"  Diversity(NN, RND): {div:.2f}")
