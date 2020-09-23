## THIS IS A FAKE FOR DEBUG PURPOSE ##

from sock_com import sockCom
from db_op import dbOp
import datetime
from functools import wraps

def debug(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("== Start func", f.__name__, "==")
        rt  = f(*args, **kwargs)
        print("== Return", rt, "==")
        return rt
    return decorated



ONLINE = 1
OFFLINE = 0

class logicProc:
    @debug
    def __init__(self):
        pass

    @debug
    def connect(self):
        pass

    @debug
    def sign_up(self, user_id, passwd):
        return "HAMA" # username 

    @debug
    def sign_in(self, user_id, passwd):
        return 1

    @debug
    def sign_out(self):
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
        # 

        return {
            "msg": [
                {114514: [datetime.datetime.now(), "HAMA"]},
                {1919810: [datetime.datetime.now(), "JZM"]}
            ],

            "freq": [
                {456: "i'm456"},
                {789: "i'm789"}
            ],

            "friend": [
                {114514: ["yy", 1]},
                {1919810: ["ut", 0]}
            ]
        }

