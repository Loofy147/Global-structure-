import time, random
from core import _build_sa3, _sa_score

def bench():
    m=6; n, arc_s, pa = _build_sa3(m); nP=6
    sigma = [random.randrange(nP) for _ in range(n)]
    t0 = time.perf_counter()
    for _ in range(1000):
        _sa_score(sigma, arc_s, pa, n)
    t1 = time.perf_counter()
    print(f"1000 iters in {t1-t0:.4f}s ({1000/(t1-t0):.1f} iters/sec)")

if __name__ == "__main__":
    bench()
