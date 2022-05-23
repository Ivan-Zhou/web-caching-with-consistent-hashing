from app.single_hash_table import singleHashTable

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
