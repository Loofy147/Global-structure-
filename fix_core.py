import re

with open("core.py", "r") as f:
    content = f.read()

# Fix h2_uni condition for k % 2 == 1 (Parity obstruction)
new_content = content.replace(
    'h2_uni = (phi_m > 0 and all(r % 2 == 1 for r in cp)) and (k % 2 == 1) and (m % 2 == 0)',
    'h2_uni = (phi_m > 0 and all(r % 2 == 1 for r in cp)) and (k % 2 != 0) and (m % 2 == 0)'
)

# sol_lb fix: sol_lb should be cb**(k-1) * phi_m only if r_count > 0 and not h2_uni
# Currently: sol_lb = phi_m * (cb**(k-1)) if (not h2_uni and r_count > 0) else 0
# We need to ensure r_count is calculated correctly even if h2_uni is true (but then sol_lb is 0)

with open("core.py", "w") as f:
    f.write(new_content)
print("core.py patched.")
