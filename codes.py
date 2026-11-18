import string
import secrets

ALPHABET = string.ascii_letters + string.digits


def generate_code(length: int) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))
