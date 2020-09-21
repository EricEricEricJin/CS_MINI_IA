from db_op import dbOp
from threading import Thread

class Service:
    def __init__(self, sock_conn):
        self.db_op_ins = dbOp("test.db")
        self.sock_conn = sock_conn
        self.user_id = None

    def start(self):
        t = Thread(target = self._service)
        t.start()

    def _service(self):
        while True:
            recv_raw = self.sock_conn.recv(1024)
            recv_decoded = eval(recv_raw.decode())
            mode = recv_decoded["mode"]

            if mode == "sign_up":
                try:
                    user_name = recv_decoded["name"]
                    password = recv_decoded["pwd"]

                    user_id = self.db_op_ins.get_max_userid() + 1

                    self.db_op_ins.insert_allusertable(user_id, user_name, password, 0)
                    self.db_op_ins.create_msgtable(user_id)
                    self.db_op_ins.create_friendlisttable(user_id)
                    self.db_op_ins.create_friendrequesttable(user_id)

                    self.sock_conn.send(str(user_id).encode())
                except:
                    self.sock_conn.send(b"0")

            elif mode == "sign_in":
                user_id = recv_decoded["id"]
                self.user_id = user_id
                password = recv_decoded["pwd"]


                db_q_dict = self.db_op_ins.query_allusertable(user_id)
                if db_q_dict["PASSWD"] == password:
                    # correct
                    self.sock_conn.send(db_q_dict["USERNAME"].encode())
                    pass
                else:
                    self.sock_conn.send(b"0")

            elif mode == "sign_out":
                self.db_op_ins.update_allusertable()

            elif mode == "add_friend":
                pass

            elif mode == "del_friend":
                pass

            elif "mode" == "send_msg":
                pass

        self.sock_conn.close()
        del self.db_op_ins