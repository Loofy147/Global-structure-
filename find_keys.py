import sys; sys.path.insert(0,'.')
from core import solve_spike, verify_sigma
import time

def find_and_save_keys(m_list):
    results = {}
    for m in m_list:
        print(f"Finding key for m={m}...", flush=True)
        t0 = time.time()
        sigma = solve_spike(m, max_iter=500000)
        dt = time.time() - t0
        if sigma:
            valid = verify_sigma(sigma, m)
            print(f"  m={m} FOUND in {dt:.2f}s (Verified: {valid})")
            results[m] = sigma
        else:
            print(f"  m={m} NOT FOUND in {dt:.2f}s")
    return results

if __name__ == "__main__":
    m_values = [3, 5, 7, 9, 11]
    keys = find_and_save_keys(m_values)

    import pickle
    with open('found_keys.pkl', 'wb') as f:
        pickle.dump(keys, f)
    print(f"\nSaved {len(keys)} keys to found_keys.pkl")
