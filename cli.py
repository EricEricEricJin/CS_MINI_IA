from curses import *


KEY_TAB = 9
KEY_COLON = 58
KEY_ENTER = 10
KEY_ESC = 27

KEY_CTRL_W = 23

# KEY A - Z: 65-90
# KEY a - z: 97 - 122
# KEY 0-9: 48-57


class CLI:

    

    def __init__(self):
        self.CMD2FUNC_TABLE = {
            "signin": self._cmd_signin,
            "signout": self._cmd_signout,
            "signup": self._cmd_signup,
            "addfriend": self._cmd_addfriend,
            "delfriend": self._cmd_delfriend
        }

        self.msg_data = [
            {"username": "a"}
        ]

        self.normal_left_curs = 0
        self.normal_left_offset = 0

        self.normal_right_offset = 0
        self.normal_right_curs = 0
        

        self.active_win = "left"

    def _init_win(self):
        noecho()
        self.main_win = initscr()
        self.win_size = self.main_win.getmaxyx()

        self.left_win = self.main_win.subwin(self.win_size[0] - 1, int(self.win_size[1] / 3), 0, 0)
        self.right_win = self.main_win.subwin(self.win_size[0] - 1, self.win_size[1] - int(self.win_size[1] / 3), 0, int(self.win_size[1] / 3))
        self.bottom_win = self.main_win.subwin(1, self.win_size[1], self.win_size[0] - 1, 0)

    def run(self):
        while True:
            key = self.main_win.getch()
            if key == ord("a"):
                pass


    def _bottom_line_mode(self):
        self.bottom_win.clear()
        self.bottom_win.addch(0, 0, ":")
        
        command = ":"
        while True:
            key = self.main_win.getch()
            if key == KEY_ENTER:
                break
            elif key == KEY_TAB:
                pass
            elif key == KEY_ESC:
                return 0
            elif 65 <= key <= 90 or 97 <= key <= 122 or 48 <= key <= 57:
                command += chr(key)
            
            self.bottom_win.addstr(0, 0, command)
        
        command = command[1:]

        if command in self.CMD2FUNC_TABLE:
            self.bottom_win.clear()
            self.CMD2FUNC_TABLE[command]()
        else:
            self.bottom_win.clear()
            self.bottom_win.addstr(0, 0, "E492: Not an vichat command: " + command)
            return 0

    def _normal_mode(self):
        while True:
            self.main_win.clear()

            key = self.main_win.getch()
            if key == KEY_CTRL_W:
                self.active_win = "right" if self.active_win == "left" else "left"
            

    def _insert_mode(self):
        pass

    def _normal_refresh(self):
        # Display the self.msg_list in main win
        for i in range(self.win_size[0] - 10):
            un_str = ""
            if self.normal_left_curs - self.normal_left_offset == i:
                un_str += "> "
            else:
                un_str += "  "
            if i + self.normal_left_offset >= len(self.msg_data):
                break
            else:
                un_str += self.msg_data[self.normal_left_offset + i]["username"]
            self.left_win.addstr(i + 5, 0, un_str)

        if self.normal_left_curs < len(self.msg_data):
            current_msg = self.msg_data[self.normal_left_curs + self.normal_left_offset]["message"]
            # current_msg: [["me", xx], "friend", xx]
            pass



    def _cmd_signup(self):
        pass

    def _cmd_signin(self):
        pass

    def _cmd_signout(self):
        pass

    def _cmd_addfriend(self):
        pass

    def _cmd_delfriend(self):
        pass
        
