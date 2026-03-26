import sys; sys.path.insert(0,'.')
from core import solve_spike, verify_sigma, valid_levels, compose_Q, is_single_cycle
from math import gcd

def test_spike_existence():
    for m in [3, 5]:
        print(f"Testing spike existence for m={m}...")
        sigma = solve_spike(m)
        if not sigma:
            print(f"FAILED: No sigma found for m={m}")
            return False
        if not verify_sigma(sigma, m):
            print(f"FAILED: Sigma found for m={m} but failed verification")
            return False
        print(f"PASSED: Sigma found and verified for m={m}")
    return True

def test_single_cycle_property():
    def make_Q_spike(m, r, delta, j0=0):
        Q={}
        for i in range(m):
            for j in range(m):
                b = delta if j==j0 else 0
                Q[(i,j)] = ((i+b)%m, (j+r)%m)
        return Q

    for m in [3, 5, 7, 9]:
        r_triple = (1, m-2, 1)
        delta = 1
        for r in r_triple:
            Q = make_Q_spike(m, r, delta)
            if not is_single_cycle(Q, m):
                print(f"FAILED: Q not single cycle for m={m}, r={r}")
                return False
    print("PASSED: Single cycle property verified for m in [3, 5, 7, 9]")
    return True

if __name__ == "__main__":
    s1 = test_spike_existence()
    s2 = test_single_cycle_property()
    if s1 and s2:
        print("\nALL PRE-COMMIT TESTS PASSED")
        sys.exit(0)
    else:
        print("\nPRE-COMMIT TESTS FAILED")
        sys.exit(1)
