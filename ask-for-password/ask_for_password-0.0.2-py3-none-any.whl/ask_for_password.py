from tkinter import Tk, Label, Button, Entry, Frame



class AskForPassword:
    __has_instance = 0
    def __init__(self,**kws):
        """
        Constructor method

        Some arguments may be input as a dictionary as follows:
            user = "User_label"             # default is "User:"
            passw = "Pass_label"            # default is "Password:"
            asterisk = "\u263a"             # default is "*"
            ok = "OK_button"                # default is "OK"
            cancel = "Cancel_button"        # default is "Cancel"
            wtitle = "Window_title"         # default is "Type your password"
            caps_on = "Caps_Locked_label"   # default is "CAPS LOCKED"
            caps_off = "Caps_Unlocked_label"# default is "caps unlocked"
            
        """        
        kws.setdefault('user','User:')
        kws.setdefault('passw','Password:')
        kws.setdefault('asterisk','*')
        kws.setdefault('ok','OK')
        kws.setdefault('cancel','Cancel')
        kws.setdefault('wtitle','Type your password')
        kws.setdefault('caps_on','CAPS LOCKED')
        kws.setdefault('caps_off','caps unlocked')
        self.__kws = kws
        if AskForPassword.__has_instance == 0:
            largura_botoes = 15
            largura_entries = 30
            
            self.__user_pass = ['','']
            
            self.__tk = Tk()        
            self.__tk.title(kws['wtitle'])
            self.__tk.bind("<Key>", self.__key)

            self.__frame_entries = Frame(self.__tk,pady=10,padx=20)
            self.__frame_capital = Frame(self.__tk)
            self.__frame_buttons = Frame(self.__tk,pady=10,padx=20)
            self.__frame_entries.pack()
            self.__frame_capital.pack()
            self.__frame_buttons.pack()
            ## entries
            self.__user_label = Label(self.__frame_entries,text=kws['user'])
            self.__user_label.grid(row=0,column=0)            

            self.__user_entry = Entry(self.__frame_entries)
            self.__user_entry['width'] = largura_entries
            self.__user_entry.grid(row=0,column=1)
            self.__user_entry.focus()

            self.__pass_label = Label(self.__frame_entries,text=kws['passw'])
            self.__pass_label.grid(row=1,column=0)

            self.__pass_entry = Entry(self.__frame_entries,show=kws['asterisk'])
            self.__pass_entry['width'] = largura_entries
            self.__pass_entry.grid(row=1,column=1)
            ## capital
            self.__capital = Label(self.__frame_capital)
            self.__capital['fg'] = 'red'
            self.__capital.pack()
            
            ## buttons
            
            self.__button_ok = Button(self.__frame_buttons,text=kws['ok'])
            self.__button_ok['width'] = largura_botoes
            self.__button_ok['command'] = self.__retornook
            self.__button_ok.grid(row=0,column=0)
            
            
            self.__button_cancel = Button(self.__frame_buttons,text=kws['cancel'])            
            self.__button_cancel['width'] = largura_botoes
            self.__button_cancel['command'] = self.__retornocancel
            self.__button_cancel.grid(row=0,column=1)
            
            self.__tk.protocol('WM_DELETE_WINDOW', self.__retornocancel)
            AskForPassword.__has_instance = 1
            self.__tk.mainloop()
            
    def __retornocancel(self):
        AskForPassword.__has_instance = 0
        self.__tk.destroy()
        self.__tk.quit()

    def __retornook(self):
        AskForPassword.__has_instance = 0
        self.__user_pass = (self.__user_entry.get(),AskForPassword.crypto(self.__pass_entry.get()))
        self.__tk.destroy()
        self.__tk.quit()
        
        

    def get(self):
        """This method returns a list [user,password] or ['',''] if canceled."""
        return self.__user_pass

    def has_user_pass(self,user_pass_list):
        """This method asserts whether 'user_pass_list' has a pair (user,password) correct."""
        User, Passw = self.__user_pass
        try:
            for user,passw in user_pass_list:
                if User==str(user) and Passw==str(passw):
                    return True
        except Exception as e:
            print('AskForPassword.has_user_pass:ERROR:',e)
            print(f'The {str(type(user_pass_list))[7:-1]} argument is invalid. Please, try a list of tuples, for example.')
            return None
        return False

    def __key(self,event):
        if event.keycode in [66] and event.state == 0:
            self.__capital['text'] = self.__kws['caps_on']
        elif event.keycode in [66] and event.state != 0:
            self.__capital['text'] = self.__kws['caps_off']
            
            

    def crypto(passw):
        """
        This method needs to be implemented to do encryption. It receives a string.
        You can implement, for example, by doing:

        def new_crypto(string):
            ans = ''
            for letter in string:
                ans += str(ord(letter)-103)
            return ans

        AskForPassword.crypto = new_crypto

        Now, you can use the method 'get()' and it returns [user,crypto_pass].
        """
        return passw
        
    





