## THIS IS A FAKE FOR DEBUG PURPOSE ##

from sock_com import sockCom
from db_op import dbOp
import datetime
from functools import wraps

def debug(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("start func", f.__name__)
        print("args", args, kwargs)
        rt  = f(*args, **kwargs)
        print("return", rt)
        return rt
    return decorated


ONLINE = 1
OFFLINE = 0

class logicProc:
    @debug
    def __init__(self):
        self.login_status = 0

    @debug
    def connect(self):
        pass

    @debug
    def sign_up(self, user_id, passwd):
        return "HAMA" # username 

    @debug
    def sign_in(self, user_id, passwd):
        self.login_status = 1
        return 1

    @debug
    def sign_out(self):
        self.login_status = 0
        return 1

    @debug
    def add_friend(self, friend_id, req_note):
        return 1

    @debug
    def del_friend(self, friend_id):
        return 1

    @debug
    def accept_friend(self, friend_id):
        return 1

    @debug
    def refuse_friend(self, friend_id):
        return 1
        
    @debug
    def send_message(self, friend_id, msg):
        return 1

    @debug
    def refresh(self):
        # Put new messages into database
        # Fatch ALL from data base
        # return
        # {"msg": [[sender, send_t, msg], [], ...], "freq": [[friend_id, req_note], [], ...], "friend": [[friend_id, friend_username, login_status], [], ...]}
        # {"msg": {id: [[sender, time, msg]]}, "freq": {id: note}, "friend": {id: [name, status]}}

        return {
            "msg": {
                114514: [[True, datetime.datetime.now(), "HAMA"], [False, datetime.datetime.now(), "ELSB"]],
                1919810: [[False, datetime.datetime.now(), "JZM"], [True, datetime.datetime.now(), "XXWN"]]
            },

            "freq": {
                456: "i'm456",
                789: "i'm789"
            },

            "friend": {
                114514: ["yy", 1],
                1919810: ["ut", 0]
            }
        }

    @debug
    def clear_history(self, friend_id):
        return 1
        pass
