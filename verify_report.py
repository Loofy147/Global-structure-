import sys, math
from math import gcd
from core import construct_spike_sigma, verify_sigma, extract_weights, count_coprime_sum_functions
from solutions import SOLUTION_M4_LIST, SOLUTION_Z4X6

def report_status(msg, ok):
    sym = "\033[92m✓\033[0m" if ok else "\033[91m✗\033[0m"
    print(f"{sym} {msg}")

def verify_report():
    print("\nVerifying Report Content vs. Codebase:\n")

    # 1. Odd m (Spike)
    m_odd = [3, 5, 7]
    seeds = {3: 42, 5: 42, 7: 123}
    ok_odd = all(verify_sigma(construct_spike_sigma(m, seed=seeds[m]), m) for m in m_odd)
    report_status(f"Odd m (Spike) construction verified for {m_odd}", ok_odd)

    # 2. Even m=4 (SA)
    ok_m4 = verify_sigma(SOLUTION_M4_LIST, 4)
    report_status("Even m=4 verified solution exists and is valid", ok_m4)

    # 3. Nb(m) Formula
    m_list = [2, 3, 4, 5]
    ok_nb = all(count_coprime_sum_functions(m) == sum(1 for b in __import__('itertools').product(range(m), repeat=m) if gcd(sum(b)%m, m) == 1) for m in m_list)
    report_status(f"Nb(m) formula verified for {m_list}", ok_nb)

    # 4. Product Groups (Z4xZ6)
    m, n = 4, 6
    gens = [(1, 0), (0, 1)]
    ok_z4x6 = True
    for c in range(2):
        visited = set(); curr = (0, 0)
        for _ in range(m * n):
            if curr in visited: break
            visited.add(curr)
            p = SOLUTION_Z4X6[curr]
            gen = gens[p[c]]
            curr = ((curr[0] + gen[0]) % m, (curr[1] + gen[1]) % n)
        if len(visited) != m * n: ok_z4x6 = False; break
    report_status("Z4xZ6 product group verified solution valid", ok_z4x6)

    # 5. Parity Obstruction (m=6)
    w_m6 = extract_weights(6, 3)
    ok_m6_obs = w_m6.h2_blocks
    report_status("m=6 parity obstruction correctly identified (h2_blocks=True)", ok_m6_obs)

    print("\nReport validation complete.\n")

if __name__ == "__main__":
    verify_report()
