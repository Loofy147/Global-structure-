# Global Structure in Highly Symmetric Systems (v2.3)

**Finding global structure in combinatorial problems via the short exact sequence**  
**0 → H → G → G/H → 0**

Derived from Knuth's *Claude's Cycles* (Feb 2026). This framework provides a universal engine governing Cayley digraphs, Latin squares, Hamming codes, magic squares, product groups, and **combinatorial optimization (TSP)**.

---

## Repository Structure

```
core.py                 Verifier · Deterministic Spike Constructor · SA engine · m=4 solution
engine.py               Multi-domain pipeline · domain registry · classifying space
domains.py              Domain definitions (Cycles, S_3, Z_m x Z_n, TSP, Latin/Magic squares)
theorems.py             9 theorems verified · moduli theorem · cross-domain table
frontiers.py            Open problem solvers (m=6 search, k=4 search, TSP solver)
solutions.py            Registry of hardcoded verified solutions
benchmark_spike.py      O(m^2) construction benchmark for odd m
global_research_paper.pdf  The formal project findings and proofs
```

---

## Quick Start

```bash
# Run deterministic construction and verification for odd m
python3 benchmark_spike.py

# Run multi-domain verification engine
python3 engine.py

# Solve TSP on stratified symmetric graphs
python3 -c "import frontiers; frontiers.solve_tsp_P7(5)"
```

---

## Major Milestones (v2.3)

1.  **TSP Breakthrough:** Integrated the Traveling Salesman Problem into the framework, proving that stratification reduces optimization complexity on symmetric graphs.
2.  **m=4 Breakthrough:** Successfully found and verified a Hamiltonian decomposition for $m=4, k=3$, resolving the parity obstruction via a full 3D mapping.
3.  **Multi-Domain Expansion:** Integrated non-abelian Cayley graphs ($S_3$) and product groups ($Z_m \times Z_n$), proving the framework's universality.

## The Four Coordinates of Global Structure

Every symmetric system is stratified into:
- **C1: Fiber Map (Stratification):** Decomposes $G$ via $H$.
- **C2: Twisted Translation (Lifting):** Maps fiber actions to global cycles/paths.
- **C3: Governing Condition:** Algebraic constraints for Hamiltonian property.
- **C4: Parity Obstruction:** Cohomological gaps identifying "impossible" uniform configurations.
