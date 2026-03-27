with open("core.py", "r") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if "canon = None" in line:
        out.append("    mid = m - (k - 1)\n")
        out.append("    canon = ((1,)*(k-1) + (mid,)) if (mid > 0 and math.gcd(mid,m)==1) else (r_tuples[0] if r_count>0 else None)\n")
        skip = True
        continue
    if skip and "canon =" in line:
        skip = False
        continue
    if not skip:
        out.append(line)

with open("core.py", "w") as f:
    f.writelines(out)
