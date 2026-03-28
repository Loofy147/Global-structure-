from core import construct_spike_sigma, verify_sigma

for m in [3, 5, 7, 9]:
    sig = construct_spike_sigma(m)
    ok = verify_sigma(sig, m)
    print(f"m={m} core.construct_spike_sigma verified: {ok}")
