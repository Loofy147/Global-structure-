# SYSTEM MAP: GLOBAL STRUCTURE ENGINE v2.0

## C1: Fiber Map (Stratification)
- `core.py: extract_weights(m, k)` -> Computes $H^2$ obstruction and $\phi(m)$.
- `engine.py: Engine.run(m, k)` -> Orchestrates the analysis.

## C2: Twisted Translation (Lifting)
- `core.py: solve_spike(m)` -> Geometric construction for odd $m$ using b-function spikes.
- `core.py: run_sa(m)` -> Full-space Simulated Annealing for non-uniform solutions.

## C3: Governing Condition
- `core.py: Weights.h1_exact` -> $\phi(m)$ exact gauge multiplicity.
- `core.py: Weights.sol_lb` -> Predicted solutions via generalized W7.

## C4: Parity Obstruction
- `core.py: Weights.h2_blocks_uniform` -> Specifically identifies the $H^2$ gap in column-uniform space.
- `engine.py: print_space()` -> Visualizes the feasibility grid.

## Solvers
- **Uniform Solver:** `solve_spike` (O(fast) for odd m).
- **Frontier Solver:** `solve_P2` in `frontiers.py` (Basin Hopping for even m).
