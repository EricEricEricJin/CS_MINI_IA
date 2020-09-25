from socket import *
from service import Service

SERVER_ADDR = ("127.0.0.1", 2345)

class Main:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(SERVER_ADDR)
        self.sock.listen(10)


    def run(self):
        while True:
            conn, addr = self.sock.accept()
            Service(conn).start()


if __name__ == "__main__":
    M_ins = Main()
    M_ins.run()