from .hash_utils import FLUSH_INTERVAL, md5_hash
import time

class singleHashTable:
    def __init__(self, hash_fn=md5_hash):
        self.hash_fn = hash_fn
        self.nodes = {}

    def get_node(self, key):
        if not self.nodes:
            return None
        return list(self.nodes.values())[self.get_node_idx(key) % len(self.nodes)]

    def add_node(self, node):
        if node["nodename"] not in self.nodes:
            self.nodes[node["nodename"]] = node

    def remove_node(self, nodename):
        if not self.nodes:
            return
        if nodename in self.nodes:
            self.nodes.pop(nodename, None)

    def flush(self, time_stamp):
        for node_meta in self.nodes:
            if node_meta["lastHeartbeat"] < time_stamp:
                self.remove_node(node_meta["nodename"])

    def get_node_idx(self, key):
        return self.hash_fn(key) % len(self.nodes)

    def handle_heartbeat(self, node_name):
        """
        Handle a heartbeat message. Update the lastHeartbeat time in the meta
        data associated with node with "node_name". Do nothing if no such node
        exists (e.g. the heartbeat message arrives too late due to network delays
        and the node has already been deleted due to being inactive.

        Parameters
        ----------
        node_name : str
            name identifying the node.
        """
        if node_name in self.nodes:
            self.nodes[node_name]["lastHeartbeat"] = time.time()

    def flush(self, time_stamp):
        for nodename in self.nodes.copy():
            node_meta = self.nodes[nodename]
            if node_meta["lastHeartbeat"] is None or node_meta["lastHeartbeat"] < time_stamp:
                self.remove_node(node_meta["nodename"])
