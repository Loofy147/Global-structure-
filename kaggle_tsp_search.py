import time
import random
from typing import List, Tuple, Dict, Any
import math
from itertools import product, combinations

# --- CORE CLASSES ---
class EdgeMetrics:
    def __init__(self, distance, time, risk, fuel, cost):
        self.distance = distance
        self.time = time
        self.risk = risk
        self.fuel = fuel
        self.cost = cost
    def to_vec(self): return [self.distance, self.time, self.risk, self.fuel, self.cost]
    @staticmethod
    def sum_metrics(metrics_list):
        if not metrics_list: return EdgeMetrics(0,0,0,0,0)
        return EdgeMetrics(
            sum(m.distance for m in metrics_list),
            sum(m.time for m in metrics_list),
            sum(m.risk for m in metrics_list),
            sum(m.fuel for m in metrics_list),
            sum(m.cost for m in metrics_list)
        )

class Constraints:
    def __init__(self, max_risk=float('inf')): self.max_risk = max_risk
    def check(self, metrics): return 1 if metrics.risk > self.max_risk else 0

class CayleyTSP:
    def __init__(self, m, generators, weights):
        self.m, self.n, self.generators, self.weights, self.k = m, m*m, generators, weights, len(generators)
    def get_score(self, metrics, weights_vec, violations):
        base = sum(v * w for v, w in zip(metrics.to_vec(), weights_vec))
        return base + (violations * 100000)
    def sigma_to_path(self, sigma):
        path, curr = [], (0, 0)
        for _ in range(self.n):
            s = (curr[0] + curr[1]) % self.m
            idx = sigma[s]; path.append(idx)
            gen = self.generators[idx]; curr = ((curr[0] + gen[0]) % self.m, (curr[1] + gen[1]) % self.m)
        return path
    def evaluate_path(self, path, constraints=None):
        if len(path) != self.n: return None
        visited, curr, metrics_list = set(), (0, 0), []
        for idx in path:
            if curr in visited: return None
            visited.add(curr); gen = self.generators[idx]; metrics_list.append(self.weights[gen])
            curr = ((curr[0] + gen[0]) % self.m, (curr[1] + gen[1]) % self.m)
        if len(visited) == self.n and curr == (0, 0):
            total = EdgeMetrics.sum_metrics(metrics_list)
            return total, (constraints.check(total) if constraints else 0)
        return None

# --- SOLVERS ---
class FiberUniformSolver:
    def __init__(self, tsp, weights_vec, constraints=None): self.tsp, self.weights_vec, self.constraints = tsp, weights_vec, constraints
    def solve(self):
        best_sigma, best_score, best_metrics, best_viols = None, float('inf'), None, 0
        for sigma in product(range(self.tsp.k), repeat=self.tsp.m):
            res = self.tsp.evaluate_path(self.tsp.sigma_to_path(sigma), self.constraints)
            if res:
                m, v = res; score = self.tsp.get_score(m, self.weights_vec, v)
                if score < best_score: best_score, best_sigma, best_metrics, best_viols = score, sigma, m, v
        return (self.tsp.sigma_to_path(best_sigma), best_score, best_metrics, best_viols) if best_sigma else (None, 0, None, 0)

class NearestNeighborSolver:
    def __init__(self, tsp, weights_vec, constraints=None): self.tsp, self.weights_vec, self.constraints = tsp, weights_vec, constraints
    def solve(self):
        visited, curr, path, metrics_list = set(), (0, 0), [], []
        for _ in range(self.tsp.n):
            visited.add(curr); best_idx, best_ls = -1, float('inf')
            for idx, gen in enumerate(self.tsp.generators):
                nxt = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
                if len(visited) < self.tsp.n:
                    if nxt not in visited:
                        ls = sum(v * w for v, w in zip(self.tsp.weights[gen].to_vec(), self.weights_vec))
                        if ls < best_ls: best_ls, best_idx = ls, idx
                elif nxt == (0, 0): best_idx = idx; break
            if best_idx == -1: return None, 0, None, 0
            path.append(best_idx); metrics_list.append(self.tsp.weights[self.tsp.generators[best_idx]])
            curr = ((curr[0] + self.tsp.generators[best_idx][0]) % self.tsp.m, (curr[1] + self.tsp.generators[best_idx][1]) % self.tsp.m)
        total = EdgeMetrics.sum_metrics(metrics_list); v = self.constraints.check(total) if self.constraints else 0
        return path, self.tsp.get_score(total, self.weights_vec, v), total, v

# --- EXPERIMENT ---
def run():
    print("GLOBAL STRUCTURE TSP BENCHMARK (KAGGLE)")
    ms = [5, 6, 7, 8, 9, 10]
    sw = [1.0, 2.0, 50.0, 1.0, 0.5]
    for m in ms:
        print(f"\n--- Testing m={m} ---")
        random.seed(m)
        gens = [(1, 0), (0, 1), (1, 1)]
        weights = {g: EdgeMetrics(random.uniform(5,15), random.uniform(1,5), random.uniform(0.01,0.2), random.uniform(2,10), random.uniform(10,50)) for g in gens}
        tsp = CayleyTSP(m, gens, weights)
        for name, solver in [("FiberUniform", FiberUniformSolver), ("NearestNeighbor", NearestNeighborSolver)]:
            t0 = time.perf_counter()
            p, s, m_res, v = solver(tsp, sw, Constraints(100.0)).solve()
            dt = (time.perf_counter()-t0)*1000
            if p: print(f"{name:<16} Score: {s:>10.2f}  Time: {dt:>8.1f}ms")
            else: print(f"{name:<16} DNF")

if __name__ == "__main__": run()
