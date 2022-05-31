from .hash_utils import FLUSH_INTERVAL, md5_hash

class singleHashTable:
    def __init__(self, hash_fn=md5_hash):
        self.hash_fn = hash_fn
        self.nodes = []

    def get_node(self, key):
        return self.nodes[self.get_node_idx(key) % len(self.nodes)]

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, nodename):
        # Note this does not check if nodename is in self.nodes!
        self.nodes.pop(self.get_node_idx(nodename))

    def flush(self, time_stamp):
        for node_meta in self.nodes:
            if node_meta["lastHeartbeat"] < time_stamp:
                self.remove_node(node_meta["nodename"])

    def get_node_idx(self, key):
        return self.hash_fn(key) % len(self.nodes)
