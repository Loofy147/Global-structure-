# SYSTEM MAP: GLOBAL STRUCTURE ENGINE v2.3

## C1: Fiber Map (Stratification)
- `core.py: extract_weights(m, k)` -> Computes $H^2$ obstruction and $\phi(m)$.
- `engine.py: Engine.run(m, k)` -> Orchestrates feasibility analysis across domains.
- `domains.py`: Registry for multi-domain stratified maps including **TSP on $Z_m^2$**.

## C2: Twisted Translation (Lifting)
- `core.py: construct_spike_sigma(m)` -> Robust $O(m^2)$ search for odd $m$ decompositions.
- `frontiers.py: solve_tsp_P7()` -> Optimization solver leveraging fiber symmetry.
- `frontiers.py: solve_P2()` -> Basin Hopping SA for even $m$.

## C3: Governing Condition
- `theorems.py: verify_all_theorems()` -> Integrated suite for core results.
- `solutions.py`: Validated repository for proven $\sigma$ mappings.

## C4: Parity Obstruction
- `core.py: Weights.h2_blocks` -> Identifies $H^2$ gaps for uniform mappings.
- `domains.py: analyse_P6_product_groups()` -> Extends parity logic to mixed moduli.

## Optimization Flow (TSP)
1. **Model:** Define weights on arc types.
2. **Stratify:** Restrict paths to fiber-uniform mappings.
3. **Minimize:** Exhaustively or heuristically search the reduced space $k^m$.
