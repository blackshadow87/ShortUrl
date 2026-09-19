import string
from math import gcd

import config

ALPHABET = string.ascii_letters + string.digits
BASE = len(ALPHABET)
LENGTH = config.CODE_LENGTH
SPACE = BASE**LENGTH
MULT = 1_000_000_007

assert gcd(MULT, SPACE) == 1, f"MULT должен быть взаимно прост с SPACE = {SPACE}"


def encode_id(identifier: int) -> str:
    if not 0 <= identifier < SPACE:
        raise ValueError(f"identifier вне диапазона [0, {SPACE - 1}]: {identifier}")
    x = identifier * MULT % SPACE
    chars = []
    for _ in range(LENGTH):
        x, digit = divmod(x, BASE)
        chars.append(ALPHABET[digit])
    return "".join(reversed(chars))