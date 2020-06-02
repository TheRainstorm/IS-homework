import socket

VPN_SERVER_IP = "0.0.0.0"
VPN_SERVER_PORT = 8888

def parse_ip_in_ip_packet(ip_in_ip_packet):
    header, ip_packet, _ = ip_in_ip_packet.split('---')

    return ip_packet.strip()

def parse_ip_packet(ip_packet):
    src_ip_str, dst_ip_str, content_str  = ip_packet.split('\n')
    dst_ip = dst_ip_str.split(':')[1].strip()
    return (dst_ip, 8002)

print("VPN server start")
vpn_server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vpn_server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
vpn_server_s.bind((VPN_SERVER_IP, VPN_SERVER_PORT))
vpn_server_s.listen(1)
vpn_client, client_addr = vpn_server_s.accept()
print("Connect by {}:{}".format(client_addr[0], client_addr[1]))

# ---------- 解封装 start----------#
ip_in_ip_packet = vpn_client.recv(1024).decode()

ip_packet = parse_ip_in_ip_packet(ip_in_ip_packet)

print("解封装:")
print(ip_packet)
dst_addr = parse_ip_packet(ip_packet)
print("转发到:",dst_addr)
# ---------- 解封装 end  ----------#

# ---------- 转发 start --------#
server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.connect(dst_addr)

server_s.send(ip_packet.encode())
# ---------- 转发 end   --------#
