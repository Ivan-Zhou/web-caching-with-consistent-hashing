from hashlib import md5

FLUSH_INTERVAL = 10

def md5_hash(key):
    """
    Returns the md5 hash of the key.
    """
    return int(md5(str(key).encode("utf-8")).hexdigest(), 16)

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

if __name__ == "__main__":
    hashTable = singleHashTable()

    name1 = "node1"
    name2 = "node2"
    meta1 = {
        "hostname": name1,
        "instance": None,
        "nodename": name1,
        "port": None,
        "vnodes": None,
        "lastHeartbeat": None,
    }

    meta2 = {
        "hostname": name2,
        "instance": None,
        "nodename": name2,
        "port": None,
        "vnodes": None,
        "lastHeartbeat": None,
    }

    hashTable.add_node(meta1)
    hashTable.add_node(meta2)
    print(hashTable.get_node("msg1"))
    print(hashTable.get_node("msg2"))
    print("removing node1")
    hashTable.remove_node(("node1"))
    print(hashTable.get_node("msg1"))
    print(hashTable.get_node("msg2"))

