from tkinter import *
from tkinter.ttk import *
import sqlite3
import datetime
from logic_proc import logicProc
import global_var 

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("800x600")
    
class messageFrame:
    def __init__(self, master, x, y, w, h, logic_proc_ins, db_op_ins):
        self.x = x
        self.y = y

        self.logic_proc_ins = logic_proc_ins
        self.db_op_ins = db_op_ins
        # {
        #   sender_1: [[], [], ...],
        #   ... 
        # }

        self.msg_data = {}
        # {
        #   "114514": [
        #    ["19260816", "LAOHAMAA"]
        # ]
        # } 
        self.frame = Frame(master = master)

        self.friend_list = Treeview(master = master, columns = ("Friends"), show = "headings")
        self.friend_list.bind("<Button-1>", self._friend_list_clicked)

        self.msg_textbox = Text(master = master)
        self.input_box = Entry(master = master)

        self.send_bt = Button(master = master, command = self._send_bt_clicked)
        self.clear_history_bt = Button(master = master, command = self._clear_history_bt_clicked)
        self.rm_from_list_bt = Button(master = master, command = self._rm_from_list_bt_clicked)

        self.friend_list.heading("#0", text = "Friends")


        self.friend_selected = None


    def pack(self):
        self.frame.place(x = self.x, y = self.y)

    def pack_forget(self):
        pass

    def add_msg(self, sender_id, time, msg):
        if sender_id in self.msg_data:
            self.msg_data[sender_id].append([time, msg])
        else:
            self.msg_data.update({sender_id: [[time, msg]]})
        

        
    def _friend_list_clicked(self):
        # clear text box
        # add data into textbox
        # upgrade selected 
        self.friend_selected = self.friend_list.selection()[0]

        self.msg_textbox.delete("1.0", "end")

        self.msg_textbox.insert(END, self._fmt_msgdata_to_str(self.msg_data))

        pass

    

    def _send_bt_clicked(self):
        # put into db
        # send to server
        friend_id = self.friend_selected
        msg = self.msg_textbox.get("0", "end")
        self.logic_proc_ins.send_message(friend_id, msg)
        self.db_op_ins.insert_msgtable(friend_id, datetime.datetime.now(), msg)

    def _clear_history_bt_clicked(self):
        sender_id = self.friend_selected
        del self.msg_data[sender_id]
        self.db_op_ins.delete_msgtable(sender_id)

    def _rm_from_list_bt_clicked(self):
        items = self.friend_list.selection()
        for item in items:
            self.friend_list.delete(item)

    def _insert_friend_list_ontop(self, text):
        self.friend_list.insert("", index = TOP, text = text)

    def _fmt_msgdata_to_str(self, msg_data):
        return str(msg_data) # temporary debug



class friendFrame:
    def __init__(self, master):
        self.frame = Frame(master = master)

    def pack(self):
        pass

    def pack_forget(self):
        pass

    def init_frame(self):
        pass

    def refresh(self):
        pass

    def _add_clicked(self):
        # Top view
        # Entry box: friend_id
        # Button: confirm, cancel
        pass

    def _del_clicked(self):
        # Top view
        # Button: confirm, cancel
        pass

    def _chat_clicked(self):
        # Turn to msg frame
        pass

class aboutmeFrame:
    def __init__(self):
        pass

    def pack(self):
        pass

    def pack_forget(self):
        pass

