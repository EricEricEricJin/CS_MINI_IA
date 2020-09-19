#列表的事件处理
#之前我们有提到过回调函数，比如按键的回调函数，当按下按键时执行回调函数里面的代码
#但是列表没有回调函数这么一说，他有的是事件，当我双击列表了，就触发了列表的双击事件，就要对此作出处理
#我们现在来试试，如何双击列表的某个元素时，将其删除

# from tkinter import *

# window = Tk()

# list = Listbox(window,width=20,height=10,selectmode = EXTENDED)
# list.pack()
# def delete_index(event):
#     list.delete(list.curselection())
# list.bind('<Double-Button-1>',delete_index)
# #bind()就是我们定义事件处理的方法，'<Double-Button-1>'指的是双击事件，当事件触发时就调用delete_index
# #事件的详细讲解会做专题讲解
# list.insert(0,'1','2','3','4','5')

# window.mainloop()


from threading import Thread
from tkinter import *

def f():
    while True:
        # lb.delete(0, "end")
        # lb.insert(0, "HAMA", "WEINI")
        lb.selection_set(0, 0)
        print(lb.curselection())

window = Tk()
window.geometry("800x600")

lb = Listbox(window, height = 600, width = 800, selectmode = EXTENDED)
lb.place(x = 0, y = 0)

lb.insert(0, "HAMA", "WEINI")

t = Thread(target = f)
t.start()


window.mainloop()

