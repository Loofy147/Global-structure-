import itertools

def check_period(R, m, k):
    # R in Z_m^k such that sum(R) = 0 mod m.
    # We want to check if R generates the kernel {x : sum(x) = 0 mod m}.
    # The kernel is isomorphic to Z_m^{k-1}.

    curr = [0]*k
    visited = {tuple(curr)}
    for _ in range(256):
        for i in range(k): curr[i] = (curr[i] + R[i]) % m
        if tuple(curr) == (0,0,0,0): return len(visited)
        if tuple(curr) in visited: break
        visited.add(tuple(curr))
    return len(visited)

def solve():
    m, k = 4, 4
    # For k=4, m=4: kernel size is 4^3 = 64.
    # Can any R generate it?
    found = False
    for R in itertools.product(range(m), repeat=k):
        if sum(R) % m == 0:
            p = check_period(R, m, k)
            if p == 64:
                found = True; break

    if not found:
        print("THEOREM 4.1: For m=4, k=4, no single translation R generates the fiber kernel.")
        print("Thus, fiber-uniform sigma is never Hamiltonian.")

if __name__ == "__main__":
    solve()
