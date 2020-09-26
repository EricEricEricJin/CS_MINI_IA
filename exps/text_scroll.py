from tkinter import *
from tkinter.scrolledtext import ScrolledText

root = Tk()
t = ScrolledText(root, height = 10, width = 10)
t.pack()
t.insert(END, """
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
a
a
a
a
a
a
a
a
a
a
a
a
a
""")
t.mainloop()