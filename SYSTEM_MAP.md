# SYSTEM MAP: GLOBAL STRUCTURE ENGINE v2.1

## C1: Fiber Map (Stratification)
- `core.py: extract_weights(m, k)` -> Computes $H^2$ obstruction and $\phi(m)$.
- `engine.py: Engine.run(m, k)` -> Orchestrates the feasibility analysis.

## C2: Twisted Translation (Lifting)
- `core.py: construct_spike_sigma(m)` -> **Deterministic** O(m²) construction for odd m.
- `core.py: solve_spike(m)` -> Geometric search for b-function spikes.
- `core.py: run_sa(m)` -> Full-space Simulated Annealing for even m solutions.

## C3: Governing Condition
- `core.py: Weights.h1_exact` -> $\phi(m)$ exact gauge multiplicity.
- `core.py: Weights.sol_lb` -> Predicted solution count lower bound.

## C4: Parity Obstruction
- `core.py: Weights.h2_blocks` -> Identifies the $H^2$ gap for column-uniform mappings.
- `engine.py: print_space()` -> Feasibility grid for Z_m^k.

## Solvers & Verification
- **Odd Solver:** `construct_spike_sigma` (Deterministic/Instant).
- **Even Solver:** `solve_P2` in `frontiers.py` (Full 3D SA).
- **Benchmark:** `benchmark_spike.py` (Scaling verification).
