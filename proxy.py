import socket
import sys
import signal
import _thread
import threading

from utils import get_master_address, parse_request_info
from app import HashRing, FLUSH_INTERVAL
from heartbeat import HEART_BEAT_INTERVAL

MAX_CONN = 1
RECV_SIZE = 4096

# socketToClient talks to browsers
# socketToOrigin talks to origin

class Proxy:
    def __init__(self):
        try:

            # Create a TCP socket
            self.socketToClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Re-use the socket
            self.socketToClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # bind the socket to a public host, and a port
            master_address = get_master_address()
            self.socketToClient.bind((master_address["host"], master_address["port"]))

            self.socketToClient.listen(MAX_CONN) # become a proxy socket
            self.hash_ring = HashRing()
        except Exception as e:
            print(f"Error occured on Proxy init: {e}")
            self.socketToClient.close()
            return

    
    def request_handler(self, clientSocket, clientAddr, clientData):
        if clientData == "heartbeat":
            print(f"Receive a heartbeat message from a Cache Server {clientAddr}")
            self._handle_heartbeat(clientAddr)
        else:
            requestInfo = parse_request_info(clientAddr, clientData)
            print(f"Sending request to origin server {requestInfo['server_url']}")
            # create server socket (socket to talk to origin server)
            socketToOrigin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
            socketToOrigin.send(requestInfo["client_data"])
            print("receiving reply from origin server")

            # get reply for server socket (origin server)
            reply = socketToOrigin.recv(RECV_SIZE)
            print("sending reply to client server")
            while len(reply):
                clientSocket.send(reply)
                reply = socketToOrigin.recv(RECV_SIZE)
            clientSocket.send(str.encode("\r\n\r\n"))
            print("finished sending reply to client")

            socketToOrigin.close()
        clientSocket.close()


    def service_requests(self):
        while True:
            try:
                # clientSocket is the socket on client side
                clientSocket, clientAddr = self.socketToClient.accept()
                clientData = clientSocket.recv(RECV_SIZE)
                _thread.start_new_thread(self.request_handler, (clientSocket, clientAddr, str(clientData, encoding='utf-8', errors='ignore')))
            except KeyboardInterrupt:
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
    proxy = Proxy()
    proxy.run()
