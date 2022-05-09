from app.hash_ring import HashRing


def main():
    # create a consistent hash ring of 3 nodes of weight 1
    hash_ring = HashRing(nodes=["node1", "node2", "node3"])

    # get the node name for the 'coconut' key
    test_url = "https://www.scs.stanford.edu/22sp-cs244b/"
    target_node = hash_ring.get_node("coconut")
    print(f"{test_url} is assigned to {target_node}")


if __name__ == "__main__":
    main()
