import threading
import socket
import os
from datetime import datetime, timedelta
from utils import parse_request_info, get_cache_port, MAX_CONN, RECV_SIZE
from heartbeat import send_heartbeat, HEART_BEAT_INTERVAL
from rwlock import ReadWriteLock
# CACHE_DIR = "./cache"
from requests import get

# how often to go through dict and flush expired
CACHE_FLUSH_INTERVAL = 3600 # 1 hour
CACHE_EXPIRATION = 1 # days

# socketToMaster talks to master
# masterSocket is the socket in master which is used to talk to cache server

class Cache():
    def __init__(self):
        self.threads = []
        self.cacheDict = {
        }
        self.cacheDictLock = ReadWriteLock()

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

        # Solution:
        # Remove the data (set it to None). Set timestamp to None. Keep lock.
        #
        # SWMR lock around entire cache dict
        # Adding new entry = lock entire dict as writer
        # Editing existing entry = lock entire dict as reader, lock


    def fetch_from_origin_mem(self, masterSocket, masterAddr, requestInfo):
        try:
            # print("requestInfo:\n", requestInfo)
            # create server socket (socket to talk to origin server)
            socketToOrigin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
            socketToOrigin.send(requestInfo["client_data"])



            # get reply for server socket (origin server)
            reply = socketToOrigin.recv(RECV_SIZE)
            print("FetchFromOrigin sending reply from cache to master server")

            # acquire high level SWMR lock as writer
            self.cacheDictLock.acquire_write()
            print ("etchFromOrigin after coarse grain acquire write")
            self.cacheDict[requestInfo["total_url"]] = {
                "data": [],
                "timestamp": datetime.now(),
                "lock": ReadWriteLock()
            }
            self.cacheDict[requestInfo["total_url"]]["lock"].acquire_write()
            print("FetchFromOrigin after fine grain acquire write")
            # release high level SWMR lock as writer
            self.cacheDictLock.release_write()
            print("FetchFromOrigin after coarse grain release write")

            # acquire coarse grain lock as reader, fine grain as writer
            self.cacheDictLock.acquire_read()
            print("FetchFromOrigin after coarse grain acquire read")

            print("FetchFromOrigin start constructing chuncked data")
            chunkedData = []
            
            while len(reply):
                masterSocket.send(reply)
                print("FetchFromOrigin sending a chunk to master")
                chunkedData.append(reply)
                reply = socketToOrigin.recv(RECV_SIZE)

            self.cacheDict[requestInfo["total_url"]]["data"] = chunkedData
            for chunk in chunkedData:
                print(str(chunk, encoding='utf-8', errors='ignore'))

            masterSocket.send(str.encode("\r\n\r\n"))
            print("FetchFromOrigin finished sending reply to master server")

            # release fine grain lock as writer, coarse grain as reader
            self.cacheDict[requestInfo["total_url"]]["lock"].release_write()
            self.cacheDictLock.release_read()
            socketToOrigin.close()

            print("FetchFromOrigin finished")

        except Exception as e:
            masterSocket.close()
            print(e)
        return

    def server_init(self):
        try:
            # Create a TCP socket
            self.socketToMaster = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketToMaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # get IP and PORT from 3rd party??? only when running on myth
            # IP = get('https://api.ipify.org').text
            # print(f'The public IP address of cache is: {IP}')
            PORT = get_cache_port()
            # listen for connections to cache server
            self.socketToMaster.bind(("", PORT)) #running on AWS
            self.socketToMaster.listen(MAX_CONN) # become a cache socket
        except Exception as e:
            print(f"Error occured on Cache server init: {e}")
            self.socketToMaster.close()

        print("socket creation done in server_init")




    def server_run(self):
        print("start server run")
        while True:
            try:
                masterSocket, masterAddr = self.socketToMaster.accept()
                print("Received connection from master")
                masterData = masterSocket.recv(RECV_SIZE)
                t = threading.Thread(
                    target=self.request_handler_mem,
                    args=(masterSocket, masterAddr, str(masterData, encoding='utf-8', errors='ignore')))
                self.threads.append(t)
                t.start()
                print("start processing connection from master")

            except KeyboardInterrupt:
                # join threads
                for t in self.threads:
                    t.join()

                masterSocket.close()
                self.socketToMaster.close()
                break

    def ifExpired(self, key):
        cacheTime = self.cacheDict[key]["timestamp"]
        return datetime.now() - cacheTime > timedelta(days=CACHE_EXPIRATION)


    def flush_cache(self):
        '''
        Clear out contents of an expired entry. Set data field to None.
        Keep key in dict for efficiency and ease of concurrency implementation.
        '''
        # acquire coarse grain lock as a reader
        print("Start flushing cache")
        print("attempt to acquire coarse grain read lock in flush")
        self.cacheDictLock.acquire_read()
        print("acquired coarse grain read lock in flush")
        for cacheKey in self.cacheDict:
            # acquire fine grain lock as writer
            self.cacheDict[cacheKey]["lock"].acquire_write()
            if self.ifExpired(cacheKey):
                self.cacheDict[cacheKey]["timestamp"] = None
                self.cacheDict[cacheKey]["data"] = None

            self.cacheDict[cacheKey]["lock"].release_write()

        # release coarse grain lock as a reader
        self.cacheDictLock.release_read()
        print("release coarse grain read lock in flush")

    def request_handler_mem(self, masterSocket, masterAddr, masterData):
        # print("Request handler master data: \n", masterData)
        requestInfo = parse_request_info(masterAddr, masterData)
        # print("Request info: \n", requestInfo)
        cacheKey = requestInfo["total_url"]
        
        
        # print("begin request handler")

        # acquire coarse grain lock as a reader
        self.cacheDictLock.acquire_read()

        # print("request handler acquire initial read lock")

        if cacheKey in self.cacheDict:
            chunks = None
            found = False
            # acquire fine grain lock as a reader
            self.cacheDict[cacheKey]["lock"].acquire_read()
            if not self.ifExpired(cacheKey):
                found = True
                chunks = self.cacheDict[cacheKey]["data"].copy()
            # release fine grain lock as a reader
            self.cacheDict[cacheKey]["lock"].release_read()
            # release coarse grain lock as a reader
            self.cacheDictLock.release_read()

            # send in chunks to master server
            if found:
                print("cache hits for {}".format(requestInfo["total_url"]))
                for chunk in chunks:
                    masterSocket.send(chunk)
                    print("CacheHit sending data to master")
                masterSocket.send(str.encode("\r\n\r\n"))

                print("finished servicing cache hit")
            else:
                print("fetch from origin to get {}".format(requestInfo["total_url"]))
                self.fetch_from_origin_mem(masterSocket, masterAddr, requestInfo)

        else:
            # release coarse grain lock as a reader
            self.cacheDictLock.release_read()
            print("NOT in cache dict, release coarse lock")
            self.fetch_from_origin_mem(masterSocket, masterAddr, requestInfo)


        masterSocket.close()

    def run(self):
        """
        Run scheduled tasks in thread to maintain cache servers
        """
        t_main = threading.Thread(target=self.server_run)
        t_cache_flush = threading.Timer(CACHE_FLUSH_INTERVAL, self.flush_cache)
        t_heartbeat = threading.Thread(target=send_heartbeat)

        # start threads
        t_main.start()
        t_cache_flush.start()
        t_heartbeat.start()

        # end threads
        t_main.join()
        t_cache_flush.join()
        t_heartbeat.join()

if __name__ == '__main__':
    cache = Cache()
    cache.server_init()
    cache.run()

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

