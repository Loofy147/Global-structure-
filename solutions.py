"""
solutions.py — Hardcoded verified solutions for Claude's Cycles.

All solutions have been computationally verified (3 Hamiltonian cycles).
"""

from typing import Optional, List, Dict, Tuple

# m=4 verified solution (found via SA)
SOLUTION_M4_LIST = [1, 1, 5, 5, 1, 0, 0, 5, 2, 3, 3, 4, 3, 4, 4, 1, 1, 5, 1, 0, 2, 4, 3, 4, 2, 5, 4, 0, 5, 1, 0, 2, 1, 2, 2, 4, 1, 0, 4, 5, 5, 1, 0, 3, 1, 2, 5, 5, 3, 5, 4, 2, 2, 1, 1, 1, 1, 1, 5, 4, 5, 3, 1, 4]

_KNOWN = {4: SOLUTION_M4_LIST}

def get_solution(m: int) -> Optional[List[int]]:
    """Return the raw permutation index list for known m values."""
    return _KNOWN.get(m)

def known_m_values() -> List[int]:
    """Return sorted list of m values with hardcoded solutions."""
    return sorted(_KNOWN.keys())

# Z4xZ6 k=2 verified solution
# Coset choice (0, 1) -> sigma(i,j) = (0, 1) if (i+j)%2==0 else (1, 0)
SOLUTION_Z4X6 = {(i, j): ((0, 1) if (i+j)%2 == 0 else (1, 0)) for i in range(4) for j in range(6)}

def get_z4x6_solution():
    return SOLUTION_Z4X6

# S_3 solutions
SOLUTION_S3_K2 = {'generators': [(1, 0, 2), (0, 2, 1)], 'sigma': {'fiber0': (0, 1), 'fiber1': (1, 0)}}
SOLUTION_S3_K3 = {'generators': [(0, 2, 1), (1, 0, 2), (2, 1, 0)], 'sigma': {'fiber0': (0, 1, 2), 'fiber1': (1, 2, 0)}}

def get_s3_solutions():
    return {"k2": SOLUTION_S3_K2, "k3": SOLUTION_S3_K3}

# Z_2^4 Hamiltonian Decomposition (Full Coordinate)
SOLUTION_Z2K4 = [2, 12, 3, 19, 16, 9, 12, 1, 7, 3, 14, 17, 21, 14, 9, 8]
def get_z2k4_solution(): return SOLUTION_Z2K4
