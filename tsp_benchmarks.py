import random
import time
import math
import itertools
from itertools import product
from typing import List, Tuple, Dict, Optional
from tsp_global_engine import CayleyTSP, EdgeMetrics, Constraints

class NearestNeighborSolver:
    def __init__(self, tsp: CayleyTSP, weights_vector: List[float], constraints: Constraints = None):
        self.tsp = tsp
        self.weights_vector = weights_vector
        self.constraints = constraints

    def solve(self) -> Tuple[Optional[List[int]], float, Optional[EdgeMetrics], int]:
        visited = set()
        curr = (0, 0)
        path = []
        metrics_list = []
        for step in range(self.tsp.n):
            visited.add(curr)
            best_gen_idx = -1
            best_local_score = float('inf')
            for idx, gen in enumerate(self.tsp.generators):
                next_node = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
                if step < self.tsp.n - 1:
                    if next_node not in visited:
                        m_edge = self.tsp.weights[gen]
                        local_score = sum(v * w for v, w in zip(m_edge.to_vec(), self.weights_vector))
                        if local_score < best_local_score:
                            best_local_score = local_score
                            best_gen_idx = idx
                else:
                    if next_node == (0, 0):
                        best_gen_idx = idx
                        break
            if best_gen_idx == -1: return None, float('inf'), None, 0
            gen = self.tsp.generators[best_gen_idx]
            path.append(best_gen_idx)
            metrics_list.append(self.tsp.weights[gen])
            curr = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
        if len(visited) == self.tsp.n and curr == (0, 0):
            total_metrics = EdgeMetrics.sum_metrics(metrics_list)
            violations = self.constraints.check(total_metrics) if self.constraints else 0
            score = self.tsp.get_score(total_metrics, self.weights_vector, violations)
            return path, score, total_metrics, violations
        return None, float('inf'), None, 0

class RandomizedSolver:
    def __init__(self, tsp: CayleyTSP, weights_vector: List[float], constraints: Constraints = None):
        self.tsp = tsp
        self.weights_vector = weights_vector
        self.constraints = constraints

    def solve(self, iterations: int = 1000) -> Tuple[Optional[List[int]], float, Optional[EdgeMetrics], int]:
        best_path, best_score, best_metrics, best_violations = None, float('inf'), None, 0
        for _ in range(iterations):
            visited = set(); curr = (0, 0); path = []; valid = True
            for step in range(self.tsp.n):
                visited.add(curr); possible = []
                for idx, gen in enumerate(self.tsp.generators):
                    next_node = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
                    if step < self.tsp.n - 1:
                        if next_node not in visited: possible.append(idx)
                    else:
                        if next_node == (0, 0): possible.append(idx)
                if not possible: valid = False; break
                chosen_idx = random.choice(possible); path.append(chosen_idx)
                gen = self.tsp.generators[chosen_idx]
                curr = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
            if valid:
                res = self.tsp.evaluate_path(path, self.constraints)
                if res:
                    metrics, violations = res; score = self.tsp.get_score(metrics, self.weights_vector, violations)
                    if score < best_score:
                        best_score, best_path, best_metrics, best_violations = score, path, metrics, violations
        return best_path, best_score, best_metrics, best_violations

class GeneticAlgorithmSolver:
    def __init__(self, tsp: CayleyTSP, weights_vector: List[float], constraints: Constraints = None):
        self.tsp = tsp
        self.weights_vector = weights_vector
        self.constraints = constraints

    def solve(self, pop_size: int = 100, generations: int = 200) -> Tuple[Optional[List[int]], float, Optional[EdgeMetrics], int]:
        population = []
        for _ in range(pop_size * 2):
            p = self._generate_random_path()
            if p: population.append(p)
        if not population: return None, float('inf'), None, 0

        for _ in range(generations):
            population = sorted(population, key=lambda p: self._fitness(p))
            elite_size = max(1, len(population) // 2)
            new_pop = population[:elite_size]
            while len(new_pop) < pop_size:
                p1, p2 = random.sample(new_pop, 2) if len(new_pop) >= 2 else (new_pop[0], new_pop[0])
                pt = random.randint(1, self.tsp.n - 1)
                child = p1[:pt] + p2[pt:]
                if self.tsp.evaluate_path(child): new_pop.append(child)
                else: new_pop.append(p1)
            population = new_pop

        best_path = sorted(population, key=lambda p: self._fitness(p))[0]
        res = self.tsp.evaluate_path(best_path, self.constraints)
        if res: return best_path, self.tsp.get_score(res[0], self.weights_vector, res[1]), res[0], res[1]
        return None, float('inf'), None, 0

    def _generate_random_path(self):
        curr = (0, 0); visited = set(); path = []
        for step in range(self.tsp.n):
            visited.add(curr); possible = []
            for idx, gen in enumerate(self.tsp.generators):
                next_node = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
                if step < self.tsp.n - 1:
                    if next_node not in visited: possible.append(idx)
                else:
                    if next_node == (0, 0): possible.append(idx)
            if not possible: return None
            idx = random.choice(possible); path.append(idx)
            gen = self.tsp.generators[idx]; curr = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
        return path

    def _fitness(self, path):
        res = self.tsp.evaluate_path(path, self.constraints)
        return self.tsp.get_score(res[0], self.weights_vector, res[1]) if res else 1e18

class AntColonySolver:
    def __init__(self, tsp: CayleyTSP, weights_vector: List[float], constraints: Constraints = None):
        self.tsp = tsp
        self.weights_vector = weights_vector
        self.constraints = constraints
        self.pheromone = {(i, j, g_idx): 1.0 for i in range(tsp.m) for j in range(tsp.m) for g_idx in range(tsp.k)}

    def solve(self, ants: int = 20, iterations: int = 50) -> Tuple[Optional[List[int]], float, Optional[EdgeMetrics], int]:
        best_path, best_score = None, float('inf')
        for _ in range(iterations):
            paths = []
            for _ in range(ants):
                p = self._run_ant()
                if p:
                    score = self._fitness(p)
                    if score < best_score: best_score, best_path = score, p
                    paths.append((p, score))
            for k in self.pheromone: self.pheromone[k] *= 0.9
            for p, s in paths:
                if s < 1e17:
                    curr = (0, 0)
                    for g_idx in p:
                        self.pheromone[(curr[0], curr[1], g_idx)] += 100.0 / s
                        gen = self.tsp.generators[g_idx]
                        curr = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
        if best_path:
            res = self.tsp.evaluate_path(best_path, self.constraints)
            return best_path, self.tsp.get_score(res[0], self.weights_vector, res[1]), res[0], res[1]
        return None, float('inf'), None, 0

    def _run_ant(self):
        curr = (0, 0); visited = set(); path = []
        for step in range(self.tsp.n):
            visited.add(curr); possible = []
            for idx, gen in enumerate(self.tsp.generators):
                next_node = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
                if step < self.tsp.n - 1:
                    if next_node not in visited: possible.append(idx)
                else:
                    if next_node == (0, 0): possible.append(idx)
            if not possible: return None
            weights = [self.pheromone[(curr[0], curr[1], idx)] for idx in possible]
            idx = random.choices(possible, weights=weights)[0]; path.append(idx)
            gen = self.tsp.generators[idx]; curr = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
        return path

    def _fitness(self, path):
        res = self.tsp.evaluate_path(path, self.constraints)
        return self.tsp.get_score(res[0], self.weights_vector, res[1]) if res else 1e18

class HeldKarpSolver:
    def __init__(self, tsp: CayleyTSP, weights_vector: List[float], constraints: Constraints = None):
        self.tsp = tsp
        self.weights_vector = weights_vector
        self.constraints = constraints

    def solve(self) -> Tuple[Optional[List[int]], float, Optional[EdgeMetrics], int]:
        n = self.tsp.n
        node_to_idx = {(i, j): idx for idx, (i, j) in enumerate(product(range(self.tsp.m), repeat=2))}
        idx_to_node = {idx: node for node, idx in node_to_idx.items()}
        dist = [[float('inf')] * n for _ in range(n)]
        gen_for_edge = [[-1] * n for _ in range(n)]
        for u_idx in range(n):
            u_node = idx_to_node[u_idx]
            for g_idx, gen in enumerate(self.tsp.generators):
                v_node = ((u_node[0] + gen[0]) % self.tsp.m, (u_node[1] + gen[1]) % self.tsp.m)
                v_idx = node_to_idx[v_node]
                m_edge = self.tsp.weights[gen]
                cost = sum(v * w for v, w in zip(m_edge.to_vec(), self.weights_vector))
                if cost < dist[u_idx][v_idx]: dist[u_idx][v_idx], gen_for_edge[u_idx][v_idx] = cost, g_idx

        dp = {}
        dp[(1, 0)] = 0
        for size in range(2, n + 1):
            for subset in self._get_subsets(size, n):
                if not (subset & 1): continue
                for last in range(1, n):
                    if not (subset & (1 << last)): continue
                    prev_subset = subset & ~(1 << last)
                    res = float('inf')
                    for prev in range(n):
                        if (prev_subset & (1 << prev)) and dist[prev][last] != float('inf'):
                            val = dp.get((prev_subset, prev), float('inf')) + dist[prev][last]
                            if val < res: res = val
                    dp[(subset, last)] = res

        full_mask = (1 << n) - 1
        best_total, last_node = float('inf'), -1
        for i in range(1, n):
            if dist[i][0] != float('inf'):
                val = dp.get((full_mask, i), float('inf')) + dist[i][0]
                if val < best_total: best_total, last_node = val, i
        if last_node == -1: return None, float('inf'), None, 0
        path_indices, curr_mask, curr_node = [gen_for_edge[last_node][0]], full_mask, last_node
        while curr_mask != 1:
            prev_mask = curr_mask & ~(1 << curr_node)
            for prev in range(n):
                if (prev_mask & (1 << prev)) and dist[prev][curr_node] != float('inf'):
                    if math.isclose(dp[(curr_mask, curr_node)], dp.get((prev_mask, prev), float('inf')) + dist[prev][curr_node]):
                        path_indices.append(gen_for_edge[prev][curr_node]); curr_node, curr_mask = prev, prev_mask; break
        path_indices.reverse()
        res = self.tsp.evaluate_path(path_indices, self.constraints)
        return (path_indices, self.tsp.get_score(res[0], self.weights_vector, res[1]), res[0], res[1]) if res else (None, float('inf'), None, 0)

    def _get_subsets(self, size, n):
        for combo in itertools.combinations(range(n), size):
            mask = 0
            for i in combo: mask |= (1 << i)
            yield mask
