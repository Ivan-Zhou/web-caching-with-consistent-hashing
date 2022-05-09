from bisect import bisect

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
        self._configure_nodes(nodes)
        self.cons_hash.setup()

    def get(self, key):
        return self._get(key, "dict")

    def _get(self, key, item):
        """
        Get the item from the node that is responsible for the key.
        The node with the nearest to the right side of the key is chosen

        Parameters
        ----------
        key : _type_
            the key to get the item for
        item : str
            the item to get
        """
        assigned_pos = self._get_pos(key)
        if item == "pos":
            return assigned_pos

        assigned_key = self.cons_hash._keys[assigned_pos]
        nodename = self.cons_hash._ring[assigned_key]

        if item == "dict":
            return self.cons_hash._nodes[nodename]

        if item == "nodename":
            return nodename

        if item == "tuple":
            return (assigned_pos, nodename)

        node = self.cons_hash._nodes[nodename]
        if item.isin(node.keys()):
            return node[item]
        raise KeyError(f"{item} is not supported in _get()!")

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
                "vnodes": self.vnodes,
                "weight": 1,
            }
            self.cons_hash._nodes[node] = meta

    def _get_pos(self, key):
        """
        Locate the node index assigned for the given key.
        The position should be the nearest node to the right side
        of the hash of the given key.
        """
        key_hash = self.cons_hash.hash_key(key)
        # returns an insertion point which comes after (to the right of) any
        # existing entries of key_hash in existing keys.
        pos = bisect(self.cons_hash._keys, key_hash)
        if pos == len(self.cons_hash._keys):
            return 0
        return pos

    def get_node(self, key):
        return self._get(key, "nodename")
