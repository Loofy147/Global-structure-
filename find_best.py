import re
with open("record_search.log", "r") as f:
    best = 999
    for line in f:
        m = re.search(r"P1-k4: (\d+)", line)
        if m:
            s = int(m.group(1))
            if s < best: best = s
    print(best)
