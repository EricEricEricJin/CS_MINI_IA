from tkinter import *
from tkinter.ttk import *

def react(event):
    selected = event.widget.selection()[0]
    print(selected)
    print(tv.item(selected))

root = Tk()

tv = Treeview(root, columns = ("A", "B"), show = "headings")
tv.place(x = 0, y = 0)
tv.heading("#0", text = "a")
tv.heading("#1", text = "b")

tv.column("#0")
tv.column("#1")

tv.insert("", "end", values = [111,222])
tv.bind("<<TreeviewSelect>>", react)

root.mainloop()
