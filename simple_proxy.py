import sys
import signal
import _thread
import threading
import time
import socket
from utils import get_master_address, get_cache_port, parse_request_info, MAX_CONN, RECV_SIZE
from app import HashRing, FLUSH_INTERVAL, singleHashTable
from heartbeat import HEART_BEAT_INTERVAL


# socketToClient talks to browsers
# socketToOrigin talks to origin

class SimpleProxy:
    def __init__(self, useConsistentCaching = True):
        try:
            # Create a TCP socket
            self.socketToClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Re-use the socket
            self.socketToClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # bind the socket to a public host, and a port
            master_address = get_master_address()
            self.socketToClient.bind(("", master_address["port"]))

            self.socketToClient.listen(MAX_CONN) # become a proxy socket
      

        except Exception as e:
            print(f"Error occured on Proxy init: {e}")
            exit()

    def request_handler(self, clientSocket, clientAddr, clientData):
        # if POST (or other), do the process of sending request to origin
        requestInfo = parse_request_info(clientAddr, clientData)
        print(f"Sending request to origin server {requestInfo['server_url']}")

                # create server socket (socket to talk to origin server)
        socketToOrigin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
        socketToOrigin.send(requestInfo["client_data"])
        print("receiving reply from origin server")

     
        reply = socketToOrigin.recv(RECV_SIZE)
        print("FETCH origin, sending reply to client")
        while len(reply):
            clientSocket.send(reply)
            reply = socketToOrigin.recv(RECV_SIZE)
            # print(str.encode(reply))

        clientSocket.send(str.encode("\r\n\r\n"))
        print("Finished sending reply to client for non-GET request")

        socketToOrigin.close()
        clientSocket.close()
        
                



    def service_requests(self):
        while True:
            try:
                # clientSocket is the socket on client side
                clientSocket, clientAddr = self.socketToClient.accept()
                clientData = clientSocket.recv(RECV_SIZE)
                self.request_handler(clientSocket, clientAddr,
                            str(clientData, encoding='utf-8', errors='ignore'))
               

            except KeyboardInterrupt:
                clientSocket.close()
                self.socketToClient.close()
                break



    def run(self):
        self.service_requests()
       


if __name__ == '__main__':
    proxy = SimpleProxy()
    proxy.run()





# import sys
# import signal
# import _thread
# import threading

# import socket
# from utils import get_master_address, get_cache_port, parse_request_info, MAX_CONN, RECV_SIZE
# from app import HashRing, singleHashTable, FLUSH_INTERVAL
# from heartbeat import HEART_BEAT_INTERVAL


# class Proxy:
#     def __init__(self):
#         try: 

#             # Create a TCP socket
#             self.proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#             # Re-use the socket
#             self.proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#             # bind the socket to a public host, and a port   
#             master_address = get_master_address()
#             self.proxySocket.bind(("", master_address["port"]))


#             self.proxySocket.listen(MAX_CONN) # become a proxy socket
#         except Exception as e:
#             print("Some error occured on init")
#             print(e)
#             self.proxySocket.close()
#             return


#     def request_handler(self, clientSocket, clientAddr, clientData):

#         # parse the get request
#         requestInfo = parse_request_info(clientAddr, clientData)

#         print("sending request to origin server")
#         print(clientData)
#         print("requestInfo:\n", requestInfo)

#         # create server socket (socket to talk to origin server)
#         serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         serverSocket.connect((requestInfo["server_url"], requestInfo["server_port"]))
#         serverSocket.send(requestInfo["client_data"])
#         print("receiving reply from origin server")
        
#         # get reply for server socket (origin server)
#         reply = serverSocket.recv(RECV_SIZE)
#         print("sending reply to client server")
#         while len(reply):
#             clientSocket.send(reply)
#             reply = serverSocket.recv(RECV_SIZE)
#         clientSocket.send(str.encode("\r\n\r\n"))
#         print("finished sending reply to client")
        
#         serverSocket.close()
#         clientSocket.close()



#     def service_requests(self):
#         while True:
#             try:
#                 clientSocket, clientAddr = self.proxySocket.accept() 
#                 clientData = clientSocket.recv(RECV_SIZE)
#                 print("recieved a request from ", clientAddr)
#                 _thread.start_new_thread(self.request_handler, (clientSocket, clientAddr, str(clientData, encoding='utf-8', errors='ignore')))
#             except KeyboardInterrupt:
#                     clientSocket.close()
#                     self.proxySocket.close()
#                     break


# proxy = Proxy()
# proxy.service_requests()
