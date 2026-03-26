# SYSTEM MAP: GLOBAL STRUCTURE ENGINE v2.2

## C1: Fiber Map (Stratification)
- `core.py: extract_weights(m, k)` -> Computes $H^2$ obstruction and $\phi(m)$.
- `engine.py: Engine.run(m, k)` -> Orchestrates feasibility analysis across domains.
- `domains.py`: Registry for multi-domain stratified maps ($Z_m^k$, $S_3$, $Z_m \times Z_n$).

## C2: Twisted Translation (Lifting)
- `core.py: construct_spike_sigma(m)` -> Robust $O(m^2)$ search for odd $m$ decompositions.
- `core.py: verify_sigma(sigma, m)` -> Universal verifier for list/dict mappings.
- `frontiers.py: solve_P2()` -> Basin Hopping SA for even $m$ (current best score=8).

## C3: Governing Condition
- `theorems.py: verify_all_theorems()` -> Integrated suite for 9 core results.
- `solutions.py`: Validated repository for proven $\sigma$ mappings (e.g., $m=4$).

## C4: Parity Obstruction
- `core.py: Weights.h2_blocks` -> Identifies $H^2$ gaps for uniform mappings.
- `domains.py: analyse_P6_product_groups()` -> Extends parity logic to mixed moduli.

## Architectural Flow
1. **Stratify:** Define $G \to G/H$ in `domains.py`.
2. **Predict:** Use `engine.py` to check $H^2$ and solution lower bounds ($W7$).
3. **Solve:** Deploy `core.py` (Odd $m$) or `frontiers.py` (Even $m$).
4. **Register:** Add verified solutions to `solutions.py`.
