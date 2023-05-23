import random
import string
from typing import List

def random_reference(length: int) -> str:
    charset = string.ascii_uppercase + string.digits
    random_chars = (random.choice(charset) for _ in range(length))
    return ''.join(random_chars)

def generate_random_reference_list_by_limit(limit: int) -> List[str]:
    unique_codes = set()
    while len(unique_codes) < limit:
        code = random_reference(20)
        unique_codes.add(code)
    return list(unique_codes)
