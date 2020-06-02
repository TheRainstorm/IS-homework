import socket

VPN_IP = "127.0.0.1"
VPN_PORT = 8001

def encapsulate_ip_in_ip_packet(src_ip, dst_ip, ip_packet):
    ip_in_ip_packet = \
    '''
    src ip: %s
    dst ip: %s
    ---
    %s
    ---
    '''%(src_ip, dst_ip, ip_packet)

    return ip_in_ip_packet.strip()

# 输入vpn server ip和port
ip_port_str = input("Input vpn server ip and port (ip:port): ")
VPN_SERVER_IP, port_str = ip_port_str.split(':')
VPN_SERVER_PORT = int(port_str)
# VPN_SERVER_IP, VPN_SERVER_PORT = "127.0.0.1", 8888

# 和client建立连接
print("VPN client start")
vpn_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vpn_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
vpn_s.bind((VPN_IP, VPN_PORT))
vpn_s.listen(1)
client, client_addr = vpn_s.accept()
print("Connect by {}:{}".format(client_addr[0], client_addr[1]))

# 接收client输入
ip_packet = client.recv(1024).decode()
vpn_s.close()

# ---------- 封装 start ----------#
src_ip, dst_ip = "127.0.0.1", VPN_SERVER_IP
ip_in_ip_packet = encapsulate_ip_in_ip_packet(src_ip, dst_ip, ip_packet)
# ---------- 封装 end   ----------#

# ---------- 转发 start ----------#
print("Connect to VPN server")
vpn_server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vpn_server_s.connect((VPN_SERVER_IP, VPN_SERVER_PORT))
print("Connect to VPN server successed")

print("封装:")
print(ip_in_ip_packet)
vpn_server_s.send(ip_in_ip_packet.encode())
# ---------- 转发 end   ----------#