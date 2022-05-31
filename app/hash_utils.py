from hashlib import md5

FLUSH_INTERVAL = 10  # seconds

def md5_hash(key):
    """
    Returns the md5 hash of the key.
    """
    return int(md5(str(key).encode("utf-8")).hexdigest(), 16)