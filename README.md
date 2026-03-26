# Global Structure in Highly Symmetric Systems

**Finding global structure in combinatorial problems via the short exact sequence**  
**0 → H → G → G/H → 0**

Derived from Knuth's *Claude's Cycles* (Feb 2026). Converges on a universal framework governing Cayley digraphs, Latin squares, Hamming codes, magic squares, difference sets, and Pythagorean triples.

---

## Repository

```
core.py                 8 weights · verifier · Deterministic Spike Constructor · SA engine
engine.py               pipeline · domain registry · classifying space
theorems.py             9 theorems verified · moduli theorem · cross-domain table
domains.py              all domains incl. P5 (non-abelian S_3) + P6 (product groups)
frontiers.py            open problem solvers P1/P2/P3 · parity proof
benchmark_spike.py      O(m^2) construction benchmark for odd m
global_research_paper.pdf  The formal project findings and proofs
README.md               this file
```

---

## Quick Start

```bash
# Run deterministic construction and verification for odd m
python3 benchmark_spike.py

# Prove m=4 k=3 impossible via parity obstruction
python3 engine.py

# Run all 9 theorems
python3 theorems.py
```

---

## The Four Coordinates

Every highly symmetric combinatorial problem reduces to the short exact sequence:

```
0  →  H  →  G  →  G/H  →  0
```

## Key Result: The Spike Rule (Odd m)
- `core.py: construct_spike_sigma(m)`: Deterministically builds a valid Hamiltonian decomposition for any odd $m$ in $O(m^2)$.
- `GEOMETRIC_CONSTRUCTION.md`: Theoretical background on the spike-function framework.
