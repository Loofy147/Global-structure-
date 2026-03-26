import sys; sys.path.insert(0,'.')
from core import valid_levels, compose_Q, is_single_cycle
from math import gcd

m = 3
levels = valid_levels(m)
print(f"Checking {len(levels)}^3 = {len(levels)**3} combinations for m=3")

for l0 in levels:
    for l1 in levels:
        for l2 in levels:
            table = [l0, l1, l2]
            Qs = compose_Q(table, m)
            if all(is_single_cycle(Q, m) for Q in Qs):
                print(f"Found valid m=3 decomposition!")
                for c in range(3):
                    # Extract r and sum_b
                    Q = Qs[c]
                    # r = j(0,0) - j(0,-1) ? No, let's just check the property
                    # In our construction, r_c = sum(s in 0..m-1) [arc_c at level s is 1]
                    r = sum(1 for s in range(m) if table[s][0][c] == 1)
                    # sum_b = sum(s in 0..m-1) [arc_c at level s is 0]
                    # Wait, b_c(j) is the i-shift at column j.
                    # Q_c(i,j) = (i + b_c(j), j + r_c)
                    # Let's check if Q_c indeed has this form.
                    is_tt = True
                    r_ref = (Q[(0,0)][1] - 0) % m
                    b_ref = [ (Q[(0,j)][0] - 0) % m for j in range(m) ]
                    for i in range(m):
                        for j in range(m):
                            if Q[(i,j)] != ((i + b_ref[j]) % m, (j + r_ref) % m):
                                is_tt = False; break
                        if not is_tt: break

                    if is_tt:
                        sb = sum(b_ref) % m
                        print(f"  Cycle {c}: r={r_ref}, sum_b={sb}, gcd(r,m)={gcd(r_ref,m)}, gcd(sb,m)={gcd(sb,m)}")
                sys.exit(0)
