import time
import random
from typing import List, Tuple, Dict, Any
from tsp_global_engine import CayleyTSP, EdgeMetrics, Constraints, FiberUniformSolver
from tsp_benchmarks import NearestNeighborSolver, RandomizedSolver, GeneticAlgorithmSolver, AntColonySolver, HeldKarpSolver
from tsp_metrics import calculate_stability, calculate_diversity

def generate_problem(m: int, seed: int = 42):
    random.seed(seed)
    # Generators for Z_m x Z_m
    gens = [(1, 0), (0, 1), (1, 1)]
    weights = {}
    for g in gens:
        weights[g] = EdgeMetrics(
            distance=random.uniform(5, 15),
            time=random.uniform(1, 5),
            risk=random.uniform(0.01, 0.2),
            fuel=random.uniform(2, 10),
            cost=random.uniform(10, 50)
        )
    return CayleyTSP(m, gens, weights)

def run_experiment(ms: List[int]):
    # Weights for multi-objective score: [distance, time, risk, fuel, cost]
    score_weights = [1.0, 2.0, 50.0, 1.0, 0.5]
    constraints = Constraints(max_risk=100.0)

    solvers = [
        ("FiberUniform", FiberUniformSolver),
        ("NearestNeighbor", NearestNeighborSolver),
        ("Randomized", RandomizedSolver),
        ("Genetic", GeneticAlgorithmSolver),
        ("AntColony", AntColonySolver),
        ("HeldKarp", HeldKarpSolver)
    ]

    header = f"{'m':<2} {'Solver':<16} {'Score':>10} {'Dist':>8} {'Time':>6} {'Risk':>6} {'Fuel':>6} {'Cost':>6} {'Viol':>4} {'Stab':>6} {'Div':>6} {'Time(ms)':>8}"
    print(header)
    print("-" * len(header))

    for m in ms:
        tsp = generate_problem(m)
        ref_path = None

        # Determine reference for diversity (HeldKarp if m=3, else FiberUniform)
        # Actually FiberUniform is our baseline.

        for name, solver_class in solvers:
            if m > 4 and name == "HeldKarp": continue
            if m > 3 and name == "FiberUniform":
                # FiberUniform search space is k^m. 3^m. 3^5=243, 3^6=729. OK.
                pass

            t0 = time.perf_counter()
            try:
                # Limit iterations for metaheuristics to keep it fast
                if solver_class == RandomizedSolver:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve(iterations=500)
                elif solver_class == GeneticAlgorithmSolver:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve(pop_size=30, generations=50)
                elif solver_class == AntColonySolver:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve(ants=15, iterations=30)
                else:
                    path, score, metrics, violations = solver_class(tsp, score_weights, constraints).solve()
            except Exception as e:
                print(f"{m:<2} {name:<16} ERROR: {e}")
                continue

            elapsed = (time.perf_counter() - t0) * 1000

            if not path:
                print(f"{m:<2} {name:<16} {'DNF':>10}")
                continue

            if name == "FiberUniform" or (name == "HeldKarp" and ref_path is None):
                ref_path = path
                div = 0.0
            else:
                div = calculate_diversity(ref_path, path) if ref_path else 0.0

            stab = calculate_stability(tsp, solver_class, score_weights, constraints, iterations=2) if m <= 4 else 0.0

            print(f"{m:<2} {name:<16} {score:>10.2f} {metrics.distance:>8.1f} {metrics.time:>6.1f} {metrics.risk:>6.2f} {metrics.fuel:>6.1f} {metrics.cost:>6.1f} {violations:>4} {stab:>6.2f} {div:>6.2f} {elapsed:>8.1f}")
        print("-" * len(header))

if __name__ == "__main__":
    run_experiment([3, 4, 5, 6])
