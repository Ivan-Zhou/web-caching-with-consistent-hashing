from .hash_utils import FLUSH_INTERVAL, md5_hash
import time

class singleHashTable:
    def __init__(self, hash_fn=md5_hash):
        self.hash_fn = hash_fn
        self.nodes = {}

    def get_node(self, key):
        if not self.nodes:
            return None
        node_idx = self.get_node_idx(key)
        return list(self.nodes.values())[node_idx]["nodename"]  
        # return list(self.nodes.values())[self.get_node_idx(key) % len(self.nodes)]

    def add_node(self, nodename):
        if nodename not in self.nodes:
            node = {
                "nodename": nodename,
                "lastHeartbeat": None,
                }
            self.nodes[nodename] = node
        
       

    def remove_node(self, nodename):
        if not self.nodes:
            return
        if nodename in self.nodes:
            self.nodes.pop(nodename, None)

    def get_node_idx(self, key):
        return self.hash_fn(key) % len(self.nodes)

    def handle_heartbeat(self, node_name):
        if node_name in self.nodes:
            self.nodes[node_name]["lastHeartbeat"] = time.time()
        else:
            # Add new node 
            print(f"Add a new node: {node_name}")
            self.add_node(node_name)

    def flush_(self, time_stamp):
        for nodename in self.nodes.copy():
            node_meta = self.nodes[nodename]
            if node_meta["lastHeartbeat"] is None or node_meta["lastHeartbeat"] < time_stamp:
                self.remove_node(node_meta["nodename"])
    # public method called by proxy          
    def flush(self):
        # print(f"Flush the traditional hash ring at {time.ctime()}")
        timestamp = time.time() - FLUSH_INTERVAL
        self.flush_(timestamp)