from hashlib import md5
from .hash_utils import md5_hash

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

    def get_node_meta(self, node_name):
        if node_name not in self._nodes:
            return None
        return self._nodes[node_name]

    def flush(self, time_stamp):
        for key in self._nodes:
            node_meta = self._nodes[key]
<<<<<<< HEAD
            if node_meta["lastHeartbeat"] < time_stamp:
=======
            if node_meta["lastHeartbeat"] is None or node_meta["lastHeartbeat"] < time_stamp:
>>>>>>> a14098c0fb6dcfdad8b1d1ffa81e0ffc5154eb24
                self.remove_node(node_meta["nodename"])
