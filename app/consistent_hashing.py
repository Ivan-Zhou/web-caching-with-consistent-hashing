from collections import Counter
from hashlib import md5


def md5_hash(key):
    """
    Returns the md5 hash of the key.
    """
    return int(md5(str(key).encode('utf-8')).hexdigest(), 16)


class ConsistentHashing:
    def __init__(self, hash_fn=md5_hash):
        if hasattr(hash_fn, "__call__"):
            raise TypeError("hash_fn must be a function")
        self.hash_fn = hash_fn
        self._distribution = Counter()
        self._ring = {}
        self._keys = []
        self._nodes = {}

    def hash_key(self, key):
        return self.hash_fn(key)

    def setup(self, nodes):
        """
        Setup the hash ring with the given nodes and virtual nodes.
        """
        for node_name, node_meta in nodes:
            n_vnodes = node_meta["vnodes"] * node_meta["weight"]
            self._distribution[node_name] = n_vnodes
            for vnode_idx in range(n_vnodes):
                vnode_key = self.hash_key(f"{node_name}-{vnode_idx}")
                self._ring[vnode_key] = node_name
        self._keys = sorted(self._ring.keys())
