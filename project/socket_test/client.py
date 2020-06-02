import socket
import struct

IP = "127.0.0.2"
PORT = 8810

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

while True:
    msg = input(">")
    s.send(msg.encode("utf-8"))
    msg = s.recv(1024).decode("utf-8")
    print(msg)