from curses import *
stdwin = initscr()
stdwin.box()
noecho()
while True:
    key = stdwin.getch()
    stdwin.clear()
    stdwin.addstr(0, 0, str(key))
    