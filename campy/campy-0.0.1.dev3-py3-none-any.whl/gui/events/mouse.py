"""Interact with the graphics libraries via mouse events.

- MOUSE_CLICKED
- MOUSE_PRESSED
- MOUSE_RELEASED
- MOUSE_MOVED
- MOUSE_DRAGGED
"""
from campy.private.platform

def onmousemotion(function):


mouse_click_event = None

def onmousepress(root, button=1):
    def decorator(function):
        root.bind('<Button-{}>'.format(button), mouse_clicked)
        return function
    return decorator

def onmousemotion(root, button=1):
    def decorator(function):
        # Really, add function to a list of handlers and dispatch ourselves.
        root.bind('<Motion>', function)
        return function
    return decorator

def onmousedragged(root, button=1):
    def decorator(function):
        root.bind('<B{}-Motion>'.format(button), mouse_dragged)
        return function
    return decorator

def mouse_clicked(event, function):
    global mouse_click_event  # Everyone writing and reading at the same time. What could go wrong?
    mouse_click_event = event
    print('Clicked')
    # print(event.__dict__)

def mouse_moved(event):
    import random
    print('Moved' + str(random.random()))
    # pass
    # print(event.__dict__)

def mouse_dragged(event):
    print('Dragged')
    # print(event.__dict__)

# import tkinter as tk
# root = tk.Tk()

# @onmousemotion(root)
# def foobar():
#     print('hello there')

# root.lift()
# root.mainloop()
