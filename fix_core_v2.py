with open("core.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "r_tuples = [] if h2_uni else" in line:
        lines[i] = "    r_tuples = [t for t in iprod(cp, repeat=k) if sum(t) % m == 0] if not h2_uni else []\n"
    if "mid = m - (k - 1)" in line:
        lines[i] = "    canon = None\n    if r_tuples:\n        canon = r_tuples[0]\n"
    if "sol_lb = phi_m * (cb**(k-1)) if (not h2_uni and r_count > 0) else 0" in line:
        lines[i] = "    sol_lb = phi_m * (cb**(k-1)) if (not h2_uni) else 0\n"

with open("core.py", "w") as f:
    f.writelines(lines)
