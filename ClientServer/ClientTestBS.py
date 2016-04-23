import socket
import sys

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('10.42.0.1', 8089))
clientsocket.send(sys.argv[1])
