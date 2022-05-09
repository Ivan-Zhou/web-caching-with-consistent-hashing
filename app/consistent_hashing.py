from hashlib import md5


def md5_hash(key):
    """
    Returns the md5 hash of the key.
    """
    return int(md5(str(key).encode("utf-8")).hexdigest(), 16)


class ConsistentHashing:
    def __init__(self, hash_fn=md5_hash):
        self.hash_fn = hash_fn
        self.reset()

    def reset(self):
        self._ring = {}
        self._keys = []
        self._nodes = {}

    def hash_key(self, key):
        return self.hash_fn(key)

    def add_node(self, node_name, node_meta):
        for idx in range(node_meta["vnodes"]):
            vnode_key = self.hash_key(f"{node_name}-{idx}")
            self._ring[vnode_key] = node_name
        self._nodes[node_name] = node_meta
        self._keys = sorted(self._ring.keys())

    def remove_node(self, node_name):
        try:
            node_meta = self._nodes.pop(node_name)
        except Exception:
            raise KeyError(
                f"node '{node_name}' not found, available nodes: {self._nodes.keys()}"
            )
        else:
            for idx in range(node_meta["vnodes"]):
                vnode_key = self.hash_key(f"{node_name}-{idx}")
                del self._ring[vnode_key]
            self._keys = sorted(self._ring.keys())
