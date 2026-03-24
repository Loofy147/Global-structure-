import math
from math import gcd

def phi(m):
    return sum(1 for r in range(1, m) if gcd(r, m) == 1)

def calc_W7(m, k=3):
    # phi(m) * coprime_b(m)^(k-1)
    # where coprime_b = m^(m-1) * phi(m)
    p = phi(m)
    cb = (m**(m-1)) * p
    return p * (cb**(k-1))

def main():
    print(f"{'m':<4} {'phi(m)':<8} {'W7 (predicted)':<20}")
    print("-" * 35)
    for m in [3, 4, 5, 6]:
        w7 = calc_W7(m)
        print(f"{m:<4} {phi(m):<8} {w7:<20,}")

if __name__ == "__main__":
    main()
