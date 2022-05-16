from socket import socket, AF_INET, SOCK_STREAM
from time import time, ctime, sleep

from utils import get_master_address

BEATWAIT = 1

def send_heartbeat():
    master_address = get_master_address()
    while True:
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect((master_address["host"], master_address["port"]))
        serverSocket.send("heartbeat".encode())
        sleep(BEATWAIT)


if __name__ == '__main__':
    # for testing purpose
    send_heartbeat()
