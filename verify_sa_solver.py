from tsp_global_engine import CayleyTSP, EdgeMetrics, Constraints, FiberUniformSolver
from tsp_benchmarks import FiberUniformSASolver
import random

def test():
    m = 5
    random.seed(m)
    gens = [(1, 0), (0, 1), (1, 1)]
    weights = {g: EdgeMetrics(random.uniform(5, 15), random.uniform(1, 5), random.uniform(0.01, 0.2), random.uniform(2, 10), random.uniform(10, 50)) for g in gens}
    tsp = CayleyTSP(m, gens, weights)
    sw = [1.0, 5.0, 100.0, 2.0, 1.0]
    constraints = Constraints(max_risk=1.5, max_time=1000.0)

    print("Exhaustive FiberUniform:")
    path, score, m_res, v = FiberUniformSolver(tsp, sw, constraints).solve()
    print(f"Score: {score:.1f}, Viol: {v}")

    print("\nSA FiberUniform:")
    path2, score2, m_res2, v2 = FiberUniformSASolver(tsp, sw, constraints).solve(iterations=5000)
    print(f"Score: {score2:.1f}, Viol: {v2}")

if __name__ == "__main__":
    test()
