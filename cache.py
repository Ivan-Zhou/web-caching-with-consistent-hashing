import _thread
import socket
import os
from datetime import datetime, timedelta
from proxy import Proxy
CACHE_DIR = "./cache"

# how to pass requestInfo??
class Cache(Proxy):
    def __init__(self, requestInfo):
        super().__init__(self, requestInfo)
        
        
        

        # Make cache directory
        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for file in os.listdir(CACHE_DIR):
            os.remove(CACHE_DIR + "/" + file)


       
    # Check if the requested resource has been cached
    def check_if_cached(requestInfo):      
        if fileRequested.startswith("/"):
            fileRequested = fileRequested.replace("/", "", 1)

        cache_path = CACHE_DIR + "/" + fileRequested.replace("/", "__")

        if os.path.isfile(cachePath):
            return true, cachePath
        else:
            return false, cachePath

    # Check if the cache file is expired (>1d)
    def ifExpired(f):
        filePath = CACHE_DIR + "/" + f
        fileTime = datetime.fromtimestamp(path.getctime(filePath))
        return datetime.now() - fileTime > timedelta(days=1)

    #Clear cache when expired 
    def clearCache():
        #requestInfo is class variable
        cacheFiles = os.listdir(CACHE_DIR)
        for f in cacheFiles:
            if ifExpired(f):
                os.remove(CACHE_DIR + "/" + f)

    def fetch_from_cache(masterSocket, masterAddr):
        print("Fetching cache from " + cachePath + " to master " + masterAddr)
        file = open(cachePath, "rb")
        chunk = f.read(RECV_SIZE)
        while chunk:
            masterSocket.send(chunk)
            chunk = f.read(RECV_SIZE)
        f.close()

    def write_to_cache(masterSocket):
        print("Fetching cache from " + cachePath + " to master " + masterAddr)
        file = open(cachePath, "w+")
        while len(reply):
            client_socket.send(reply)
            f.write(str(reply, 'utf-8'))
            reply = server_socket.recv(RECV_SIZE)
        f.close()
        client_socket.send(str.encode("\r\n\r\n"))

    def fetch_from_origin(masterSocket, masterAddr, requestInfo):
        try: 
            # create server socket (socket to talk to origin server)
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.connect((requestInfo["server_url"], requestInfo["server_port"]))
            serverSocket.send(requestInfo["client_data"])
            print("receiving reply from origin server")
        
            # get reply for server socket (origin server)
            reply = serverSocket.recv(RECV_SIZE)
            print("sending reply to client server")
            while len(reply):
                masterSocket.send(reply)
                reply = serverSocket.recv(RECV_SIZE)
            masterSocket.send(str.encode("\r\n\r\n"))
            print("finished sending reply to client")
        
            serverSocket.close()
          
        
        except Exception as e:
            server_socket.close()
            print(e)
        return
       

    def request_handler():
        # masterSocket, masterAddr, requestInfo
        Proxy.service_requests(self)
        ifCached, cachePath = check_if_cached(requestInfo["total_url"])
        requestInfo["if_cached"] = ifCached
        requestInfo["cache_path"] = cachePath
        # clear expired cache before handling new request
        clearCache()

        if requestInfo["if_cached"]:
            fetch_from_cache(masterSocket, masterAddr, requestInfo)
        else:
            fetch_from_origin(masterSocket, masterAddr, requestInfo)

cache = Cache()
cache.request_handler()