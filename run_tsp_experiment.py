import time
import random
from typing import List, Tuple, Dict, Any
from tsp_global_engine import CayleyTSP, EdgeMetrics, Constraints, FiberUniformSolver
from tsp_benchmarks import NearestNeighborSolver, RandomizedSolver, GeneticAlgorithmSolver, AntColonySolver, HeldKarpSolver
from tsp_metrics import calculate_stability, calculate_diversity

def generate_problem(m: int, seed: int = 42):
    random.seed(seed)
    gens = [(1, 0), (0, 1), (1, 1)]
    weights = {g: EdgeMetrics(random.uniform(5, 15), random.uniform(1, 5), random.uniform(0.01, 0.2), random.uniform(2, 10), random.uniform(10, 50)) for g in gens}
    return CayleyTSP(m, gens, weights)

def run_experiment(ms: List[int]):
    # Weights for multi-objective score: [distance, time, risk, fuel, cost]
    score_weights = [1.0, 5.0, 100.0, 2.0, 1.0]
    constraints = Constraints(max_risk=1.5, max_time=1000.0)

    solvers = [
        ("FiberUniform", FiberUniformSolver),
        ("NearestNeighbor", NearestNeighborSolver),
        ("Randomized", RandomizedSolver),
        ("Genetic", GeneticAlgorithmSolver),
        ("AntColony", AntColonySolver),
        ("HeldKarp", HeldKarpSolver)
    ]

    header = f"{'m':<2} {'Solver':<16} {'Score':>10} {'Dist':>7} {'Time':>6} {'Risk':>5} {'Fuel':>5} {'Cost':>6} {'Viol':>4} {'Stab':>5} {'Div':>5} {'Time(ms)':>9}"
    print(header)
    print("-" * len(header))

    for m in ms:
        tsp = generate_problem(m)
        ref_path = None
        for name, solver_class in solvers:
            if m > 4 and name == "HeldKarp": continue

            t0 = time.perf_counter()
            try:
                if solver_class == RandomizedSolver:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve(iterations=1000)
                elif solver_class == GeneticAlgorithmSolver:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve(pop_size=50, generations=100)
                elif solver_class == AntColonySolver:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve(ants=20, iterations=50)
                else:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve()
            except Exception as e:
                print(f"{m:<2} {name:<16} ERROR: {e}")
                continue

            elapsed = (time.perf_counter() - t0) * 1000
            if not path:
                print(f"{m:<2} {name:<16} {'DNF':>10}")
                continue

            if name == "FiberUniform": ref_path = path; div = 0.0
            else: div = calculate_diversity(ref_path, path) if ref_path else 0.0
            stab = calculate_stability(tsp, solver_class, score_weights, constraints, iterations=3) if m <= 4 else 0.0

            print(f"{m:<2} {name:<16} {score:>10.1f} {metrics.distance:>7.1f} {metrics.time:>6.1f} {metrics.risk:>5.2f} {metrics.fuel:>5.1f} {metrics.cost:>6.1f} {violations:>4} {stab:>5.2f} {div:>5.2f} {elapsed:>9.1f}")
        print("-" * len(header))

if __name__ == "__main__":
    run_experiment([3, 4, 5])
