import socket

IP = "0.0.0.0"
PORT = 8002

def parse_ip_packet_detail(ip_packet):
    src_ip_str, dst_ip_str, content_str  = ip_packet.split('\n')
    dst_ip = dst_ip_str.split(':')[1].strip()
    dic = {}
    dic['src ip'] = src_ip_str.split(':')[1].strip()
    dic['dst ip'] = dst_ip_str.split(':')[1].strip()
    dic['content'] = content_str.split(':')[1].strip()
    return dic

server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_s.bind((IP, PORT))

print("server start")
server_s.listen(1)
conn, client_addr = server_s.accept()
print("Connect by {}:{}".format(client_addr[0], client_addr[1]))

#接收
ip_packet = conn.recv(1024).decode()

dic = parse_ip_packet_detail(ip_packet)

print("收到的内容:")
print(dic['content'])