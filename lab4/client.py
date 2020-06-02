import socket
import struct

VPN_IP = "127.0.0.1"
VPN_PORT = 8001 #vpn-client port

vpn_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connect to vpn client")
vpn_s.connect((VPN_IP, VPN_PORT))
print("Connected")

src_ip = "127.0.0.1"
dst_ip = "127.0.1.2"
ip_packet ='''src ip: %s
dst_ip: %s
content: %s
'''%(src_ip, dst_ip, "hello")

vpn_s.send(ip_packet.encode())
print("Send finish")