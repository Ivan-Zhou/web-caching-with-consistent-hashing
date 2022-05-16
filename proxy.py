import socket
import sys
import signal
import _thread
import threading

from utils import get_master_address
from app import HashRing, FLUSH_INTERVAL
from heartbeat import HEART_BEAT_INTERVAL

MAX_CONN = 1
RECV_SIZE = 4096

class Proxy:
    def __init__(self):
        try:

            # Create a TCP socket
            self.proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Re-use the socket
            self.proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # bind the socket to a public host, and a port
            master_address = get_master_address()
            self.proxySocket.bind((master_address["host"], master_address["port"]))

            self.proxySocket.listen(MAX_CONN) # become a proxy socket
            self.hash_ring = HashRing()
        except Exception as e:
            print(f"Error occured on Proxy init: {e}")
            self.proxySocket.close()
            return


    def request_handler(self, clientSocket, clientAddr, clientData):
        if clientData == "heartbeat":
            print(f"Receive a heartbeat message from a Cache Server {clientAddr}")
            self._handle_heartbeat(clientAddr)
        else:
            requestInfo = self.parse_request_info(clientAddr, clientData)
            print(f"Sending request to origin server {requestInfo['server_url']}")
            # create server socket (socket to talk to origin server)
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.connect((requestInfo["server_url"], requestInfo["server_port"]))
            serverSocket.send(requestInfo["client_data"])
            print("receiving reply from origin server")

            # get reply for server socket (origin server)
            reply = serverSocket.recv(RECV_SIZE)
            print("sending reply to client server")
            while len(reply):
                clientSocket.send(reply)
                reply = serverSocket.recv(RECV_SIZE)
            clientSocket.send(str.encode("\r\n\r\n"))
            print("finished sending reply to client")

            serverSocket.close()
        clientSocket.close()

    '''
    This function processes the client data and separates out the essential information
    '''
    def parse_request_info(self, client_addr, client_data):
        try:
            lines = client_data.splitlines()
            while lines[len(lines)-1] == '':
                lines.remove('')
            first_line_tokens = lines[0].split()
            url = first_line_tokens[1]

            url_pos = url.find("://")
            if url_pos != -1:
                protocol = url[:url_pos]
                url = url[(url_pos+3):]
            else:
                protocol = "http"

            # get port if any
            # get url path
            port_pos = url.find(":")
            path_pos = url.find("/")
            if path_pos == -1:
                path_pos = len(url)


            # change request path accordingly
            if port_pos==-1 or path_pos < port_pos:
                server_port = 80
                server_url = url[:path_pos]
            else:
                server_port = int(url[(port_pos+1):path_pos])
                server_url = url[:port_pos]

            # build up request for server
            first_line_tokens[1] = url[path_pos:]
            lines[0] = ' '.join(first_line_tokens)
            client_data = "\r\n".join(lines) + '\r\n\r\n'

            return {
                "server_port" : server_port,
                "server_url" : server_url,
                "total_url" : url,
                "client_data" : str.encode(client_data),
                                "protocol" : protocol,
                "method" : first_line_tokens[0],
            }

        except Exception as e:
            print(e)
            return None

    def service_requests(self):
        while True:
            try:
                clientSocket, clientAddr = self.proxySocket.accept()
                clientData = clientSocket.recv(RECV_SIZE)
                _thread.start_new_thread(self.request_handler, (clientSocket, clientAddr, str(clientData, encoding='utf-8', errors='ignore')))
            except KeyboardInterrupt:
                    clientSocket.close()
                    self.proxySocket.close()
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
