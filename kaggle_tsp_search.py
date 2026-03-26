import time
import random
import math
import itertools
from itertools import product, combinations
from typing import List, Tuple, Dict, Optional, Any

# --- CORE ENGINE ---

class EdgeMetrics:
    def __init__(self, distance, time, risk, fuel, cost):
        self.distance, self.time, self.risk, self.fuel, self.cost = distance, time, risk, fuel, cost
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
    def __init__(self, max_risk=2.0, max_time=1000.0):
        self.max_risk, self.max_time = max_risk, max_time
    def check(self, metrics):
        v = 0
        if metrics.risk > self.max_risk: v += 1
        if metrics.time > self.max_time: v += 1
        return v

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
        if not path or len(path) != self.n: return None
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
        if self.tsp.m <= 11:
            it = product(range(self.tsp.k), repeat=self.tsp.m)
        else:
            def sampler():
                for _ in range(5000000):
                    yield [random.randrange(self.tsp.k) for _ in range(self.tsp.m)]
            it = sampler()
        for sigma in it:
            path = self.tsp.sigma_to_path(sigma)
            res = self.tsp.evaluate_path(path, self.constraints)
            if res:
                m, v = res; score = self.tsp.get_score(m, self.weights_vec, v)
                if score < best_score: best_score, best_sigma, best_metrics, best_viols = score, sigma, m, v
        return (self.tsp.sigma_to_path(best_sigma), best_score, best_metrics, best_viols) if best_sigma else (None, 0, None, 0)

class NearestNeighborSolver:
    def __init__(self, tsp, weights_vec, constraints=None): self.tsp, self.weights_vec, self.constraints = tsp, weights_vec, constraints
    def solve(self):
        visited, curr, path, metrics_list = set(), (0, 0), [], []
        for step in range(self.tsp.n):
            visited.add(curr); best_idx, best_ls = -1, float('inf')
            for idx, gen in enumerate(self.tsp.generators):
                nxt = ((curr[0] + gen[0]) % self.tsp.m, (curr[1] + gen[1]) % self.tsp.m)
                if step < self.tsp.n - 1:
                    if nxt not in visited:
                        ls = sum(v * w for v, w in zip(self.tsp.weights[gen].to_vec(), self.weights_vec))
                        if ls < best_ls: best_ls, best_idx = ls, idx
                elif nxt == (0, 0): best_idx = idx; break
            if best_idx == -1: return None, 0, None, 0
            path.append(best_idx); metrics_list.append(self.tsp.weights[self.tsp.generators[best_idx]])
            curr = ((curr[0] + self.tsp.generators[best_idx][0]) % self.tsp.m, (curr[1] + self.tsp.generators[best_idx][1]) % self.tsp.m)
        total = EdgeMetrics.sum_metrics(metrics_list); v = self.constraints.check(total) if self.constraints else 0
        return path, self.tsp.get_score(total, self.weights_vec, v), total, v

class GeneticAlgorithmSolver:
    def __init__(self, tsp, weights_vector, constraints=None):
        self.tsp, self.weights_vector, self.constraints = tsp, weights_vector, constraints
    def solve(self, pop_size=100, generations=300):
        population = []
        for _ in range(pop_size * 2):
            p = self._gen_rand()
            if p: population.append(p)
        if not population: return None, 0, None, 0
        for _ in range(generations):
            population = sorted(population, key=lambda p: self._fit(p))
            new_pop = population[:pop_size//2]
            while len(new_pop) < pop_size:
                p1, p2 = random.sample(new_pop, 2) if len(new_pop) >= 2 else (new_pop[0], new_pop[0])
                pt = random.randint(1, self.tsp.n - 1)
                c = p1[:pt] + p2[pt:]
                if self.tsp.evaluate_path(c): new_pop.append(c)
                else: new_pop.append(p1)
            population = new_pop
        best = sorted(population, key=lambda p: self._fit(p))[0]
        res = self.tsp.evaluate_path(best, self.constraints)
        return (best, self.tsp.get_score(res[0], self.weights_vector, res[1]), res[0], res[1]) if res else (None, 0, None, 0)
    def _gen_rand(self):
        c, v, p = (0,0), set(), []
        for s in range(self.tsp.n):
            v.add(c); poss = [i for i,g in enumerate(self.tsp.generators) if (((c[0]+g[0])%self.tsp.m, (c[1]+g[1])%self.tsp.m) not in v if s < self.tsp.n-1 else ((c[0]+g[0])%self.tsp.m, (c[1]+g[1])%self.tsp.m) == (0,0))]
            if not poss: return None
            i = random.choice(poss); p.append(i); c = ((c[0]+self.tsp.generators[i][0])%self.tsp.m, (c[1]+self.tsp.generators[i][1])%self.tsp.m)
        return p
    def _fit(self, p):
        res = self.tsp.evaluate_path(p, self.constraints)
        return self.tsp.get_score(res[0], self.weights_vector, res[1]) if res else 1e18

class AntColonySolver:
    def __init__(self, tsp, weights_vec, constraints=None):
        self.tsp, self.weights_vec, self.constraints = tsp, weights_vec, constraints
        self.pheromone = {(i, j, g_idx): 1.0 for i in range(tsp.m) for j in range(tsp.m) for g_idx in range(tsp.k)}
    def solve(self, ants=20, iterations=50):
        best_p, best_s = None, float('inf')
        for _ in range(iterations):
            paths = []
            for _ in range(ants):
                p = self._run_ant()
                if p:
                    res = self.tsp.evaluate_path(p, self.constraints)
                    if res:
                        s = self.tsp.get_score(res[0], self.weights_vec, res[1])
                        if s < best_s: best_s, best_p = s, p
                        paths.append((p, s))
            for k in self.pheromone: self.pheromone[k] *= 0.9
            for p, s in paths:
                c = (0,0)
                for i in p:
                    self.pheromone[(c[0], c[1], i)] += 100.0/s
                    g = self.tsp.generators[i]; c = ((c[0]+g[0])%self.tsp.m, (c[1]+g[1])%self.tsp.m)
        if best_p:
            res = self.tsp.evaluate_path(best_p, self.constraints)
            return best_p, self.tsp.get_score(res[0], self.weights_vec, res[1]), res[0], res[1]
        return None, 0, None, 0
    def _run_ant(self):
        c, v, p = (0,0), set(), []
        for s in range(self.tsp.n):
            v.add(c); poss = [i for i,g in enumerate(self.tsp.generators) if (((c[0]+g[0])%self.tsp.m, (c[1]+g[1])%self.tsp.m) not in v if s < self.tsp.n-1 else ((c[0]+g[0])%self.tsp.m, (c[1]+g[1])%self.tsp.m) == (0,0))]
            if not poss: return None
            w = [self.pheromone[(c[0], c[1], i)] for i in poss]
            i = random.choices(poss, weights=w)[0]; p.append(i); c = ((c[0]+self.tsp.generators[i][0])%self.tsp.m, (c[1]+self.tsp.generators[i][1])%self.tsp.m)
        return p

def calc_stability(tsp, solver_class, weights_vec, constraints, iters=5):
    path, _, _, _ = solver_class(tsp, weights_vec, constraints).solve()
    if not path: return 0.0
    total = 0
    for _ in range(iters):
        nw = {g: EdgeMetrics(*(v*(1+random.uniform(-0.1,0.1)) for v in m.to_vec())) for g, m in tsp.weights.items()}
        nt = CayleyTSP(tsp.m, tsp.generators, nw)
        np, _, _, _ = solver_class(nt, weights_vec, constraints).solve()
        if np: total += sum(1 for a, b in zip(path, np) if a != b) / len(path)
        else: total += 1.0
    return total / iters

def calc_diversity(p1, p2):
    if not p1 or not p2 or len(p1) != len(p2): return 1.0
    return sum(1 for a, b in zip(p1, p2) if a != b) / len(p1)

def run():
    print("GLOBAL STRUCTURE TSP BENCHMARK (KAGGLE - INTENSIVE V4)")
    ms = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    sw = [1.0, 5.0, 100.0, 2.0, 1.0]
    constraints = Constraints(max_risk=1.5, max_time=1000.0)
    solvers = [("FiberUniform", FiberUniformSolver), ("NearestNeighbor", NearestNeighborSolver), ("Genetic", GeneticAlgorithmSolver), ("AntColony", AntColonySolver)]
    header = f"{'m':<2} {'Solver':<16} {'Score':>10} {'Dist':>7} {'Time':>6} {'Risk':>5} {'Fuel':>5} {'Cost':>6} {'Viol':>4} {'Stab':>5} {'Div':>5} {'Time(ms)':>9}"
    print(header); print("-" * len(header))
    for m in ms:
        random.seed(m)
        gens = [(1,0),(0,1),(1,1)]; weights = {g: EdgeMetrics(random.uniform(5,15), random.uniform(1,5), random.uniform(0.01,0.2), random.uniform(2,10), random.uniform(10,50)) for g in gens}
        tsp = CayleyTSP(m, gens, weights); ref_path = None
        for name, solver_class in solvers:
            t0 = time.perf_counter()
            p, s, m_res, v = solver_class(tsp, sw, constraints).solve()
            elapsed = (time.perf_counter()-t0)*1000
            if not p:
                print(f"{m:<2} {name:<16} {'DNF':>10}")
                continue
            if name == "FiberUniform": ref_path = p; div = 0.0
            else: div = calc_diversity(ref_path, p) if ref_path else 0.0
            stab = calc_stability(tsp, solver_class, sw, constraints, iters=10) if m <= 11 else 0.0
            print(f"{m:<2} {name:<16} {s:>10.1f} {m_res.distance:>7.1f} {m_res.time:>6.1f} {m_res.risk:>5.2f} {m_res.fuel:>5.1f} {m_res.cost:>6.1f} {v:>4} {stab:>5.2f} {div:>5.2f} {elapsed:>9.1f}")
        print("-" * len(header))
if __name__ == "__main__": run()
