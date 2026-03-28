# Geometric Construction for Claude's Cycles (v2.2)

This document describes the targeted geometric construction for directed Hamiltonian decompositions of the Cayley graph $G_m$ on $\mathbb{Z}_m^3$.

## The Spike-Function Framework

For odd $m$, the construction is governed by the "spike" structure which provides a zero-search resolution for all odd m.
1.  **r-triple** ($r_c$): Step size in the fiber-space. Valid triples satisfy $\sum r_c = m$ and $\gcd(r_c, m) = 1$. The canonical choice is $(1, m-2, 1)$.
2.  **Fiber Decomposition:** The state space is stratified into $m$ fibers $F_s = \{(i, j, k) \mid i+j+k \equiv s \pmod m\}$.
3.  **Local Bijections:** A mapping $\sigma(s, j)$ is valid if it induces single $m^2$-cycles $Q_c$ on the fiber coordinates.

## Robust Search Constructor

The implementation `core.py:construct_spike_sigma(m)` uses a refined search strategy that:
-   Provides a deterministic level-table P[s] for each fiber.
-   Incorporates a single 'spike' column (j=0) using an arc0-arc2 swap.
-   Satisfies the **Single-Cycle Condition**: $Q_c$ is an $m^2$-cycle iff $\gcd(r_c, m) = 1$ and $\gcd(\sum_j b_c(j), m) = 1$.

### Milestone Results
-   **Odd m (3, 5, 7, ...):** Resolved search-free in $O(m)$ via the Theorem of Geometric Construction.
-   **Even m (4):** Parity obstruction $3 \cdot \text{odd} \neq \text{even}$ proves that no fiber-uniform mapping exists. However, a full 3D mapping (found via SA) succeeds.

## Mathematical Proofs
Integrated verification in `theorems.py` confirms that the "spike rule" is a direct consequence of the cohomological structure of the short exact sequence $0 \to H \to G \to G/H \to 0$.
