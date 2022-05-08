from .consistent_hashing import ConsistentHashing

class HashRing:
    def __init__(self, nodes=[], hash_fn=None, vnodes=100, weight_fn=None):
        """
        Create a new hash ring.

        Parameters
        ----------
        nodes : list, optional
            the nodes used to create the ring, by default []
        hash_fn : _type_, optional
            a callable function to hash keys, by default None
        vnodes : int, optional
            the default number of virtual nodes per node, by default 100
        weight_fn : _type_, optional
            a callable function to calculate the node's weight, by default None
        """
        self.nodes = nodes
        self.vnodes = vnodes
        self.chashing = ConsistentHashing()
        self.chashing.setup(nodes)


