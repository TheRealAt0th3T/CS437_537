import curses
import time

curses.initscr()
# Turn off line buffering
curses.cbreak()

# Initialize the terminal
win = curses.initscr()

# Make getch() non-blocking
win.nodelay(True)

while True:
    key = win.getch()
    if key != -1:
        print('Pressed key', key)
    time.sleep(0.01)