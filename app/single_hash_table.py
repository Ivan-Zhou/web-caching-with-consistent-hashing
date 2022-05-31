from .hash_utils import FLUSH_INTERVAL, md5_hash
import time

class singleHashTable:
    def __init__(self, hash_fn=md5_hash):
        self.hash_fn = hash_fn
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
