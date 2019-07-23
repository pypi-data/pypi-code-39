try:
    from _tkinter import DONT_WAIT
except ImportError:
    DONT_WAIT = 2 # What magic is this.
import time

def run_every(root, delay):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            out = fn(*args, **kwargs)
            root.after(delay, wrapper)
            return out
        root.after(delay, wrapper)
        return wrapper
    return decorator

def pause(root, millis, step=0):
    start = time.time()
    # root.update()
    print('Pausing...')
    ct = 0
    while time.time() - start < millis / 1000:  # round w/ step! todo
        # time.sleep(step / 1000)

        root.update_idletasks()  # Force process tasks that have changed (probably just events)
        root.dooneevent(DONT_WAIT)
        ct += 1
    end = time.time()
    print('Elapsed: {}'.format(end - start))
    print('Handled', ct, 'events')



# # Desktop
# ## From desktop
# import tkinter as tk

# root = tk.Tk()



# def onkeypress(letter):
#     foobar

# @campy.register(letter, function)
# root.configure('windowclose')

# @campy.register_onmouseclick()

# ball = [4, 5]

# # every one of these needs a collection of listeners.
# # action events are bound to interactors.


# @slider.onclick()


# @run_every(1000)
# def say_hello():
#     print('Hello!')
#     ball[0] += 1
#     print(ball)

# print(say_hello)


# root.mainloop()

# import tkinter as tk
# root = tk.Tk()

# def callback(event):
#     frame.focus_set()
#     print('mouse-clicked')

# frame = tk.Frame(root, width=100, height=100)
# frame.bind("<Button-1>", callback)
# frame.pack()
# root.lift()
# # root.update()


# DELAY = 1000
# start = time.time()
# pause(DELAY)
# end = time.time()
# print('Desired delay: {}. Elapsed: {}'.format(DELAY, end-start))
