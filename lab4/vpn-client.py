import socket

VPN_IP = "127.0.0.1"
VPN_PORT = 8001

# 设置学校代理服务器地址和端口
VPN_SERVER_IP = "127.0.0.1"
# VPN_SERVER_IP = "192.168.31.52"
VPN_SERVER_PORT = 8888

vpn_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vpn_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
vpn_s.bind((VPN_IP, VPN_PORT))

print("VPN client start")
vpn_s.listen(1)
client, client_addr = vpn_s.accept()
print("Connect by {}:{}".format(client_addr[0], client_addr[1]))

ip_packet = client.recv(1024).decode()

print(ip_packet)
vpn_s.close()

### connect vpn server
print("Connect to VPN server")
vpn_server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vpn_server_s.connect((VPN_SERVER_IP, VPN_SERVER_PORT))

ip_in_ip_packet = '''
header
------
%s
------
'''%ip_packet

print(ip_in_ip_packet)
vpn_server_s.send(ip_in_ip_packet.encode())