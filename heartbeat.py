from socket import socket, AF_INET, SOCK_STREAM
from time import time, ctime, sleep

from utils import get_master_address

HEART_BEAT_INTERVAL = 1

def send_heartbeat():
    master_address = get_master_address()
    alerted = False
    while True:
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
            serverSocket.connect((master_address["host"], master_address["port"]))
            serverSocket.send("heartbeat".encode())
            sleep(HEART_BEAT_INTERVAL)
            serverSocket.close()
        except Exception as e:
            if not alerted:
                print(f"Error occured on sending heartbeat to {master_address} due to error: {e}")
            alerted = True
        else:
            # to avoid repeatedly sending alerts
            alerted = False


if __name__ == '__main__':
    # for testing purpose
    send_heartbeat()
