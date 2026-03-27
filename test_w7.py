from core import extract_weights

m, k = 3, 3
w = extract_weights(m, k)
expected = 648
print(f"m={m}, k={k}: W7={w.sol_lb}, Expected={expected}")
if w.sol_lb == expected:
    print("W7 formula verified for m=3!")
else:
    print("W7 formula verification FAILED.")

m, k = 4, 3
w = extract_weights(m, k)
print(f"m={m}, k={k}: W7={w.sol_lb}")
