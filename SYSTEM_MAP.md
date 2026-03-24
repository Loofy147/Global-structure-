# SYSTEM MAP: THE GLOBAL STRUCTURE ENGINE

This map aligns the Python implementation with the algebraic framework of the short exact sequence:
$0 \to H \to G \to G/H \to 0$

---

## C1: Fiber Map (Stratification)
*Methods that define the decomposition of the group into layers.*

- `core.py: _level_valid(lv, m)` -> Validates if a level assignment obeys group structure.
- `core.py: valid_levels(m)` -> Enumerates possible fiber-level mappings.
- `engine.py: Domain(m, k)` -> High-level registry for fiber-quotient parameters.
- `frontiers.py: dec4(v), enc4(i,j,k,l)` -> 4D coordinate mapping for $G_4^4$.

---

## C2: Twisted Translation (Lifting)
*Methods governing the local-to-global lift via $Q_c(i,j) = (i+b_c(j), j+r_c)$.*

- `core.py: table_to_sigma(table, m)` -> Converts a fiber-table to a full permutation $\sigma$.
- `core.py: compose_Q(table, m)` -> Composes the fiber-level permutations into the kernel map $Q$.
- `core.py: is_single_cycle(Q, m)` -> Verifies if the composition generates a single $m^2$-cycle.
- `engine.py: ProofBuilder.build(w, solution)` -> Constructs a formal proof object from a twisted translation.

---

## C3: Governing Condition (Minimal Predicates)
*Methods that compute the arithmetic feasibility conditions.*

- `core.py: extract_weights(m, k)` -> Computes the 8 fundamental weights of the problem.
- `moduli_theorem.py: GroupCohomology.H1_classes(m)` -> Counts the number of distinct "governing classes".
- `theorems.py: verify_all_theorems()` -> Exhaustive verification of existence conditions across domains.

---

## C4: Parity Obstruction (Impossibility)
*Methods identifying why a solution cannot exist.*

- `core.py: h2_blocks` (in Weights) -> The boolean flag for the H² parity obstruction.
- `moduli_theorem.py: H2_obstruction(k)` -> Explicitly identifies the non-trivial class in $H^2(\mathbb{Z}_2, \mathbb{Z}/2)$.
- `frontiers.py: prove_fiber_uniform_k4_impossible()` -> Exhaustive proof of the m=4, k=4 fiber-uniform gap.

---

## Solvers & Orchestration
- `core.py: run_sa(m, ...)` -> The primary Simulated Annealing engine for finding $\sigma$.
- `engine.py: Engine.run(m, k)` -> The top-level entry point for analysis.
- `engine.py: ClassifyingSpace.obstruction_grid()` -> Visualizes the feasibility map across the $(m,k)$ plane.
- `benchmark.py: run_benchmark()` -> Performance metrics for solver variations.


---

## 5. Summary of Built Value
- **Consolidated Knowledge:** All triage findings and proofs from `open_problems.py` are now unified in the core `frontiers.py` and `engine.py`.
- **Structural Audit:** This document itself provides a first-ever mapping of the code to the 0-H-G framework.
- **Precision Targeting:** The `Basin Hopping` strategy and `Geometric Complexity` audit (GENUINE_HEADS.md) provide the roadmap for the next development phase.
- **Accuracy:** Corrected the W7 formula in `core.py`, providing an exact solution lower bound for the first time.
