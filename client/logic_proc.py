from sock_com import sockCom
from db_op import dbOp

ONLINE = 1
OFFLINE = 0

class logicProc:
    def __init__(self):
        self.login_status = OFFLINE
        self.user_name = None
        self.user_id = None
        
        self.sockCom_ins = sockCom()


    def connect(self):
        self.sockCom_ins.connect()

    def sign_up(self, user_name, passwd):
        # if success:
        #     return 1
        # else:
        #     return 0
        data = {"mode": "sign_up", "name": user_name, "pwd": passwd}
        self.sockCom_ins.send(str(data).encode())
        recv_raw = self.sockCom_ins.recv()
        
        if recv_raw == b"0":
            # failed
            return 0
        else:
            return recv_raw.decode()
        pass

    def sign_in(self, user_id, passwd):
        # if success:
        #     modify self.user_id, self.user_name, self.login_status
        #     return 1
        # else:
        #     return 0

        data = {"mode": "sign_in", "id": user_id, "pwd": passwd}
        self.sockCom_ins.send(str(data).encode())
        recv_raw = self.sockCom_ins.recv()
        if recv_raw == b"0":
            return 0
        else:
            self.user_name = recv_raw.decode()
            self.user_id = user_id
            self.login_status = ONLINE
            return 1

    def sign_out(self):
        # if success:
        #     self.login_status = OFFLINE
        #     self.user_name = None
        #     self.user_id = None
        #     return 1
        # else:
        #     return 0
        self.sockCom_ins.send(str({"mode": "sign_out"}).encode())
        recv_raw = self.sockCom_ins.recv()

        if recv_raw == b"0":
            return 0
        else:
            return 1

        pass

    def add_friend(self, friend_id, req_note):
        # if success:
        #     return 1
        # else:
        #     return 0
        
        data = {"mode": "add_friend", "friend_id": friend_id, "req_note": req_note}
        self.sockCom_ins.send(str(data).encode())
        recv_raw = self.sockCom_ins.recv()
        if recv_raw == b"1":
            return 1
        else:
            return 0
        pass

    def del_friend(self, friend_id):
        # if success:
        #     return 1
        # else:
        #     return 0
        data = {"mode": "del_friend", "friend_id": friend_id}
        self.sockCom_ins.send(str(data).encode())

        recv_raw = self.sockCom_ins.recv()
        if recv_raw == b"1":
            return 1
        else:
            return 0
        pass

    def accept_friend(self, friend_id):
        data = {"mode": "accept_friend", "friend_id": friend_id}
        self.sockCom_ins.send(str(data).encode())

        recv_raw = self.sockCom_ins.recv()
        if recv_raw == b"1":
            return 1
        else:
            return 0

    def refuse_friend(self, friend_id):
        data = {"mode": "refuse_friend", "friend_id": friend_id}
        self.sockCom_ins.send(str(data).encode())

        recv_raw = self.sockCom_ins.recv()
        if recv_raw == b"1":
            return 1
        else:
            return 0
        
    def send_message(self, friend_id, msg):
        data = {"mode": "send_msg", "friend_id": friend_id, "msg": msg}
        self.sockCom_ins.send(str(data).encode())
        recv_raw = self.sockCom_ins.recv()
        if recv_raw == b"1":
            return 1
        else:
            return 0

    def refresh(self):
        # Put new messages into database
        # Fatch ALL from data base
        # return
        # {"msg": [[sender, send_t, msg], [], ...], "freq": [[friend_id, req_note], [], ...], "friend": [[friend_id, friend_username, login_status], [], ...]}
        # 

        self.sockCom_ins.send(str({"mode": "refresh"}).encode())
        recv_raw = self.sockCom_ins.recv()
        if recv_raw == b"0":
            return 0
        else:
            return eval(recv_raw)


    def close_sock(self):
        self.sockCom_ins.send(str({"mode": "close_sock"}).encode())
        del self.sockCom_ins