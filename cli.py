from curses import *


KEY_TAB = 9
KEY_COLON = 58
KEY_ENTER = 10
KEY_ESC = 27

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

        self.active_win = "left"

    def _init_win(self):
        noecho()
        self.main_win = initscr()
        self.win_size = self.main_win.getmaxyx()

        self.left_win = self.main_win.subwin(self.win_size[0] - 1, int(self.win_size[1] / 3), 0, 0)
        self.right_win = self.main_win.subwin(self.win_size[0] - 1, self.win_size[1] - int(self.win_size[1] / 3), 0, int(self.win_size[1] / 3))
        self.bottom_win = self.main_win.subwin(1, self.win_size[1], self.win_size[0] - 1, 0)

    def run(self):
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
        pass

    def _insert_mode(self):
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
        
