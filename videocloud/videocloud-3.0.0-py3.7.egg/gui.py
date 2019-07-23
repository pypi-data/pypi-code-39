import tkinter as tk

master = tk.Tk()
master.geometry("600x300")
tk.Label(master, text="Video URL").grid(row=0)
tk.Label(master, text="Font").grid(row=1)

e1 = tk.Entry(master)
e2 = tk.Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

master.mainloop()
