import sys; sys.path.insert(0,'.')
from core import solve_spike, verify_sigma

for m in [3, 5, 7]:
    print(f"Testing solve_spike for m={m}...")
    sigma = solve_spike(m)
    if sigma:
        valid = verify_sigma(sigma, m)
        print(f"m={m}: SIGMA FOUND AND VERIFIED={valid}")
    else:
        print(f"m={m}: NOT FOUND")
