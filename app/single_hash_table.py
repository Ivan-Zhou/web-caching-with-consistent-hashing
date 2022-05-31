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
        # TODO: should we change to python dict for implementation? How does it affect the performance.
        for node_meta in self.nodes:
            if node_meta["nodename"] == "node_name":
                node_name["lastHeartbeat"] = time.time()

        # node_meta = self.cons_hash.get_node_meta(node_name)
        # if node_meta is not None:
        #     node_meta["lastHeartbeat"] = time.time()
        # else:
        #     # Add new node to consistent caching
        #     print(f"Add a new node to consistent caching: {node_name}")
        #     self.add_node(node_name)

    def flush(self, time_stamp):
        for node_meta in self.nodes:
            if node_meta["lastHeartbeat"] < time_stamp:
                self.remove_node(node_meta["nodename"])
