from core import extract_weights
import math

def check_w7(m, k):
    w = extract_weights(m, k)
    phi_m = sum(1 for r in range(1, m) if math.gcd(r, m) == 1)
    cb = (m**(m-1)) * phi_m
    manual_w7 = phi_m * (cb**(k-1))
    print(f"m={m}, k={k}: extract_weights={w.sol_lb}, manual={manual_w7}, h2_blocks={w.h2_blocks}")

for m in [3, 4, 5, 6]:
    for k in [3, 4]:
        check_w7(m, k)
