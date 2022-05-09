from app.hash_ring import HashRing

TEST_URLS = [
    "https://www.scs.stanford.edu/22sp-cs244b/",
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.wikipedia.org",
    "https://www.amazon.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.github.com",
    "https://www.reddit.com",
    "https://www.quora.com",
]


def get_nodes_of_urls(hash_ring):
    for url in TEST_URLS:
        node = hash_ring.get_node(url)
        print(f"{url} is assigned to {node}")


def main():
    # create a consistent hash ring of 3 nodes of weight 1
    hash_ring = HashRing(nodes=["node1", "node2", "node3"])
    print(f"\nNodes in the ring: {hash_ring.nodes}")
    get_nodes_of_urls(hash_ring)

    # add three node
    for node in ["node4", "node5", "node6"]:
        hash_ring.add_node(node)
    print(f"\nNodes in the ring: {hash_ring.nodes}")
    get_nodes_of_urls(hash_ring)


if __name__ == "__main__":
    main()
