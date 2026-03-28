import re

with open("core.py", "r") as f:
    content = f.read()

new_spike_impl = """
def construct_spike_sigma(m, seed=42):
    if m % 2 == 0: return None
    identity = (0, 1, 2); swap12 = (0, 2, 1); swap01 = (1, 0, 2)
    def swap02(p): return (p[2], p[1], p[0])

    P = [identity] * (m - 2) + [swap12, swap01]
    res = {}
    for s in range(m):
        for j in range(m):
            if j == 0 and s != m - 2:
                res[(s, j)] = swap02(P[s])
            else:
                res[(s, j)] = P[s]
    return res
"""

# Replace the old construct_spike_sigma
pattern = r"def construct_spike_sigma\(m, seed=42\):.*?return None"
content = re.sub(pattern, new_spike_impl, content, flags=re.DOTALL)

with open("core.py", "w") as f:
    f.write(content)
print("core.py updated with deterministic Spike construction.")
