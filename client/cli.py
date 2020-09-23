from logic_proc import logicProc

class CLI:
    def __init__(self):
        self.LP_ins = logicProc()
        

        self.LP_ins.connect()

    def run(self):
        while True:
            in_str = input(">>> ")
            if in_str == "signin":
                user_id = input("User name: ")
                passwd = input("Password: ")
                print(self.LP_ins.sign_in(user_id, passwd))

            elif in_str == "signup":
                user_name = input("User name: ")
                passwd = input("Password")
                print(self.LP_ins.sign_up(user_name, passwd))

            elif in_str == "signout":
                print(self.LP_ins.sign_out())

            elif in_str == "addfriend":
                friend_id = input("Friend id: ")
                req_note = input("Req note: ")
                print(self.LP_ins.add_friend(int(friend_id), req_note))

            elif in_str == "delfriend":
                friend_id = input("Friend id: ")
                print(self.LP_ins.del_friend(friend_id))

            elif in_str == "sendmsg":
                friend_id = input("Friend id")
                msg = input("Message: ")
                print(self.LP_ins.send_message(friend_id, msg)


if __name__ == "__main__":
    CLI_ins = CLI()
    CLI_ins.run()
    