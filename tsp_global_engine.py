import math
import time
from itertools import product
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

@dataclass
class EdgeMetrics:
    distance: float
    time: float
    risk: float
    fuel: float
    cost: float

    def to_vec(self):
        return [self.distance, self.time, self.risk, self.fuel, self.cost]

    @staticmethod
    def sum_metrics(metrics_list: List['EdgeMetrics']) -> 'EdgeMetrics':
        if not metrics_list:
            return EdgeMetrics(0, 0, 0, 0, 0)
        return EdgeMetrics(
            distance=sum(m.distance for m in metrics_list),
            time=sum(m.time for m in metrics_list),
            risk=sum(m.risk for m in metrics_list),
            fuel=sum(m.fuel for m in metrics_list),
            cost=sum(m.cost for m in metrics_list)
        )

@dataclass
class Constraints:
    max_risk: float = float('inf')
    max_time: float = float('inf')
    max_fuel: float = float('inf')
    max_cost: float = float('inf')

    def check(self, metrics: EdgeMetrics) -> int:
        violations = 0
        if metrics.risk > self.max_risk: violations += 1
        if metrics.time > self.max_time: violations += 1
        if metrics.fuel > self.max_fuel: violations += 1
        if metrics.cost > self.max_cost: violations += 1
        return violations

class CayleyTSP:
    def __init__(self, m: int, generators: List[Tuple[int, int]], weights: Dict[Tuple[int, int], EdgeMetrics]):
        self.m = m
        self.n = m * m
        self.generators = generators
        self.weights = weights
        self.k = len(generators)

    def get_score(self, path_metrics: EdgeMetrics, weights_vector: List[float], violations: int) -> float:
        vec = path_metrics.to_vec()
        base_score = sum(v * w for v, w in zip(vec, weights_vector))
        return base_score + (violations * 10000)

    def sigma_to_path(self, sigma: Tuple[int, ...]) -> List[int]:
        path = []
        curr = (0, 0)
        for _ in range(self.n):
            s = (curr[0] + curr[1]) % self.m
            gen_idx = sigma[s]
            path.append(gen_idx)
            gen = self.generators[gen_idx]
            curr = ((curr[0] + gen[0]) % self.m, (curr[1] + gen[1]) % self.m)
        return path

    def evaluate_sigma(self, sigma: Tuple[int, ...], constraints: Constraints = None) -> Optional[Tuple[EdgeMetrics, int]]:
        path = self.sigma_to_path(sigma)
        return self.evaluate_path(path, constraints)

    def evaluate_path(self, path: List[int], constraints: Constraints = None) -> Optional[Tuple[EdgeMetrics, int]]:
        if len(path) != self.n: return None
        visited = set()
        curr = (0, 0)
        metrics_list = []
        for gen_idx in path:
            if curr in visited: return None
            visited.add(curr)
            gen = self.generators[gen_idx]
            metrics_list.append(self.weights[gen])
            curr = ((curr[0] + gen[0]) % self.m, (curr[1] + gen[1]) % self.m)

        if len(visited) == self.n and curr == (0, 0):
            total_metrics = EdgeMetrics.sum_metrics(metrics_list)
            violations = constraints.check(total_metrics) if constraints else 0
            return total_metrics, violations
        return None

class FiberUniformSolver:
    def __init__(self, tsp: CayleyTSP, weights_vector: List[float], constraints: Constraints = None):
        self.tsp = tsp
        self.weights_vector = weights_vector
        self.constraints = constraints

    def solve(self) -> Tuple[Optional[List[int]], float, Optional[EdgeMetrics], int]:
        best_sigma = None
        best_score = float('inf')
        best_metrics = None
        best_violations = 0

        for sigma in product(range(self.tsp.k), repeat=self.tsp.m):
            result = self.tsp.evaluate_sigma(sigma, self.constraints)
            if result:
                metrics, violations = result
                score = self.tsp.get_score(metrics, self.weights_vector, violations)
                if score < best_score:
                    best_score = score
                    best_sigma = sigma
                    best_metrics = metrics
                    best_violations = violations

        if best_sigma:
            return self.tsp.sigma_to_path(best_sigma), best_score, best_metrics, best_violations
        return None, float('inf'), None, 0
