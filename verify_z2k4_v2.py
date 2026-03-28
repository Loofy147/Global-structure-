import math
from itertools import permutations

def verify():
    m = 2; k = 4; n = 16
    all_p = list(permutations(range(k)))
    # Found in seed 48 of find_z2k4_full.py
    sigma = [2, 12, 3, 19, 16, 9, 12, 1, 7, 3, 14, 17, 21, 14, 9, 8]

    def get_adj(v, c):
        coords = [ (v >> i) & 1 for i in range(4) ]
        coords[c] ^= 1
        return sum(coords[i] << i for i in range(4))

    adj = [[get_adj(v, c) for c in range(k)] for v in range(n)]

    for c in range(k):
        vis = set()
        curr = 0
        for _ in range(n):
            if curr in vis: break
            vis.add(curr)
            cur_p_idx = sigma[curr]
            p = all_p[cur_p_idx]
            gen_idx = p[c]
            curr = adj[curr][gen_idx]
        if len(vis) != n:
            print(f"Color {c} failed. Length: {len(vis)}")
            return False
    print("Z_2^4 Hamiltonian Decomposition VERIFIED!")
    return True

if __name__ == "__main__":
    verify()
