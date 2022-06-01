from .hash_utils import FLUSH_INTERVAL, md5_hash
import time

class singleHashTable:
    def __init__(self, hash_fn=md5_hash):
        self.hash_fn = hash_fn
<<<<<<< HEAD
        self.nodes = []
        self.flush_interval = FLUSH_INTERVAL

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
    # public method called by proxy          
    def flush_cache(self):
        print(f"Flush the traditional hash ring at {time.ctime()}")
        timestamp = time.time() - self.flush_interval
        self.flush(timestamp)

    def get_node_idx(self, key):
        print(f"num of nodes: {len(self.nodes)}")
        return self.hash_fn(key) % len(self.nodes)
    
    # def get_node_meta(self, node_name):
    #     if node_name not in self.nodes:
    #         return None
    #     return self.nodes[node_name]

    # def handle_heartbeat(self, node_name):
    #     node_meta = self.get_node_meta(node_name)
    #     if node_meta is not None:
    #         node_meta["lastHeartbeat"] = time.time()
    #     else:
    #         # Add new node 
    #         print(f"Add a new node: {node_name}")
    #         self.add_node(node_name)
=======
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
>>>>>>> a14098c0fb6dcfdad8b1d1ffa81e0ffc5154eb24
