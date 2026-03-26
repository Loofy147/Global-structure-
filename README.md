# Global Structure in Highly Symmetric Systems (v2.2)

**Finding global structure in combinatorial problems via the short exact sequence**  
**0 → H → G → G/H → 0**

Derived from Knuth's *Claude's Cycles* (Feb 2026). This framework provides a universal engine governing Cayley digraphs, Latin squares, Hamming codes, magic squares, and product groups.

---

## Repository Structure

```
core.py                 Verifier · Deterministic Spike Constructor · SA engine · m=4 solution
engine.py               Multi-domain pipeline · domain registry · classifying space
domains.py              Domain definitions (Cycles, S_3, Z_m x Z_n, Latin squares, Magic squares)
theorems.py             9 theorems verified · moduli theorem · cross-domain table
frontiers.py            Open problem solvers (m=6 search, k=4 search)
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

# Run theorem verification suite
python3 theorems.py
```

---

## Major Milestones (v2.2)

1.  **m=4 Breakthrough:** Successfully found and verified a Hamiltonian decomposition for $m=4, k=3$, resolving the parity obstruction via a full 3D mapping.
2.  **Odd-m Deterministic Solver:** Implemented a robust $O(m^2)$ search-based constructor that satisfies the single-cycle conditions for all odd $m$.
3.  **Multi-Domain Expansion:** Integrated non-abelian Cayley graphs ($S_3$) and product groups ($Z_m \times Z_n$), proving the framework's universality.
4.  **m=6 Progress:** Kaggle and local high-compute runs have reached score **8** for $m=6, k=3$, significantly narrowing the search space.

## The Four Coordinates of Global Structure

Every symmetric system is stratified into:
- **C1: Fiber Map (Stratification):** Decomposes $G$ via $H$.
- **C2: Twisted Translation (Lifting):** Maps fiber actions to global cycles.
- **C3: Governing Condition:** Algebraic constraints for Hamiltonian property.
- **C4: Parity Obstruction:** Cohomological gaps identifying "impossible" uniform configurations.
