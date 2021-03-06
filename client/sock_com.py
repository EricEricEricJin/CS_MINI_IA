'''
@File       :   sock_com.py
@Time       :   9/27/2020
@Author     :   Eric Jin
@Version    :   2.0
@Contact    :   jyseric@126.com
@License    :   WTFPL
'''


from socket import *


class sockCom:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)

    def connect(self, server_addr):
        print("Connect", server_addr)
        try:
            self.sock.connect(server_addr)
            print("Can conn")
            return 1
        except:
            return 0

    def send(self, bin_data):
        self.sock.send(bin_data)

    def recv(self):
        return self.sock.recv(4096)

    def __del__(self):
        self.sock.close()
