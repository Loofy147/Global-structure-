import time
import random
import math
import copy
from typing import List, Tuple, Dict, Any
from tsp_global_engine import CayleyTSP, EdgeMetrics, Constraints, FiberUniformSolver
from tsp_benchmarks import NearestNeighborSolver, RandomizedSolver, GeneticAlgorithmSolver, AntColonySolver, HeldKarpSolver, TwoOptSolver, FiberUniformSASolver

def generate_problem(m: int, seed: int = 42):
    random.seed(seed)
    gens = [(1, 0), (0, 1), (1, 1)]
    weights = {g: EdgeMetrics(random.uniform(5, 15), random.uniform(1, 5), random.uniform(0.01, 0.2), random.uniform(2, 10), random.uniform(10, 50)) for g in gens}
    return CayleyTSP(m, gens, weights)

def run_standard_benchmark(ms: List[int]):
    # Optimized weights: Time given higher priority (index 1)
    score_weights = [1.0, 10.0, 100.0, 2.0, 1.0]
    constraints = Constraints(max_risk=1.5, max_time=1000.0)

    seeds = [42, 123, 789]
    num_runs = len(seeds)

    solvers = [
        ("FiberUniform", lambda tsp, sw, c: FiberUniformSASolver(tsp, sw, c).solve(iterations=10000) if tsp.m > 10 else FiberUniformSolver(tsp, sw, c).solve()),
        ("NearestNeighbor", lambda tsp, sw, c: NearestNeighborSolver(tsp, sw, c).solve()),
        ("NN+2-Opt", lambda tsp, sw, c: TwoOptSolver(tsp, sw, c).solve()),
        ("Genetic", lambda tsp, sw, c: GeneticAlgorithmSolver(tsp, sw, c).solve(pop_size=50, generations=100)),
        ("AntColony", lambda tsp, sw, c: AntColonySolver(tsp, sw, c).solve(ants=20, iterations=50))
    ]

    print(f"{'Instance':<12} {'Cities':<6} {'Solver':<16} {'Best':>10} {'Avg':>10} {'Worst':>10} {'Gap %':>8} {'Time(ms)':>9} {'Runs':>4}")
    print("-" * 100)

    for m in ms:
        tsp = generate_problem(m)
        n = tsp.n
        instance_name = f"Cayley Z_{m}^2"

        # Determine "Best Known" using HeldKarp for small m
        if m <= 4:
            _, best_known, _, _ = HeldKarpSolver(tsp, score_weights, constraints).solve()
        else:
            best_known = float('inf')
            for _, solve_func in solvers:
                for s in seeds:
                    random.seed(s)
                    _, score, _, _ = solve_func(tsp, score_weights, constraints)
                    if score < best_known: best_known = score

        for name, solve_func in solvers:
            scores = []
            runtimes = []

            for s in seeds:
                random.seed(s)
                t0 = time.perf_counter()
                path, score, metrics, violations = solve_func(tsp, score_weights, constraints)
                dt = (time.perf_counter() - t0) * 1000

                if path:
                    scores.append(score)
                    runtimes.append(dt)

            if not scores:
                print(f"{instance_name:<12} {n:<6} {name:<16} {'DNF':>10}")
                continue

            best = min(scores)
            avg = sum(scores) / len(scores)
            worst = max(scores)
            gap = 100.0 * (best - best_known) / best_known if best_known != 0 else 0.0
            avg_time = sum(runtimes) / len(runtimes)

            print(f"{instance_name:<12} {n:<6} {name:<16} {best:>10.2f} {avg:>10.2f} {worst:>10.2f} {gap:>8.2f}% {avg_time:>9.1f} {num_runs:>4}")
        print("-" * 100)

if __name__ == "__main__":
    run_standard_benchmark([3, 4, 5, 10, 15])
