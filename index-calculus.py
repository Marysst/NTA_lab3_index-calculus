import random
import math
import time
from typing import List, Dict, Optional


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    sqrt_n = int(math.sqrt(n))
    i = 5
    while i <= sqrt_n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
