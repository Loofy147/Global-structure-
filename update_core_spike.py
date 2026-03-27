import sys
from math import gcd
from itertools import permutations, product as iprod

with open('core.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "def construct_spike_sigma(m, seed=42):" in line:
        new_lines.append(line)
        new_lines.append("    if m % 2 == 0: return None\n")
        new_lines.append("    n, arc_s, pa = _build_sa3(m); nP = 6; rng = random.Random(seed)\n")
        new_lines.append("    # Robust heuristic for odd m: Fiber-uniform sigma(s) (constant over j)\n")
        new_lines.append("    # This space is only 6^m, tractable for small m.\n")
        new_lines.append("    def find_fiber_sigma(m):\n")
        new_lines.append("        for combo in iprod(range(nP), repeat=m):\n")
        new_lines.append("            sig = [combo[( (idx // (m*m)) + (idx % (m*m) // m) + (idx % m) ) % m] for idx in range(n)]\n")
        new_lines.append("            if _sa_score(sig, arc_s, pa, n) == 0: return combo\n")
        new_lines.append("        return None\n\n")
        new_lines.append("    combo = find_fiber_sigma(m)\n")
        new_lines.append("    if combo:\n")
        new_lines.append("        res = {}\n")
        new_lines.append("        for v in range(n):\n")
        new_lines.append("            i, rem = divmod(v, m*m); j, k = divmod(rem, m)\n")
        new_lines.append("            res[(i, j, k)] = _ALL_P3[combo[(i+j+k)%m]]\n")
        new_lines.append("        return res\n")
        new_lines.append("    return None # Fallback if 6^m fails (should not happen for m=3,5)\n\n")
        # Now skip the old implementation
        skip = True
    elif skip and "if cur_score == 0:" in line:
        skip = False
        continue # skip the rest of the old implementation
    elif not skip:
        new_lines.append(line)

# Let's just rewrite the whole construct_spike_sigma function.
