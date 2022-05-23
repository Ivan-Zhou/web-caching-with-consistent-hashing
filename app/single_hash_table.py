from hashlib import md5

FLUSH_INTERVAL = 10

def md5_hash(key):
    """
    Returns the md5 hash of the key.
    """
    return int(md5(str(key).encode("utf-8")).hexdigest(), 16)

class singleHashTable:
    def __init__(self, hash_fn=md5_hash, flush_interval = FLUSH_INTERVAL):
        self.hash_fn = hash_fn
        self.nodes = []

    def get_node(self, key):
        return self.nodes[key % len(self.nodes)]

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, nodename):
        self.nodes.pop(self._get_node_idx(nodename))

    def flush(self, time_stamp):
        for node_meta in self.nodes:
            if node_meta["lastHeartbeat"] < time_stamp:
                self.remove_node(node_meta["nodename"])

    def _get_node_idx(selfs, nodename):
        return self.hash_fn(nodename) % len(self.nodes)



