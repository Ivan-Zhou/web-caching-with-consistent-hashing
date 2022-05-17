import _thread
import socket
import os
from datetime import datetime, timedelta
from utils import parse_request_info
CACHE_DIR = "./cache"

# socketToMaster talks to master
# masterSocket is the socket in master which is used to talk to cache server

class Cache():
    def __init__(self, HOST, PORT):
        try:
            # Create a TCP socket
            self.socketToMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Re-use the socket
            self.socketToMaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.socketToMaster.bind(HOST, PORT)

            self.socketToMaster.listen(MAX_CONN) # become a cache socket
        
        except Exception as e:
            print(f"Error occured on Cache server init: {e}")
            self.socketToMaster.close()
            return
        

        self.cacheDict = {}

        #
        # {
        #   "www.google.com":
        #      {
        #          data: ["GET R", "EQUES", "T DAT", "A"],
        #          timestamp: "10:01 PM"
        #      } 
        # }
        #
        #
        server_run()
        
    
        # Make cache directory ??store in memory
        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        for file in os.listdir(CACHE_DIR):
            os.remove(CACHE_DIR + "/" + file)


       
    # Check if the requested resource has been cached
    def check_if_cached(cacheKey):  
        '''
        File version
        '''
        if cacheKey.startswith("/"):
            cacheKey = cacheKey.replace("/", "", 1)

        cachePath = CACHE_DIR + "/" + cacheKey.replace("/", "__")

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

 
# fetch from origin and write to cache
    def fetch_from_origin(masterSocket, masterAddr, requestInfo):
        try: 
            # create server socket (socket to talk to origin server)
            socketToOrigin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
            socketToOrigin.send(requestInfo["client_data"])
            print("receiving reply from origin server")
        
            # get reply for server socket (origin server)
            reply = socketToOrigin.recv(RECV_SIZE)
            f = open(cachePath, "w+")
            print("sending reply from cache to master server")
            while len(reply):
                masterSocket.send(reply)
                f.write(str(reply, 'utf-8'))
                reply = socketToOrigin.recv(RECV_SIZE)
                
            masterSocket.send(str.encode("\r\n\r\n"))
            print("finished sending reply to master server")
            f.close()
        
            socketToOrigin.close()
          
        except Exception as e:
            masterSocket.close()
            print(e)
        return

    def fetch_from_origin_mem(masterSocket, masterAddr, requestInfo):
        try: 
            # create server socket (socket to talk to origin server)
            socketToOrigin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
            socketToOrigin.send(requestInfo["client_data"])
            print("receiving reply from origin server")
        
            # get reply for server socket (origin server)
            reply = socketToOrigin.recv(RECV_SIZE)
            print("sending reply from cache to master server")
            while len(reply):
                masterSocket.send(reply)
                reply = socketToOrigin.recv(RECV_SIZE)
                
            masterSocket.send(str.encode("\r\n\r\n"))
            print("finished sending reply to master server")
            f.close()
        
            socketToOrigin.close()
          
        except Exception as e:
            masterSocket.close()
            print(e)
        return
       

        
         

    def server_run():
        while True:
            try:
                masterSocket, masterAddr = self.socketToMaster.accept()
                masterData = masterSocket.recv(RECV_SIZE)
                _thread.start_new_thread(self.request_handler, (masterSocket, masterAddr, str(masterData, encoding='utf-8', errors='ignore')))
            except KeyboardInterrupt:
                masterSocket.close()
                self.socketToMaster.close()
                break


    def request_handler(masterSocket, masterAddr, masterData):
        requestInfo = parse_request_info(masterAddr, masterData)
        ifCached, cachePath = check_if_cached(requestInfo["total_url"])
        requestInfo["if_cached"] = ifCached
        requestInfo["cache_path"] = cachePath
        # clear expired cache before handling new request
        clearCache()

        if requestInfo["if_cached"]:
            fetch_from_cache(masterSocket, masterAddr, requestInfo)
        else:
            fetch_from_origin(masterSocket, masterAddr, requestInfo)
            write_to_cache()


    def request_handler_mem(masterSocket, masterAddr, masterData):
        requestInfo = parse_request_info(masterAddr, masterData)
        cacheKey = requestInfo["total_url"]
        if cacheKey in self.cacheDict:
            # send in chunks to master server
            for chunk in self.cacheDict[cacheKey]["data"]:
                masterSocket.
        else:
            fetch_from_origin(masterSocket, masterAddr, requestInfo)



cache = Cache()
cache.request_handler()
