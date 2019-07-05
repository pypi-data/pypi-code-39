from tkinter import *

class StatusBar(Frame):   
    def __init__(self, master):
        Frame.__init__(self, master)
        self.variable=StringVar()        
        self.label=Label(self, border=1, relief=SUNKEN, anchor=W,
                            textvariable=self.variable,
                            font=('arial',12,'normal'))
        self.label.pack(fill=X, ipadx=4, ipady=4)

    def set_text(self, text):
        self.variable.set(text)

    def get_text(self):
        return self.variable.get()