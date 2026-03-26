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
