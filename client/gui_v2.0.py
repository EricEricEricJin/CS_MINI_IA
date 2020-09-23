from tkinter import *
from logic_proc import *
from tkinter.ttk import *
import timeout_decorator

class GUI:
    BUTTON_H = 20
    BUTTON_W = 80
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.root = Tk()
        self.root.geometry("{}x{}".format(w, h))

        self.logic_proc_ins = logicProc()

        self._init_ui()

    def _init_ui(self):
        # Friend treeview
        self.friend_treeview = Treeview(master = self.root, columns = ("Friends"), show = "headings")
        self.friend_treeview.heading("#0", text = "Friends")
        self.friend_treeview.column("#0", width = int(self.w / 4))
        self.friend_treeview.place(x = 0, y = self.BUTTON_H)
        
        # Scrollbar for friend treeview
        friend_tv_scrollbar = Scrollbar(master = self.root)
        friend_tv_scrollbar.place(x = int(self.w / 4), y = self.BUTTON_H, height = self.h - self.BUTTON_H, width = 10)
        friend_tv_scrollbar.config(command = self.friend_treeview.yview)
        self.friend_treeview.configure(yscrollcommand = friend_tv_scrollbar.set)

        # Display text field
        self.display_msg_box = Text(master = self.root, height = int(self.h - 2 * self.BUTTON_H), width = int(self.w / 4 * 3 - 10))
        self.display_msg_box.place(x = int(self.w / 4 + 10), y = self.BUTTON_H)

        # Display input_box
        self.input_box = Entry(master = self.root, width = int((self.w * (3 / 4) - 10 - 3 * self.BUTTON_W) / 18))
        self.input_box.place(x = int(self.w / 4 + 10 + 2 * self.BUTTON_W), y = self.h - self.BUTTON_H)


        # View all friends button
        self.view_all_friends_bt = Button(master = self.root, text = "All friends", command = self._view_all_friends_bt_clicked)
        self.view_all_friends_bt.place(x = 0, y = 0)

        # Login / logout button
        self.loginout_bt = Button(master = self.root, text = "Login in", command = self._loginout_bt_clicked)
        self.loginout_bt.place(x = int(self.w / 4 + 10), y = 0)
        
        # remove from friend_tv button
        self.rm_selected_from_friend_treeview_bt = Button(master = self.root, text = "Remove from list", command = self._rm_selected_from_friend_treeview_bt_clicked)
        self.rm_selected_from_friend_treeview_bt.place(x = int(self.w / 4) + 10, y = self.h - self.BUTTON_H)

        # erase selected history button
        self.clear_selected_history_bt = Button(master = self.root, text = "Clear history", command = self._clear_selected_history_bt_clicked)
        self.clear_selected_history_bt.place(x = int(self.w / 4 + 10 + self.BUTTON_W), y = self.h - self.BUTTON_H)

        # send button
        self.send_bt = Button(master = self.root, text = "Send", command = self._send_bt_clicked)
        self.send_bt.place(x = self.w - self.BUTTON_W, y = self.h - self.BUTTON_H)

    def run(self):
        self.root.after(20, self._refresh)
        self.root.mainloop()

    def _refresh(self):
        pass

    def _loginout_bt_clicked(self):
        if self.logic_proc_ins.login_status == ONLINE:
            self.logic_proc_ins.sign_out()
        else:
            LOGINOUT_WIN_W = 200
            LOGINOUT_WIN_H = 150

            top = Toplevel()
            top.geometry("{}x{}".format(LOGINOUT_WIN_W, LOGINOUT_WIN_H))

            Label(top, text = "ID:").place(x = 0, y = 0)
            Label(top, text = "PWD:").place(x = 0, y = int(LOGINOUT_WIN_H / 3))

            id_entry = Entry(top, width = 20)
            pwd_entry = Entry(top, width = 20)

            id_entry.place(x = int(LOGINOUT_WIN_W / 4), y = 0)
            pwd_entry.place(x = int(LOGINOUT_WIN_W / 4), y = int(LOGINOUT_WIN_H / 3))

            def _cancel():
                top.destroy()
            
            def _login():
                user_id = id_entry.get()
                pwd = pwd_entry.get()

                try:
                    user_id = int(user_id)
                    if pwd == "":
                        raise(Exception)
                except:
                    warning = Toplevel()
                    Message(warning, text = "Invalid input!").pack()
                    def destroy_warning():
                        warning.destroy()
                    Button(warning, text = "OK", command = destroy_warning).pack()
                    return

                # print("SIGN IN")
                try:
                    sign_in_rt = self.logic_proc_ins.sign_in(user_id, pwd)
                    if sign_in_rt != 1:
                        raise(Exception)
                except:
                    warning = Toplevel()
                    Message(warning, text = "Login failed").pack()
                    def destroy_warning_1():
                        warning.destroy()
                    Button(warning, text = "OK", command = destroy_warning_1).pack()
                    return
                else:
                    top.destroy()
                

            Button(top, text = "CANCEL", command = _cancel).place(x = 0, y = int(LOGINOUT_WIN_H / 3 * 2))
            Button(top, text = "LOGIN", command = _login).place(x = int(LOGINOUT_WIN_W / 2), y = int(LOGINOUT_WIN_H / 3 * 2))



    def _view_all_friends_bt_clicked(self):
        pass

    def _rm_selected_from_friend_treeview_bt_clicked(self):
        pass

    def _clear_selected_history_bt_clicked(self):
        pass

    def _send_bt_clicked(self):
#         self.logic_proc_ins.send_message()
        pass

if __name__ == "__main__":
    GUI_ins = GUI(1200, 800)
    GUI_ins.run()