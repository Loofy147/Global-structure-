import sys; sys.path.insert(0,'.')
from core import construct_spike_sigma, verify_sigma
import time

def benchmark(m_list):
    print(f"{'m':>4} | {'Nodes':>10} | {'Construct':>12} | {'Verify':>12} | Status")
    print("-" * 65)
    for m in m_list:
        n = m**3
        t0 = time.time()
        sig = construct_spike_sigma(m)
        t1 = time.time()
        v = verify_sigma(sig, m)
        t2 = time.time()

        status = "✓" if v else "✗"
        print(f"{m:4d} | {n:10d} | {t1-t0:11.6f}s | {t2-t1:11.6f}s | {status}")

if __name__ == "__main__":
    m_values = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    benchmark(m_values)
