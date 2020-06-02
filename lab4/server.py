import socket

IP = "0.0.0.0"
PORT = 8002

server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_s.bind((IP, PORT))

print("server start")
server_s.listen(1)
conn, client_addr = server_s.accept()
print("Connect by {}:{}".format(client_addr[0], client_addr[1]))

ip_packet = conn.recv(1024).decode()

print(ip_packet)