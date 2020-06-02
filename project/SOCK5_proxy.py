import socket
import struct
import select
import threading as td

class Socks_Proxy:
    SOCKS_VERSION = 5

    def __init__(self, IP, PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(5)

        self.mainloop()
    
    def mainloop(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            proxy_thread = td.Thread(target=self.proxy, args=(client_socket, client_address))
            proxy_thread.run()
            # self.proxy(client_socket, client_address)

    def proxy(self, client_socket, client_address):
        print("[{}:{}]\t:尝试连接SOCKS服务器".format(client_address[0], client_address[1]))

        # 先验证
        authen_res = self.authenticate(client_socket)

        #验证失败
        if authen_res==False:
            client_socket.close()
            return
        
        # 验证通过则开始转发数据
        self.sending(client_socket)
        client_socket.close()
    
    def authenticate(self, client_socket):
        '''
        step1: 
            协商版本及认证方式
            VER	NMETHODS	METHODS
            1	1	        1-255
        '''
        data = client_socket.recv(2)
        VER, NMETHODS = struct.unpack("!BB", data)
        if VER!=self.SOCKS_VERSION:
            print("SOCKS版本不支持")
            return False

        methods_bytes = client_socket.recv(NMETHODS)
        '''
        step2:
            服务器从客户端提供的方法中选择一个通知客户端
            VER	METHOD
            1	1
        '''
        method = self.choose_method(methods_bytes)
        client_socket.send(struct.pack("!Bc", VER, method))
        if method==b'\xff':
            print("无可接受的方法")
            return False
        
        # 无需认证，返回认证成功
        if method==b'\x00':
            return True
        
        '''
        step 2.a:
            用户名、密码认证
        '''
        return True

    def choose_method(self, methods_bytes):
        '''
        选择认证方式
            0x00 不需要认证
            0x02 用户名、密码认证
            0xFF 无可接受的方法
        '''
        if b'\x00' in methods_bytes:
            return b'\x00'
        elif b'\x02' in methods_bytes:
            return b'\x02'
        else:
            return b'\xff'
    
    def sending(self, client_socket):
        '''
        step 1
            接收客户端SOCKS5请求
            VER	CMD	RSV	    ATYP	DST.ADDR	DST.PORT
            1	1	0x00	1	    动态	    2

            CMD: SOCK的命令码
                - 0x01表示CONNECT请求
                0x02表示BIND请求
                0x03表示UDP转发
                RSV 0x00，保留
            ATYP: DST.ADDR类型
                - 0x01 IPv4地址，DST.ADDR部分4字节长度
                - 0x03域名，DST ADDR部分第一个字节为域名长度，DST.ADDR剩余的内容为域名，没有\0结尾。
                0x04 IPv6地址，16个字节长度。
        '''
        VER, CMD, RSV, ATYP = struct.unpack("!BBBB", client_socket.recv(4))
        if VER!=self.SOCKS_VERSION:
            print("SOCKS版本不一致")
            return

        if ATYP==1: #ipv4
            DST_ADDR = socket.inet_ntoa(client_socket.recv(4))
        elif ATYP==3: #域名
            domain_length = struct.unpack("!B", client_socket.recv(1))[0]
            DST_ADDR = client_socket.recv(domain_length).decode()
        else:
            print("只支持IPv4和域名格式地址")
            client_socket.close()
            return

        DST_PORT = struct.unpack("!H", client_socket.recv(2))[0]
        '''
        step 2
            响应客户端请求
            VER	REP	RSV	    ATYP	BND.ADDR	BND.PORT
            1	1	0x00	1	    动态	    2

            REP: 应答字段
                0x00表示成功
                0x01普通SOCKS服务器连接失败
                0x02现有规则不允许连接
                0x03网络不可达
                0x04主机不可达
                0x05连接被拒
                0x06 TTL超时
                0x07不支持的命令
                0x08不支持的地址类型
                0x09 - 0xFF未定义
        '''
        if CMD==1: # CONNECT请求
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((DST_ADDR, DST_PORT))
            BND_ADDR, BND_PORT = remote_socket.getsockname()
            print("连接到: {}:{}".format(DST_ADDR, DST_PORT))
            
            client_socket.send(struct.pack("!BBBB4sH", self.SOCKS_VERSION,
                    0, 0, 1, socket.inet_aton(BND_ADDR), BND_PORT))
        else:
            print("只支持CONNECT请求")
            client_socket.close()
            return

        cnt = 0
        while True:
            print(cnt)
            cnt += 1
            rs, ws, es = select.select([client_socket, remote_socket], [], [])
            # 等待数据
            print("client" if rs[0]==client_socket else "remote")
            if client_socket in rs:
                data = client_socket.recv(4096)
                if remote_socket.send(data) <= 0:
                    break
            if remote_socket in rs:
                data = remote_socket.recv(4096)
                if client_socket.send(data) <= 0:
                    break
        print(client_socket.getsockname())

if __name__ == "__main__":
    IP = "0.0.0.0"
    PORT = 8800

    print("SOCK5 Proxy Start.")
    Socks_Proxy(IP, PORT)


