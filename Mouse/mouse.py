import win32api, win32con
from time import sleep
def move():
	x, y = win32api.GetCursorPos()
	sleep(0.1)
	win32api.SetCursorPos((x+5,y+5))
	sleep(0.1)
	win32api.SetCursorPos((x,y))

	
while True:
	sleep(1)
	move()