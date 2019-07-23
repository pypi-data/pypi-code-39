"""Wrapper around events that relate to window lifecycle.

There are two main types of window events that a caller can subscribe to:

- WindowClosed: The graphical window was closed.
- WindowResized: The graphical window was resized.
"""
import campy.private.platform as _platform

# class WindowEvent:

def register_on_window_resize():
    self.bind("<Configure>", self.on_resize)


"""Define decorators for all of the common types of events."""
def onwindowclosed():
    pass

def onwindowresized():
    pass
