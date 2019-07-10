import tkinter
from tkinter import messagebox

class ConnectDialog(object):
    def __init__(self, msg=None, default_ip=None, default_port=None):
        root = self.root = tkinter.Tk()
        root.title('Connect to server')

        # main frame
        main_frame = tkinter.Frame(root)
        main_frame.pack(ipadx=2, ipady=2, padx=2, pady=8)

        row_index = 0

        # the message
        if msg and len(msg) > 0:
            message = tkinter.Label(main_frame, text=msg)
            message.grid(row = row_index, columnspan=2, padx=8, pady=8)
            row_index += 1

        def create_labeled_entry(label_text, default_value):
            nonlocal row_index
            label = tkinter.Label(main_frame, text=label_text)
            label.grid(row=row_index, column=0, padx=(8, 0), sticky='w')
            entry = tkinter.Entry(main_frame)
            if default_value:
                entry.insert(0, default_value)
            entry.grid(row=row_index, column=1, padx=(4, 8), sticky='we')
            row_index += 1
            return entry

        # create input fields and set focus
        self.entry_ip = create_labeled_entry("Server IP", default_ip)
        self.entry_port = create_labeled_entry("Port", default_port)
        self.entry_ip.focus_set() # focus the first field

        # button frame
        button_frame = tkinter.Frame(main_frame)
        button_frame.grid(row=row_index, column=1, padx=4, pady=(4, 0), sticky='w')

        # buttons
        btn_connect = tkinter.Button(button_frame, width=8, text="Connect", command=self.clicked_connect)
        btn_connect.pack(side='left')
        btn_cancel = tkinter.Button(button_frame, width=8, text="Cancel", command=self.clicked_cancel)
        btn_cancel.pack(side='left')
        # the enter key will trigger the focused button's action
        self.entry_ip.bind('<KeyPress-Return>', func=self.clicked_connect)
        self.entry_port.bind('<KeyPress-Return>', func=self.clicked_connect)
        btn_connect.bind('<KeyPress-Return>', func=self.clicked_connect)
        btn_cancel.bind('<KeyPress-Return>', func=self.clicked_cancel)
        root.bind('<KeyPress-Escape>', func=self.clicked_cancel)

        # roughly center the box on screen
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        root.update_idletasks()
        xp = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        yp = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        geom = (root.winfo_width(), root.winfo_height(), xp, yp)
        root.geometry('{0}x{1}+{2}+{3}'.format(*geom))
        # call self.close_mod when the close button is pressed
        root.protocol("WM_DELETE_WINDOW", self.clicked_cancel)
        # a trick to activate the window (on windows 7)
        root.deiconify()

    def clicked_connect(self, event=None):
        try:
            ip = self.entry_ip.get().strip()
            if len(ip) <= 0:
                raise RuntimeError('Server address is missing')

            port = self.entry_port.get().strip()
            if len(port) <= 0:
                raise RuntimeError('Port is missing')
            port = int(port)

            self.result = (ip, port)
            self.root.quit()
        except ValueError:
            messagebox.showerror("Error", "Port has to be an integer")
        except RuntimeError as error:
            messagebox.showerror("Error", str(error))

    def clicked_cancel(self, event=None):
        self.result = (None, None)
        self.root.quit()

    @staticmethod
    def show(msg=None, default_ip=None, default_port=None):
        """Create an instance of a ConnectDialog, and get data back from the user.
        msg = optional description to be displayed above the input fields
        """
        dialog = ConnectDialog(msg, default_ip, default_port)
        dialog.root.mainloop()
        # the function pauses here until the mainloop is quit
        dialog.root.destroy()
        return dialog.result