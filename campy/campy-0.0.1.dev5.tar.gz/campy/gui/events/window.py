"""Wrapper around events that relate to window lifecycle.

There are two main types of window events that a caller can subscribe to:

- WindowClosed: The graphical window was closed.
- WindowResized: The graphical window was resized.
"""

def register_on_window_resize():
    self.bind("<Configure>", self.on_resize)


"""Define decorators for all of the common types of events."""

root = tk.Tk()

def on_window_closed(root=None):
    pass

def on_window_resize():
    root.bind()
    '<Configure>'


## USAGE

@on_window_closed()

@on_window_resize()
def resized_window(event):
    print(event.height, event.width)


# root.configure('windowclose')

