import time
import random
import itertools
from itertools import product
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

# --- CORE ENGINE: SYMMETRIC SYSTEM ON Z_m^2 ---

@dataclass
class EdgeMetrics:
    distance: float
    time: float
    risk: float
    fuel: float
    cost: float
    def to_vec(self): return [self.distance, self.time, self.risk, self.fuel, self.cost]
    @staticmethod
    def sum_metrics(metrics_list):
        if not metrics_list: return EdgeMetrics(0,0,0,0,0)
        return EdgeMetrics(*(sum(getattr(m, f) for m in metrics_list) for f in ['distance','time','risk','fuel','cost']))

class SymmetricCayleyTSP:
    def __init__(self, m: int, generators: List[Tuple[int, int]], weights: Dict[Tuple[int, int], EdgeMetrics]):
        self.m, self.n, self.generators, self.weights, self.k = m, m*m, generators, weights, len(generators)
    def evaluate_sigma(self, sigma: Tuple[int, ...]):
        v, c, m_list = set(), (0, 0), []
        for _ in range(self.n):
            if c in v: return None
            v.add(c); s = (c[0] + c[1]) % self.m; idx = sigma[s]; gen = self.generators[idx]
            m_list.append(self.weights[gen]); c = ((c[0] + gen[0]) % self.m, (c[1] + gen[1]) % self.m)
        if len(v) == self.n and c == (0, 0): return EdgeMetrics.sum_metrics(m_list)
        return None

def find_shortest_symmetric_route(m, seed=42):
    random.seed(seed)
    gens = [(1, 0), (0, 1), (1, 1)]
    # Use real-world-like weights for a challenging search
    weights = {g: EdgeMetrics(random.uniform(5, 15), random.uniform(1, 5), random.uniform(0.01, 0.2), random.uniform(2, 10), random.uniform(10, 50)) for g in gens}
    tsp = SymmetricCayleyTSP(m, gens, weights)

    # Distance is our primary objective for "Shortest Possible Route"
    best_dist, best_sigma, best_metrics = float('inf'), None, None
    t0 = time.perf_counter()

    # Exhaustive search for m <= 11
    # 3^10 = 59049
    for sigma in product(range(len(gens)), repeat=m):
        metrics = tsp.evaluate_sigma(sigma)
        if metrics and metrics.distance < best_dist:
            best_dist, best_sigma, best_metrics = metrics.distance, sigma, metrics

    elapsed = (time.perf_counter() - t0) * 1000
    return best_sigma, best_dist, best_metrics, elapsed

if __name__ == "__main__":
    m = 12
    print(f"SEARCHING SHORTEST SYMMETRIC ROUTE (m={m})")
    sigma, dist, metrics, elapsed = find_shortest_symmetric_route(m)
    if sigma:
        print(f"  Shortest Distance: {dist:.2f}")
        print(f"  Optimal Sigma: {sigma}")
        print(f"  Total Metrics: {metrics}")
        print(f"  Time: {elapsed:.1f}ms")
        with open("tsp_optimal_solution_m10.txt", "w") as f:
            f.write(f"m={m}\nDistance={dist:.2f}\nSigma={sigma}\nMetrics={metrics}\n")
    else:
        print("  No symmetric route found.")
