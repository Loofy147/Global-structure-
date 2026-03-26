import time
from typing import Any, Dict, List, Optional, Tuple, Set, Union
from enum import Enum
from dataclasses import dataclass
from core import extract_weights, Weights, verify_sigma, solve, PRECOMPUTED

G_="\033[92m";R_="\033[91m";Y_="\033[93m";B_="\033[94m";W_="\033[97m";D_="\033[2m";Z_="\033[0m"

class Status(Enum):
    SOLVED = "SOLVED"
    OPEN = "OPEN"
    IMPOSSIBLE = "IMPOSSIBLE"
    FEASIBLE = "FEASIBLE"

@dataclass
class Domain:
    name: str
    G: str
    k: int
    m: int
    status: Status
    description: str

class Engine:
    def __init__(self):
        self._domains: Dict[str, Domain] = {}
        self._cache = {}

    def register(self, domain: Domain):
        self._domains[domain.name] = domain
        return self

    def run(self, m: int, k: int=3, verbose: bool=False):
        t0 = time.perf_counter()
        w = extract_weights(m, k)

        # Determine status
        if w.h2_blocks:
            status = "IMPOSSIBLE (Uniform)" if k == 3 and m % 2 == 0 else "BLOCKED"
        elif w.r_count > 0:
            status = "SOLVED (Uniform)"
        else:
            status = "OPEN"

        elapsed = (time.perf_counter() - t0)*1000
        res = f"({m},{k}) {status:<25} W4={w.h1_exact} W7={w.sol_lb:,} ({elapsed:.1f}ms)"
        self._cache[(m,k)] = res
        return res

    def print_space(self, m_max=12, k_max=7):
        print(f"\n{W_}CLASSIFYING SPACE m=2..{m_max}, k=2..{k_max}{Z_}")
        print(f"  m\k " + " ".join(f"k={k:<2}" for k in range(2, k_max+1)))
        for m in range(2, m_max+1):
            row = f"  {m:>2}  "
            for k in range(2, k_max+1):
                w = extract_weights(m, k)
                if w.h2_blocks:
                    if k == 3 and m % 2 == 0: row += f" {R_}✗{Z_}  "
                    else: row += f" {Y_}?{Z_}  "
                elif w.r_count > 0: row += f" {G_}✓{Z_}  "
                else: row += f" {Y_}?{Z_}  "
            print(row)

if __name__ == "__main__":
    e = Engine()
    for m,k in [(3,3),(4,3),(4,4),(5,3),(6,3),(7,3)]:
        print(f"  {e.run(m,k)}")
    e.print_space()
