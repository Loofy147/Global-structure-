# Claude's Cycles: Even-m and k=4 Investigations

This repository explores the combinatorial problem introduced by Donald Knuth in "Claude's Cycles" (2026). We provide a unified algebraic framework for analyzing Hamiltonian decompositions of highly symmetric directed Cayley graphs.

## Key Features

- **Unified Algebraic Framework:** Based on the short exact sequence $0 \to H \to G \to G/H \to 0$, we formalize the "twisted translation" as a local-to-global lift.
- **Parity Obstruction Theorem:** A proof that the column-uniform construction (r-triple) is impossible for even $m$ when $k=3$.
- **$k=4$ Resolution:** We establish the arithmetic feasibility of $k=4$ via the (1,1,1,1) r-quadruple, resolving the parity obstruction observed for $k=3$.
- **Prior Art Engagement:** The work is contextualized within the Alspach conjecture literature (Bermond et al. 1989, Liu 2003).

## Files

- `paper1_even_m.py`: Main paper generation script (produces `paper1_even_m.pdf`).
- `cycles_even_m.py`: Discovery engine for even $m$ and SA search.
- `global_structure_refined.py`: Formal statement of the Master Theorem and SES framework.
- `proof_k4_obstruction.py`: Proof that fiber-uniform $\sigma$ is impossible for $m=4, k=4$.

## Usage

To generate the paper:
```bash
pip install reportlab
python3 paper1_even_m.py
```

To run the discovery engine:
```bash
python3 cycles_even_m.py
```

## Geometric Construction (Odd m)
- `verify_spike.py`: Verifies the spike-function construction for odd $m$.
- `GEOMETRIC_CONSTRUCTION.md`: Explains the spike-function framework and its parameters.
