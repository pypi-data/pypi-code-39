"""

Ask for Password GUI Interface
===========================

Based on Tkinter, this module offers a class called "AskForPassword" that
opens a window for the user to put its credentials.

.. code:: python
    from ask_for_color import AskForPassword
    ask = AskForPassword()
    user,password = ask.get()

My repository is in
.. _GitHub: https://github.com/jeykun/AskForPassword.git


THIS IS THE DOCUMENTATION OF THE CLASS
======================================
This class AskForPassword allows the user put its credentials.
    1) inputs as a dictionary (optional):
        -   user = "User_label"             # default is "User:"
        -   passw = "Pass_label"            # default is "Password:"
        -   asterisk = "\u263a"             # default is "*"
        -   ok = "OK_button"                # default is "OK"
        -   cancel = "Cancel_button"        # default is "Cancel"
        -   wtitle = "Window_title"         # default is "Type your password"
        -   caps_on = "Caps_Locked_label"   # default is "CAPS LOCKED"
        -   caps_off = "Caps_Unlocked_label"# default is "caps unlocked"
        



METHOD get()
------------
This method returns a list [user,password] or ['',''] if canceled.
See the next example:

.. code:: python
    from ask_for_password import AskForPassword
    ask = AskForPassword()
    user,pword = ask.get()  # it returns a string list like ['user','password']
    print(user,pword)

    

METHOD has_user_pass(user_pass_list)
------------------------------------
The method "has_user_pass(user_pass_list)" asserts whether 'user_pass_list' has a pair (user,password) correct.
The argument "user_pass_list" may be a list/tuple of pairs like [[user1,pass1],(user2,pass2)], etc.
It returns True whether user_pass_list has the 'user' and 'password' given by the user.
See the next example:

.. code:: python
    from ask_for_password import AskForPassword
    list_users = (['Alex','myPass'],['Joe','JoesPass'])
    ask = AskForPassword()
    user_allowed = has_user_pass(list_users)
    print(user_allowed)


    

METHOD crypto(password)
-----------------------
The method "crypto()" needs to be implemented to do encryption. Here goes the documentation:
This method needs to be implemented to do encryption. It receives a string.
You can implement, for example, by doing:

.. code:: python
    def new_crypto(string):
        ans = ''
        for letter in string:
            ans += str(ord(letter)-103)
        return ans
           
    AskForPassword.crypto = new_crypto

Now, you can use the method 'get()' and it returns [user,crypto_pass].
        




"""
from ask_for_password import AskForPassword
