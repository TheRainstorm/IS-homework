import socket

def parse_ip_in_ip_packet(ip_in_ip_packet):
    ip_packet =ip_in_ip_packet.split('------')[1]
    return ip_packet

def parse_ip_packet(ip_packet):
    src_ip = "127.0.0.1"
    dst_ip = "127.0.0.1"
    return (), (dst_ip ,8002)

VPN_SERVER_IP = "0.0.0.0"
VPN_SERVER_PORT = 8888

vpn_server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vpn_server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
vpn_server_s.bind((VPN_SERVER_IP, VPN_SERVER_PORT))

print("VPN server start")
vpn_server_s.listen(1)
vpn_client, client_addr = vpn_server_s.accept()
print("Connect by {}:{}".format(client_addr[0], client_addr[1]))

ip_in_ip_packet = vpn_client.recv(1024).decode()
print(ip_in_ip_packet)

ip_packet = parse_ip_in_ip_packet(ip_in_ip_packet)
print(ip_packet)
src_addr, dst_addr = parse_ip_packet(ip_packet)
print(src_addr, dst_addr)
###
server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.connect(dst_addr)

server_s.send(ip_packet.encode())