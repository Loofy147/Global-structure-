import random
import math
from tsp_global_engine import CayleyTSP, EdgeMetrics, Constraints
from tsp_benchmarks import FiberUniformSASolver

def run_sensitivity():
    print("TSP MULTI-OBJECTIVE SENSITIVITY ANALYSIS (m=10)")
    print("===============================================")

    m = 10
    random.seed(m)
    gens = [(1, 0), (0, 1), (1, 1)]
    # Randomly weighted instance
    weights = {g: EdgeMetrics(random.uniform(5, 15), random.uniform(1, 5), random.uniform(0.01, 0.2), random.uniform(2, 10), random.uniform(10, 50)) for g in gens}
    tsp = CayleyTSP(m, gens, weights)
    constraints = Constraints(max_risk=10.0, max_time=10000.0)

    # Pareto frontier search: Vary Time weight vs Risk weight
    print(f"{'Time Wt':>8} {'Risk Wt':>8} {'Time Metric':>12} {'Risk Metric':>12} {'Score':>12}")
    print("-" * 55)

    for t_wt in [0.1, 1.0, 10.0, 100.0]:
        for r_wt in [0.1, 1.0, 10.0, 100.0]:
            sw = [1.0, t_wt, r_wt, 1.0, 1.0]
            solver = FiberUniformSASolver(tsp, sw, constraints)
            path, score, m_res, v = solver.solve(iterations=5000)

            if path:
                print(f"{t_wt:>8.1f} {r_wt:>8.1f} {m_res.time:>12.2f} {m_res.risk:>12.2f} {score:>12.2f}")
            else:
                print(f"{t_wt:>8.1f} {r_wt:>8.1f} {'DNF':>12} {'DNF':>12} {'DNF':>12}")

if __name__ == "__main__":
    run_sensitivity()
