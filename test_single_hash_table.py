from app.single_hash_table import singleHashTable

hashTable = singleHashTable()

name1 = "node1"
name2 = "node2"
<<<<<<< HEAD
=======
name3 = "node3"
>>>>>>> a14098c0fb6dcfdad8b1d1ffa81e0ffc5154eb24
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

<<<<<<< HEAD
hashTable.add_node(meta1)
hashTable.add_node(meta2)
print(hashTable.get_node("msg1"))
print(hashTable.get_node("msg2"))
print("removing node1")
hashTable.remove_node(("node1"))
print(hashTable.get_node("msg1"))
print(hashTable.get_node("msg2"))
=======
meta3 = {
    "hostname": name3,
    "instance": None,
    "nodename": name3,
    "port": None,
    "vnodes": None,
    "lastHeartbeat": None,
}

hashTable.add_node(meta1)
hashTable.add_node(meta2)
hashTable.add_node(meta3)
print(hashTable.get_node("msg1"))
print(hashTable.get_node("msg2"))
print(hashTable.get_node("msg3"))
print(hashTable.get_node("msg4"))
print(hashTable.get_node("msg5"))
print(hashTable.nodes)
print("removing node2")
hashTable.remove_node(("node2"))
print(hashTable.get_node("msg1"))
print(hashTable.get_node("msg2"))
print(hashTable.get_node("msg3"))
print(hashTable.get_node("msg4"))
print(hashTable.get_node("msg5"))
print(hashTable.nodes)

hashTable.handle_heartbeat("node3")

hashTable.flush(1)
print(hashTable.nodes)

>>>>>>> a14098c0fb6dcfdad8b1d1ffa81e0ffc5154eb24
