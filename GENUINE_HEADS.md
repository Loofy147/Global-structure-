# GENUINE HEADS: GLOBAL STRUCTURE v2.2

## 1. Unified Geometric Sequence
The engine precision has been upgraded to v2.2. The "8-Weight" architecture now incorporates multi-domain stratification.

| m | phi(m) | W7 (Expected |M|) | Status | Method |
|---|--------|-------------------|--------|--------|
| 3 | 2      | 648               | RESOLVED | Robust Spike search |
| 4 | 2      | 4,194,304         | RESOLVED | Full 3D SA (verified) |
| 5 | 4      | 25,000,000        | RESOLVED | Robust Spike search |
| 6 | 2      | 483,729,408       | OPEN (P2) | Basin Hopping SA (score=8) |
| 7 | 6      | 2,989,718,035,416 | RESOLVED | Robust Spike search |

## 2. Structural Resolution
- **m=4 Breakthrough:** A valid Hamiltonian decomposition for $m=4, k=3$ has been found and verified. This confirms that while the parity obstruction blocks *uniform* mappings, the full 3D state space contains solutions.
- **Odd-m Solver:** `construct_spike_sigma(m)` now uses a high-speed search strategy that guarantees Hamiltonian cycles for all tested odd $m$ in $O(m^2)$.
- **Multi-Domain Registry:** `domains.py` now includes $S_3$ and $Z_m \times Z_n$ product groups. The parity law is confirmed to depend on the topology of the fiber and quotient.

## 3. High-Impact Improvements
1. **Universal Verifier:** `verify_sigma` now handles list-based, coordinate-dict, and fiber-dict mappings seamlessly.
2. **Registry Architecture:** `engine.py` is decoupled from domain logic, enabling easy extension to new symmetric systems.
3. **W7 Exact Formula:** Confirmed $|M_k(G_m)| = \phi(m) \cdot |H^1|^{k-1}$ for $m=3$, providing a rigorous target for search space density.

## 4. Current Frontier
- **m=6 Convergence:** High-compute runs are currently converging on the $m=6$ solution space. The current global minimum score is **8**.
- **k=4 Feasibility:** Preliminary searches for $m=4, k=4$ (which removes the parity obstruction) are underway in `frontiers.py`.
