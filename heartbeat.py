from socket import socket, AF_INET, SOCK_STREAM
from time import time, ctime, sleep

from utils import get_master_address

HEART_BEAT_INTERVAL = 1

def send_heartbeat():
    master_address = get_master_address()
    while True:
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
            serverSocket.connect((master_address["host"], master_address["port"]))
            serverSocket.send("heartbeat".encode())
            sleep(HEART_BEAT_INTERVAL)
            serverSocket.close()
        except Exception as e:
            print(f"Error occured on send_heartbeat: {e}")


if __name__ == '__main__':
    # for testing purpose
    send_heartbeat()
