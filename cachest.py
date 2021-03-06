import threading
import socket
import os
from datetime import datetime, timedelta
from utils import parse_request_info, get_cache_port, MAX_CONN, RECV_SIZE
from heartbeat import send_heartbeat, HEART_BEAT_INTERVAL
# CACHE_DIR = "./cache"
from requests import get
import errno

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
        #
        # {
        #   "www.google.com":
        #      {
        #          data: ["GET R", "EQUES", "T DAT", "A"],
        #          timestamp: "10:01 PM"
        #      }
        # }
        #

   
    def fetch_from_origin_mem(self, masterSocket, masterAddr, requestInfo):
        try:
            
            print("requestInfo:\n", requestInfo)
            # create server socket (socket to talk to origin server)
            socketToOrigin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketToOrigin.connect((requestInfo["server_url"], requestInfo["server_port"]))
            socketToOrigin.send(requestInfo["client_data"])

            # # get reply for server socket (origin server)
            reply = socketToOrigin.recv(RECV_SIZE)
            print("FetchFromOrigin sending reply from cache to master server")

            self.cacheDict[requestInfo["total_url"]] = {
                "data": [],
                "timestamp": datetime.now()
            }

            # get_url = "http://" + requestInfo["total_url"]
            # print(get_url)
            # reply = get(get_url).content

            # chunks = [reply[i:i+RECV_SIZE] for i in range(0, len(reply), RECV_SIZE)]
            # i=0
            # for chunk in chunks:
            #     # masterSocket.send(reply)
            #     masterSocket.send(chunk)
            #     i = i+1
            #     print("FetchFromOrigin: sending a chunk")

            # print(f"CACHE number of chunks sent: {i}")
            
            print("FetchFromOrigin start constructing chuncked data")
            chunkedData = []
            
            while len(reply):
                print("PRINTING LEN reply: \n", len(reply))
                masterSocket.send(reply)
                print("FetchFromOrigin sending a chunk to master")
                
                chunkedData.append(reply)
                reply = socketToOrigin.recv(RECV_SIZE)
                print("CACHE recieving next chunk from origin /n")

            self.cacheDict[requestInfo["total_url"]]["data"] = chunkedData

            masterSocket.send(b"\r\n\r\n")
            print("FetchFromOrigin finished sending reply to master server")

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
                self.request_handler_mem(masterSocket, masterAddr, str(masterData, encoding='utf-8', errors='ignore'))

                # global variable that holds time
                # at every point after handling mem, check if FLUSH_TIME has passed in global timer
                # if it has, run flush code and reset global timer
                # if it hasn't, continue

            except KeyboardInterrupt:
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
        print("Start flushing cache")
        for cacheKey in self.cacheDict:
            if self.ifExpired(cacheKey):
                self.cacheDict[cacheKey]["timestamp"] = None
                self.cacheDict[cacheKey]["data"] = None

    def request_handler_mem(self, masterSocket, masterAddr, masterData):
        # print("Request handler master data: \n", masterData)
        requestInfo = parse_request_info(masterAddr, masterData)
        # print("Request info: \n", requestInfo)
        cacheKey = requestInfo["total_url"]
        
        # print("begin request handler")

        if cacheKey in self.cacheDict:
            chunks = None

            # send in chunks to master server
            if not self.ifExpired(cacheKey):
                print("cache hits for {}".format(requestInfo["total_url"]))
                chunks = self.cacheDict[cacheKey]["data"]
                for chunk in chunks:
                    masterSocket.send(chunk)
                    print("CHUNK sending to master each time: /n", chunk)
                    print("CacheHit sending data to master")
                masterSocket.send(b"\r\n\r\n")

                print("finished servicing cache hit")
            else:
                print("fetch from origin to get {}".format(requestInfo["total_url"]))
                self.fetch_from_origin_mem(masterSocket, masterAddr, requestInfo)

        else:
            print("NOT in cache dict")
            self.fetch_from_origin_mem(masterSocket, masterAddr, requestInfo)


        masterSocket.close()

    def run(self):
        """
        Run scheduled tasks in thread to maintain cache servers
        """
        t_main = threading.Thread(target=self.server_run)
        # t_cache_flush = threading.Timer(CACHE_FLUSH_INTERVAL, self.flush_cache)
        t_heartbeat = threading.Thread(target=send_heartbeat)

        # start threads
        t_main.start()
        # t_cache_flush.start()
        t_heartbeat.start()

        # end threads
        t_main.join()
        # t_cache_flush.join()
        t_heartbeat.join()

if __name__ == '__main__':
    cache = Cache()
    cache.server_init()
    cache.run()