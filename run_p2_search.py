from ses_engine_v4 import run_basin_escape_sa
import sys

# Try different seeds and stratification for P2
for s in range(5):
    print(f"P2 Search Seed {s}")
    # Stratification 2 means sigma(i, j) for Z_m^3.
    # User's score 7 was likely unrestricted (table size 216).
    # Let's try unrestricted but with the fast engine.
    best_tab, score, elapsed = run_basin_escape_sa(6, 3, max_iter=200000, strat_type=None, seed=s)
    print(f"Seed {s} Score: {score}")
