from db_op import dbOp
from threading import Thread
from functools import wraps
import time

def debug(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("== Start func", f.__name__, "==")
        rt  = f(*args, **kwargs)
        print("== Return", rt, "==")
        return rt
    return decorated

class Service:
    @debug
    def __init__(self, sock_conn):
        self.sock_conn = sock_conn
        self.user_id = None

        self.MODE2FUNC = {
            "sign_up": self._sign_up,
            "sign_in": self._sign_in,
            "sign_out": self._sign_out,
            "add_friend": self._add_friend,
            "del_friend": self._del_friend,
            "accept_friend": self._accept_friend,
            "refuse_friend": self._refuse_friend,
            "send_msg": self._send_msg,
            "refresh": self._refresh,
            "close_sock": self._close_sock
        }

        self.recv_decoded = {}
        self.login_status = False

        self.do_serve = True

    @debug
    def start(self):
        t = Thread(target = self._service)
        t.start()

    @debug
    def _service(self):
        self.db_op_ins = dbOp("test.db")

        while self.do_serve:
            try:
                recv_raw = self.sock_conn.recv(4096)
                print("recv_raw", recv_raw)
                try:
                    self.recv_decoded = eval(recv_raw.decode())
                except Exception as e:
                    print("_service_run_error", e, "recv", recv_raw)

                mode = self.recv_decoded["mode"]

                if (mode in self.MODE2FUNC) and (mode == "sign_in" or self.login_status or mode == "sign_up"):
                    self.MODE2FUNC[mode]()
                    print("run_with_mode_dict")
                    
                else:
                    self.sock_conn.send(b"0")
                    print("can't run")
            except:
                break 

        self._sign_out()
        time.sleep(0.2)
        self.sock_conn.close()
        
        del self.db_op_ins

    @debug
    def _sign_up(self):
        print("enter func sign_up")
        try:
            user_name = self.recv_decoded["name"]
            password = self.recv_decoded["pwd"]

            curr_max_id = self.db_op_ins.get_max_userid()
            if curr_max_id == None:
                user_id = 1
            else:
                user_id = curr_max_id + 1

            self.db_op_ins.insert_allusertable(user_id, user_name, password, 0)
            self.db_op_ins.create_msgtable(user_id)
            self.db_op_ins.create_friendlisttable(user_id)
            self.db_op_ins.create_friendrequesttable(user_id)

            self.sock_conn.send(str(user_id).encode())

            return 1
        except Exception as e:
            print(e)
            self.sock_conn.send(b"0")
            return 0
            
    @debug
    def _sign_in(self):
        try:
            password = self.recv_decoded["pwd"]
            user_id = self.recv_decoded["id"]
            db_q_dict = self.db_op_ins.query_allusertable(user_id)
            print("db_q_dict", db_q_dict)

            if db_q_dict["PASSWD"] == password:
                self.user_id = user_id
                # correct send username
                self.db_op_ins.update_allusertable(self.user_id, "LOGIN_STATUS", 1)
                self.login_status = True
                self.sock_conn.send(db_q_dict["USERNAME"].encode())
                return 1
            else:
                raise(Exception("wong_passwd"))
        except Exception as e:
            print(e)
            self.sock_conn.send(b"0")
            return 0

    @debug
    def _sign_out(self):
        try:
            self.db_op_ins.update_allusertable(self.user_id, "LOGIN_STATUS", 0)
            self.login_status = False
            self.sock_conn.send(b"1")
            return 1
        except:
            try:
                self.sock_conn.send(b"0")
            except:
                pass
            return 0

    @debug
    def _add_friend(self):
        try:
            self.db_op_ins.insert_friendrequesttable(self.user_id, self.recv_decoded["friend_id"], self.recv_decoded["req_note"])
            self.sock_conn.send(b"1")
            return 1
        except:
            self.sock_conn.send(b"0")
            return 0
        
    @debug
    def _del_friend(self):
        try:
            self.db_op_ins.delete_friendlisttable(self.user_id, self.recv_decoded["friend_id"])
            self.db_op_ins.delete_friendlisttable(self.recv_decoded["friend_id"], self.user_id)
            self.sock_conn.send(b"1")
            return 1
        except:
            self.sock_conn.send(b"0")
            return 0

    @debug
    def _accept_friend(self):
        try:
            self.db_op_ins.insert_friendlisttable(self.user_id, self.recv_decoded["friend_id"])
            self.db_op_ins.insert_friendlisttable(self.recv_decoded["friend_id"], self.user_id)
            self.db_op_ins.delete_friendrequesttable(self.user_id, self.recv_decoded["friend_id"])
            self.sock_conn.send(b"1")
            return 1
        except:
            self.sock_conn.send(b"0")
            return 0

    @debug
    def _refuse_friend(self):
        try:
            self.db_op_ins.delete_friendrequesttable(self.user_id, self.recv_decoded["friend_id"])
            self.sock_conn.send(b"1")
            return 1
        except:
            self.sock_conn.send(b"0")
            return 0

    @debug
    def _send_msg(self):
        try:
            friend_id = self.recv_decoded["friend_id"]
            if friend_id in self.db_op_ins.query_friendlisttable(self.user_id):
                # are friends
                self.db_op_ins.insert_msgtable(self.recv_decoded["friend_id"], self.user_id, self.recv_decoded["msg"])
                self.sock_conn.send(b"1")
                return 1
            else:
                raise(Exception("not_friend"))
        except:
            self.sock_conn.send(b"0")
            return 0

    @debug
    def _refresh(self):
        # return msg, frl, fl
        # {"msg": [[sender, send_t, msg], [], ...], "freq": [[friend_id, req_note], [], ...], "friend": [[friend_id, friend_username, login_status], [], ...]}

        try:
            message = list(self.db_op_ins.query_msgtable(self.user_id))
            friend_req = list(self.db_op_ins.query_friendrequesttable(self.user_id))
            friends = list(self.db_op_ins.query_friendlisttable(self.user_id))

            # message = [list(message[i].values()) for i in range(len(message))]
            # msg_data = {}
            # for i in range(len(message)):
            #     sender_id = ess
            #     msg_data_of_this_sender = []

            #     msg_data.update({
            #         message[i]["SENDER_ID"]: 
            #     })
            # friend_req = [list(friend_req[i].values()) for i in range(len(friend_req))]
            # friends = [[friends[i], self.db_op_ins.query_allusertable(friends[i])["USERNAME"], self.db_op_ins.query_allusertable(friends[i])["LOGIN_STATUS"]] for i in range(len(friends))]

            msg_data = {}
            freq_data = {}
            friend_data = {}

            for i in range(len(message)):
                sender_id = message[i]["SENDER_ID"]
                if sender_id in msg_data:
                    msg_data[sender_id].append(
                        [True, message[i]["TIME"], message[i]["MSG"]]
                    )
                else:
                    msg_data.update({
                        sender_id: [[True, message[i]["TIME"], message[i]["MSG"]]]
                    })

            for i in range(len(friends)):
                friend_info = self.db_op_ins.query_allusertable(friends[i])
                friend_data.update({
                    friends[i]: [
                        friend_info["USERNAME"], friend_info["LOGIN_STATUS"] 
                    ]
                })

            for i in range(len(friend_req)):
                freq_data.update({
                    friend_req[i]["FRI_ID"]: friend_req[i]["REQ_NOTE"]
                })

            data = {"msg": msg_data, "freq": freq_data, "friend": friend_data}

            self.sock_conn.send(str(data).encode())

            self.db_op_ins.erase_msgtable(self.user_id)
            
            return 1
        except Exception as e:
            print(e)
            self.sock_conn.send(b"0")
            return 0

    @debug
    def _close_sock(self):
        self.do_serve = False