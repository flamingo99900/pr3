#!/usr/bin/python3

import sys

from server import Server


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8888
    server = Server(HOST, PORT)
    server.start('--async' in sys.argv)

