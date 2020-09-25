from tkinter import *
root = Tk()
def f():
    root.geometry("20x20")
    print("A")

root.after(50, f)
root.mainloop()