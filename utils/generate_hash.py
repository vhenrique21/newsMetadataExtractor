from hashlib import sha256


def generate_hash(input: str) -> str:
    random_string: bytes = input.encode("utf-8")
    random_hash: str = sha256(random_string).hexdigest()
    return random_hash
