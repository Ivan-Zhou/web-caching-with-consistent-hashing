from .proxy import Proxy
from ./app/hash_ring import HashRing

class masterServer(Proxy):
    def __init__(self, flush_interval = 10000):
        super.__init__()
        self.flush_interval = flush_interval
        self.hash_ring = HashRing()

    def handle_heartbeat(self, node_name):
        """
          Handle a heartbeat message.
          A cache server can register itself in the hash ring
          by sending a heartbeat message.

          Parameters
          ----------
          node_name : str
              name identifying the node.
        """
        self.hash_ring.handle_heartbeat(node_name)

    def flush(self):
        """
          Remove inactive nodes. Called every self.flush_interval
          milliseconds.
        """
        self.hash_ring.flush()

    def get_node_name_for_hashkey(self, hash_key):
        """
          Get the nodename for a hash key.
          Parameters
          ----------
          hash_key : str
          Return
          ----------
          node_name : str
        """
        node_name = self.hash_ring.get_node(hash_key)
        return node_name

    def server(self):
        pass