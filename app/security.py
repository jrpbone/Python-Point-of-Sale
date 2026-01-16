import base64
import hashlib
import hmac
import os

HASH_PREFIX = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 200_000
SALT_BYTES = 16


def hash_pin(pin, iterations=DEFAULT_ITERATIONS):
    if pin is None:
        raise ValueError("pin is required")
    salt = os.urandom(SALT_BYTES)
    derived = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), salt, iterations)
    salt_b64 = base64.b64encode(salt).decode("ascii")
    derived_b64 = base64.b64encode(derived).decode("ascii")
    return f"{HASH_PREFIX}${iterations}${salt_b64}${derived_b64}"


def verify_pin(pin, stored):
    parsed = _parse_hash(stored)
    if not parsed:
        return False
    iterations, salt, expected = parsed
    derived = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(derived, expected)


def is_hashed(stored):
    return _parse_hash(stored) is not None


def _parse_hash(stored):
    if not stored:
        return None
    parts = stored.split("$")
    if len(parts) != 4:
        return None
    if parts[0] != HASH_PREFIX:
        return None
    try:
        iterations = int(parts[1])
        salt = base64.b64decode(parts[2].encode("ascii"))
        digest = base64.b64decode(parts[3].encode("ascii"))
    except (ValueError, TypeError, base64.binascii.Error):
        return None
    return iterations, salt, digest
