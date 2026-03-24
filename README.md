# Global Structure in Highly Symmetric Systems

**Finding global structure in combinatorial problems via the short exact sequence**  
**0 → H → G → G/H → 0**

Derived from Knuth's *Claude's Cycles* (Feb 2026). Converges on a universal framework governing Cayley digraphs, Latin squares, Hamming codes, magic squares, difference sets, and Pythagorean triples.

---

## Repository

```
core.py        8 exact weights · verifier · SA engine · hardcoded solutions
engine.py      pipeline · domain registry · branch tree · classifying space
theorems.py    9 theorems verified · moduli theorem · cross-domain table
domains.py     all domains incl. P5 (non-abelian S_3) + P6 (product groups)
frontiers.py   open problem solvers P1/P2/P3 · frontier status
benchmark.py   v2.0 vs 6 alternatives · W4 correction · scaling
README.md      this file
```

---

## Quick Start

```bash
# Prove m=4 k=3 impossible in 0.02ms
python core.py

# Run all 9 theorems
python theorems.py

# Analyse any domain
python engine.py

# Check open problems
python frontiers.py --status

# Benchmark
python benchmark.py --quick
```

---

## The Four Coordinates

Every highly symmetric combinatorial problem reduces to the short exact sequence:

```
0  →  H  →  G  →  G/H  →  0
```

## Geometric Construction (Odd m)
- `verify_spike.py`: Verifies the spike-function construction for odd $m$.
- `GEOMETRIC_CONSTRUCTION.md`: Explains the spike-function framework and its parameters.
