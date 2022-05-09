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
        self.cons_hash = ConsistentHashing()
        self.cons_hash.setup(nodes)


    def get(self, key):
        pass

    def __getitem__(self, key):
        return self._get(key, "instance")

    def _get(self, key, item):
        """
        Get the item from the node that is responsible for the key.
        The node with the nearest to the right side of the key is chosen

        Parameters
        ----------
        key : _type_
            _description_
        item : _type_
            _description_
        """
        pos = self._get_pos(key)


    def _configure_nodes(self, nodes):
        """
        parse and set up the given nodes

        Parameters
        ----------
        nodes : list
            nodes used to create the ring
        """
        assert isinstance(nodes, list), "nodes must be a list!"
        for node in nodes:
            meta = {
                "hostname": node,
                "instance": None,
                "nodename": node,
                "port": None,
                "vnode": self.vnodes,
                "weight": 1,
            }
            self.runtime._nodes[node] = meta


