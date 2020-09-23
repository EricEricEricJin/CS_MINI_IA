from tkinter import *
from logic_proc import *
from tkinter.ttk import *


class GUI:
    BUTTON_H = 20
    BUTTON_W = 80
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.msg_list = {} # {id: [sender, time, msg], ...}

        self.friend_list = {} # {id: [username, login_status], ...}

        self.friend_req_list = {} # {id: req_note, ...}

        self.root = Tk()
        self.root.geometry("{}x{}".format(w, h))

        self.logic_proc_ins = logicProc()

        self._init_ui()

    def _init_ui(self):
        # Friend treeview
        self.friend_treeview = Treeview(master = self.root, columns = ("Friends_ID", "Friends_Name"), show = "headings")
        self.friend_treeview.heading("#1", text = "ID")
        self.friend_treeview.heading("#2", text = "Name")
        self.friend_treeview.column("#1", width = int(self.w / 8))
        self.friend_treeview.column("#2", width = int(self.w / 8))
        self.friend_treeview.place(x = 0, y = self.BUTTON_H)
        self.friend_treeview.bind("<<TreeviewSelect>>", self._friend_treeview_select_change)
        
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

        # Friend request
        self.friend_request_bt = Button(master = self.root, text = "Request", command = self._friend_request_bt_clicked)
        self.friend_request_bt.place(x = self.BUTTON_W, y = 0)

        # Add friend
        self.add_friend_bt = Button(master = self.root, text = "Add friend", command = self._add_friend_bt_clicked)
        self.add_friend_bt.place(x = 2 * self.BUTTON_W, y = 0)

        # Login / logout button
        self.loginout_bt = Button(master = self.root, text = "Login in", command = self._loginout_bt_clicked)
        self.loginout_bt.place(x = 3 * self.BUTTON_W, y = 0)
        
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
        data = self.logic_proc_ins.refresh()

        # Interprete data
        # {"msg": [[sender, send_t, msg], [], ...], "freq": [[friend_id, req_note], [], ...], "friend": [[friend_id, friend_username, login_status], [], ...]}

        self.msg_list = data["msg"]
        self.friend_list = data["friend"]
        self.friend_req_list = data["freq"]
        
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

    def _friend_treeview_select_change(self, event):
        # update selected
        selected = event.widget.selection()[0]
        sel_friend_id = self.friend_treeview.item(selected)["values"][0]

        msg = self.msg_list[sel_friend_id]
        
        self.display_msg_box.delete("1.0", "end")

        for i in range(len(msg)):
            self.display_msg_box.insert(END, str(msg[i]))

        pass

    def _view_all_friends_bt_clicked(self):
        AF_WIN_W = int(self.w / 2)
        AF_WIN_H = int(self.h / 2)

        def _selected_friend_id():
            iid = all_friends_tree.selection()[0]
            return all_friends_tree.item(iid)["values"][0]

        def _all_friends_tree_select_change(event):
            pass

        def _del_friend_bt_clicked():
            self.logic_proc_ins.del_friend(
                _selected_friend_id()
            )
            self._refresh()

        def _send_msg():
            pass

        top = Toplevel()
        top.geometry("{}x{}".format(AF_WIN_W,AF_WIN_H))
        all_friends_tree = Treeview(top, columns = ("ID", "Name", "Status"), show = "headings")
        
        all_friends_tree.heading("#1", text = "ID")
        all_friends_tree.heading("#2", text = "Name")
        all_friends_tree.heading("#3", text = "Status")

        all_friends_tree.column("#1", width = int(AF_WIN_W / 3))
        all_friends_tree.column("#2", width = int(AF_WIN_W / 3))
        all_friends_tree.column("#3", width = int(AF_WIN_W / 3))

        for fri_id in list(self.friend_list.keys()):
            all_friends_tree.insert("", "end", values = [
                fri_id,
                self.friend_list[fri_id][0],
                self.friend_list[fri_id][1]
            ])
        
        all_friends_tree.pack()
        # TODO: add scroll bar

        Button(master = top, text = "Delete", command = _del_friend_bt_clicked).pack()
        Button(master = top, text = "SendMSG", command = _send_msg).pack()

    def _rm_selected_from_friend_treeview_bt_clicked(self):
        pass

    def _clear_selected_history_bt_clicked(self):
        pass

    def _send_bt_clicked(self):
      #   self.logic_proc_ins.send_message()
        pass

    def _friend_request_bt_clicked(self):
        FR_WIN_W = int(self.w / 2)
        FR_WIN_H = int(self.h / 2)

        top = Toplevel()
        top.geometry("{}x{}".format(FR_WIN_W, FR_WIN_H))

        friend_req_tree = Treeview(top, columns = ("ID", "Req_Note"), show = "headings")
        friend_req_tree.place(x = 0, y = 0)

        friend_req_tree.heading("#1", text = "ID")
        friend_req_tree.heading("#2", text = "Req_Note")
        friend_req_tree.column("#1", width = int(FR_WIN_W / 2))
        friend_req_tree.column("#2", width = int(FR_WIN_W / 2))

        for fri_id in list(self.friend_req_list.keys()): # []
            friend_req_tree.insert("", "end", values = [fri_id, self.friend_req_list[fri_id]])

        def _select_react(event):
            selected = event.widget.selection()[0]
            fri_id = friend_req_tree.item(selected)["values"][0]
            
            def _refresh():
                pass

            def _accept():

                if self.logic_proc_ins.accept_friend(fri_id) == 1:
                    self._refresh()
                    _refresh()
                    return
                    
                    # success
                else:
                    warning = Toplevel()
                    Message(warning, text = "Fail!").pack()
                    Button(warning, text = "Ok", command = lambda: warning.destroy()).pack()
                    return

            def _refuse():
                if self.logic_proc_ins.refuse_friend(fri_id) == 1:
                    self._refresh()
                    _refresh()
                    return
                else:
                    warning = Toplevel()
                    Message(warning, text = "Fail!").pack()
                    Button(warning, text = "Ok", command = lambda: warning.destroy()).pack()
                    return


            confirm_msgbox = Toplevel()
            Button(confirm_msgbox, text = "Accept", command = _accept).pack()
            Button(confirm_msgbox, text = "Refuse", command = _refuse).pack()


        friend_req_tree.bind("TreeviewSelect", _select_react)

    def _add_friend_bt_clicked(self):
        ADDF_WIN_W = 200
        ADDF_WIN_H = 150
        top = Toplevel()
        top.geometry("{}x{}".format(ADDF_WIN_W, ADDF_WIN_H))

        Label(top, text = "Friend ID").place(x = 0, y = 0)
        Label(top, text = "Note").place(x = 0, y = int(ADDF_WIN_H / 3))

        friend_id_ent = Entry(master = top, width = 20)
        friend_id_ent.place(x = int(ADDF_WIN_W / 2), y = 0)

        req_note_ent = Entry(master = top, width = 20)
        req_note_ent.place(x = int(ADDF_WIN_W / 2), y = int(ADDF_WIN_H / 3))


        def _cancel():
            top.destroy()
            return

        def _add():

            try:
                fri_id = int(friend_id_ent.get())
                req_note = req_note_ent.get()
            except:
                warning = Toplevel()
                Message(warning, text = "Invalid input!").pack()
                def destroy_warning():
                    warning.destroy()
                Button(warning, text = "OK", command = destroy_warning).pack()
                return

            try:
                rt = self.logic_proc_ins.add_friend(fri_id, req_note)
                if rt != 1:
                    raise(Exception)
            except:
                warning = Toplevel()
                Message(warning, text = "Failed to add friend").pack()
                def destroy_warning_1():
                    warning.destroy()
                Button(warning, text = "OK", command = destroy_warning_1).pack()
                return
            else:
                top.destroy()
                return

        Button(top, text = "Cancel", command = _cancel).place(x = 0, y = int(ADDF_WIN_H / 3 * 2))
        Button(top, text = "Add", command = _add).place(x = int(ADDF_WIN_W / 2), y = int(ADDF_WIN_H / 3 * 2))

if __name__ == "__main__":
    GUI_ins = GUI(1200, 800)
    GUI_ins.run()