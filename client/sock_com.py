from socket import * 

SERVER_ADDR = ("127.0.0.1", 1234)

class sockCom:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self.sock.connect(SERVER_ADDR)

    def send(self, bin_data):
        self.sock.send(bin_data)

    def recv(self):
        return self.sock.recv(4096)

    def __del__(self):
        self.sock.close()