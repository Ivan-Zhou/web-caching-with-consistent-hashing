import threading
import socket
import os
from datetime import datetime, timedelta
from utils import parse_request_info, MAX_CONN, RECV_SIZE
CACHE_DIR = "./cache"

# socketToMaster talks to master
# masterSocket is the socket in master which is used to talk to cache server

class Cache():
    def __init__(self, HOST, PORT):
        try:
            # Create a TCP socket
            self.socketToMaster = socket(socket.AF_INET, socket.SOCK_STREAM)
            # Re-use the socket
            self.socketToMaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.socketToMaster.bind(HOST, PORT)

            self.socketToMaster.listen(MAX_CONN) # become a cache socket
        
        except Exception as e:
            print(f"Error occured on Cache server init: {e}")
            self.socketToMaster.close()
            return
        
        # TODO alternatively, we can put a lock around the cache structure
        # to avoid these threading concerns
        # we can also have a lock per cache entry
        # and one coarse grain lock for the dict
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
    
        # # Make cache directory ??store in memory
        # if not os.path.isdir(CACHE_DIR):
        #     os.makedirs(CACHE_DIR)
        # for file in os.listdir(CACHE_DIR):
        #     os.remove(CACHE_DIR + "/" + file)

    def fetch_from_origin_mem(self, masterSocket, masterAddr, requestInfo):
        try: 
            # create server socket (socket to talk to origin server)
            socketToOrigin = socket(socket.AF_INET, socket.SOCK_STREAM)
            socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
            socketToOrigin.send(requestInfo["client_data"])
            print("receiving reply from origin server")
        
            # get reply for server socket (origin server)
            reply = socketToOrigin.recv(RECV_SIZE)
            print("sending reply from cache to master server")
            self.cacheDict[requestInfo["total_url"]] = {
                "data": [],
                "timestamp": datetime.now()
            }
            while len(reply):
                masterSocket.send(reply)
                self.cacheDict[requestInfo["total_url"]]["data"].append(reply)
                reply = socketToOrigin.recv(RECV_SIZE)
                
            masterSocket.send(str.encode("\r\n\r\n"))
            print("finished sending reply to master server")
        
            socketToOrigin.close()
          
        except Exception as e:
            masterSocket.close()
            print(e)
        return
       

    def server_run(self):
        while True:
            try:
                masterSocket, masterAddr = self.socketToMaster.accept()
                masterData = masterSocket.recv(RECV_SIZE)
                t = threading.Thread(
                    target=self.request_handler_mem, 
                    args=(masterSocket, masterAddr, str(masterData, encoding='utf-8', errors='ignore')))
                t.start()
            except KeyboardInterrupt:
                # join threads
                masterSocket.close()
                self.socketToMaster.close()
                break

    def ifExpired(self, key):
        cacheTime = self.cacheDict[key]["timestamp"]
        return datetime.now() - cacheTime > timedelta(days=1)

    def request_handler_mem(self, masterSocket, masterAddr, masterData):
        requestInfo = parse_request_info(masterAddr, masterData)
        cacheKey = requestInfo["total_url"]
        if cacheKey in self.cacheDict and self.ifExpired(cacheKey):
            # send in chunks to master server
            for chunk in self.cacheDict[cacheKey]["data"]:
                masterSocket.send(chunk)
        else:
            self.fetch_from_origin_mem(masterSocket, masterAddr, requestInfo)

        masterSocket.close()

    def run(self):
        """
        Run scheduled tasks in thread to maintain cache servers
        """
        t1 = threading.Thread(target=self.server_run)
        # TODO add function to flush cache
        # 
        # t2 = threading.Timer(FLUSH_INTERVAL, self._flush)
        t1.start()
        # t2.start()
        t1.join()
        # t2.join()


    # def request_handler(masterSocket, masterAddr, masterData):
    #     requestInfo = parse_request_info(masterAddr, masterData)
    #     ifCached, cachePath = check_if_cached(requestInfo["total_url"])
    #     requestInfo["if_cached"] = ifCached
    #     requestInfo["cache_path"] = cachePath
    #     # clear expired cache before handling new request
    #     clearCache()

    #     if requestInfo["if_cached"]:
    #         fetch_from_cache(masterSocket, masterAddr, requestInfo)
    #     else:
    #         fetch_from_origin(masterSocket, masterAddr, requestInfo)
    #         write_to_cache()


       
    # # Check if the requested resource has been cached
    # def check_if_cached(cacheKey):  
    #     '''
    #     File version
    #     '''
    #     if cacheKey.startswith("/"):
    #         cacheKey = cacheKey.replace("/", "", 1)

    #     cachePath = CACHE_DIR + "/" + cacheKey.replace("/", "__")

    #     if os.path.isfile(cachePath):
    #         return true, cachePath
    #     else:
    #         return false, cachePath

    # # Check if the cache file is expired (>1d)
    # def ifExpired(f):
    #     filePath = CACHE_DIR + "/" + f
    #     fileTime = datetime.fromtimestamp(path.getctime(filePath))
    #     return datetime.now() - fileTime > timedelta(days=1)

    # #Clear cache when expired 
    # def clearCache():
    #     #requestInfo is class variable
    #     cacheFiles = os.listdir(CACHE_DIR)
    #     for f in cacheFiles:
    #         if ifExpired(f):
    #             os.remove(CACHE_DIR + "/" + f)

    # def fetch_from_cache(masterSocket, masterAddr):
    #     print("Fetching cache from " + cachePath + " to master " + masterAddr)
    #     file = open(cachePath, "rb")
    #     chunk = f.read(RECV_SIZE)
    #     while chunk:
    #         masterSocket.send(chunk)
    #         chunk = f.read(RECV_SIZE)
    #     f.close()

 
# fetch from origin and write to cache
    # def fetch_from_origin(masterSocket, masterAddr, requestInfo):
    #     try: 
    #         # create server socket (socket to talk to origin server)
    #         socketToOrigin = socket(socket.AF_INET, socket.SOCK_STREAM)
    #         socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
    #         socketToOrigin.send(requestInfo["client_data"])
    #         print("receiving reply from origin server")
        
    #         # get reply for server socket (origin server)
    #         reply = socketToOrigin.recv(RECV_SIZE)
    #         f = open(cachePath, "w+")
    #         print("sending reply from cache to master server")
    #         while len(reply):
    #             masterSocket.send(reply)
    #             f.write(str(reply, 'utf-8'))
    #             reply = socketToOrigin.recv(RECV_SIZE)
                
    #         masterSocket.send(str.encode("\r\n\r\n"))
    #         print("finished sending reply to master server")
    #         f.close()
        
    #         socketToOrigin.close()
          
    #     except Exception as e:
    #         masterSocket.close()
    #         print(e)
    #     return

cache = Cache()
cache.run()
