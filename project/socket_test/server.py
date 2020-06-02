import socket

IP = "127.0.0.2"
PORT = 8810

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))

s.listen(1)

while True:
    conn, client_addr = s.accept()
    print("connect by {}:{}".format(client_addr[0], client_addr[1]))
    while True:
        msg = conn.recv(1024).decode("utf-8")
        print("Receive: %s"%(msg))
        conn.send(msg.encode("utf-8"))