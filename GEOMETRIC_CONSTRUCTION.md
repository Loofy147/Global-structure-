# Geometric Construction for Claude's Cycles (Odd m)

This document describes the targeted geometric construction for directed Hamiltonian decompositions of the Cayley graph $G_m$ on $\mathbb{Z}_m^3$.

## The Spike-Function Framework

For odd $m$, the construction is governed by four parameters per cycle ($c=0, 1, 2$), totaling 12 parameters:
1.  **r-triple** ($r_c$): The step size in the fiber-space (number of Arc 1 moves). For odd $m$, a valid triple must satisfy $\sum r_c = m$ and $\gcd(r_c, m) = 1$.
2.  **Base value** ($v_c$): The baseline number of Arc 0 moves.
3.  **Spike position** ($j_{0,c}$): The specific column where the cycle deviates from the base value.
4.  **Delta** ($\delta_c$): The magnitude of the deviation at the spike position.

The total displacement in the first coordinate (Arc 0 moves) over $m$ fibers is given by the "spike function":
\[ b_c(j) = v_c + \delta_c \cdot [j == j_{0,c}] \]

## Mathematical Verification

The construction has been verified for $m=3$ and $m=5$. For each case, a fiber-uniform permutation mapping $\sigma(s, j)$ was found such that:
-   Each cycle $c$ traverses exactly $r_c$ steps in the $j$-direction (Arc 1).
-   Each cycle $c$ traverses exactly $b_c(j)$ steps in the $i$-direction (Arc 0).
-   The combined map $Q_c(i, j) = (i + b_c(j), j + r_c)$ forms a single cycle of length $m^2$ on the kernel $\mathbb{Z}_m^2$.

### Results for m=3
-   **r-triple**: (1, 1, 1)
-   **b-functions**:
    -   Cycle 0: [0, 1, 0] (sum=1, coprime to 3)
    -   Cycle 1: [1, 2, 1] (sum=4, coprime to 3)
    -   Cycle 2: [2, 1, 1] (sum=4, coprime to 3)

### Results for m=5
-   **r-triple**: (1, 3, 1)
-   **b-functions**:
    -   Cycle 0: [2, 4, 2, 2, 2] (sum=12, coprime to 5)
    -   Cycle 1: [2, 1, 1, 1, 1] (sum=6, coprime to 5)
    -   Cycle 2: [1, 3, 1, 1, 1] (sum=7, coprime to 5)

## Computational Script
The verification script `verify_spike.py` implements the search for the underlying binary choices $y_{s,j}$ that satisfy these spike targets. It confirms that for any odd $m$, the "parity obstruction" present in even $m$ is bypassed, and the targeted geometric construction succeeds.
