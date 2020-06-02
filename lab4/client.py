import socket
import struct

def encapsulate_ip_packet(src_ip, dst_ip, content):
    ip_packet = \
    '''
    src ip: %s
    dst ip: %s
    content: %s
    '''%(src_ip, dst_ip, content)

    return ip_packet.strip()

VPN_IP = "127.0.0.1"
VPN_PORT = 8001 #vpn-client port

#---------- connect to vpn start--------- #
print("Connect to vpn client")
vpn_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vpn_s.connect((VPN_IP, VPN_PORT))
print("Connected")
#---------- connect to vpn end ---------- #

# -----------send message start---------- #
print("Send start")
src_ip = "127.0.0.1"

dst_ip = input("Input destination:")
# dst_ip = "127.0.0.1"
content = input("Input content to send:")
# content = "hello"
ip_packet = encapsulate_ip_packet(src_ip, dst_ip, content)

vpn_s.send(ip_packet.encode())
print("Send finish")
# -----------send message end  ---------- #