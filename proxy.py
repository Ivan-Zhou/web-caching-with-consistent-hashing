import socket
import sys
import signal
import threading

class Proxy:
	def __init__(self, config):
		# Shutdown on Ctrl+C
	    signal.signal(signal.SIGINT, self.shutdown) 

	    # Create a TCP socket
	    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	    # Re-use the socket
	    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	    # bind the socket to a public host, and a port   
	    self.serverSocket.bind(('myth56.stanford.edu', 30657))
	    
	    self.serverSocket.listen(1) # become a server socket
	    self.__clients = {}
    
    def service_request(self):

    	while True:

		    # Establish the connection
		    (clientSocket, client_address) = self.serverSocket.accept() 
		    
		    d = threading.Thread(name=self._getClientName(client_address), 
		    target = self.proxy_thread, args=(clientSocket, client_address))
		    d.setDaemon(True)
		    d.start()