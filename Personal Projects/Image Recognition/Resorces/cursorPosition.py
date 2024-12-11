import pyautogui
import time
from screeninfo import get_monitors

# Get the screen's information (top, left, width, height)
monitor = get_monitors()[0]  # Assumes you're working with the primary monitor

top = monitor.y
left = monitor.x
width = monitor.width
height = monitor.height

# Get the cursor position
while True:
    cursor_x, cursor_y = pyautogui.position()

    # Display the information
    print(f"Screen position: Top = {top}, Left = {left}, Width = {width}, Height = {height}")
    print(f"Cursor position: X = {cursor_x}, Y = {cursor_y}")
    time.sleep(1)