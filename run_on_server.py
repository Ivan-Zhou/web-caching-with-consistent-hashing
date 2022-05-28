import sys
import signal
import _thread
import threading

import socket
from utils import get_master_address, get_cache_port, parse_request_info, MAX_CONN, RECV_SIZE
from app import HashRing, FLUSH_INTERVAL
from heartbeat import HEART_BEAT_INTERVAL

from test.utils import get_test_urls

# socketToClient talks to browsers
# socketToOrigin talks to origin

class Server:
    def __init__(self):
        try:

            # Create a TCP socket
            self.socketToClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Re-use the socket
            self.socketToClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # bind the socket to a public host, and a port
            master_address = get_master_address()
            self.socketToClient.bind(("", master_address["port"]))

            self.socketToClient.listen(MAX_CONN) # become a proxy socket
            self.hash_ring = HashRing()
            self.threads = []
        except Exception as e:
            print(f"Error occured on Proxy init: {e}")
            exit()

    def request_handler(self, clientSocket, clientAddr, clientData):
        if clientData == "heartbeat":
            # print(f"Receive a heartbeat message from a Cache Server {clientAddr}")
            self._handle_heartbeat(clientAddr)

        # clientSocket.close()

    def request_get(self, url):
        socketToCache = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cacheIP = self.get_node_name_for_hashkey(url)
            cachePort = get_cache_port()

            socketToCache.connect((cacheIP, cachePort))
            # send all of clientData to cache server
            # only needs one send, not a chunked send


            socketToCache.send(clientData.encode())

            # socketToCache.send(requestInfo["client_data"])
            print("receiving reply from cache server")

            # get reply for cache
            reply = socketToCache.recv(RECV_SIZE)
            # For the reply from the cache, need to do in a while loop
            # because response can be big
            while len(reply):
                print(f"reply from cache: {reply}")
                reply = socketToCache.recv(RECV_SIZE)
        except Exception as e:
            print(f"Fail to connect to cache server: {e}")

    def service_requests(self):
        while True:
            try:
                # clientSocket is the socket on client side
                clientSocket, clientAddr = self.socketToClient.accept()
                clientData = clientSocket.recv(RECV_SIZE)

                # is this a good idea? 2 threads might contact the same
                # cache for the same data at once

                # maybe, shouldn't be multi-threaded
                # we can multi thread to different caches,
                # but for a given cache should be serial
                t = threading.Thread(
                    target=self.request_handler,
                    args=(clientSocket, clientAddr,
                            str(clientData, encoding='utf-8', errors='ignore')))
                self.threads.append(t)
                t.start()

            except KeyboardInterrupt:
                # join all the threads
                for t in self.threads:
                    t.join()

                clientSocket.close()
                self.socketToClient.close()
                break

    def _handle_heartbeat(self, clientAddr):
        # use the Host Address as the nodename
        self.hash_ring.handle_heartbeat(node_name=clientAddr[0])

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

    def _flush(self):
        """
          Remove inactive nodes. Called every self.flush_interval
          milliseconds.
        """
        self.hash_ring.flush()

    def run_test(self):
        test_urls = get_test_urls(n=3)
        for url in test_urls:
            print(f"Process url: {url}")
            self.request_get(url)
        print("finished test!")

    def run(self):
        """
        Run scheduled tasks in thread to maintain cache servers
        """
        t1 = threading.Thread(target=self.service_requests)
        t2 = threading.Timer(FLUSH_INTERVAL, self._flush)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == '__main__':
    server = Server()
    server.run()
