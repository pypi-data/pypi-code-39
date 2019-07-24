
"""
Based on Tkinter, this module offers a class called "AskForPassword" that
opens a window for the user to put its credentials.
>> get()
    To get the values, just use the "get( )" method. It returns the list ['user','password'].
    See the next example:
        from ask_for_password import AskForPassword
        ask = AskForPassword()
        user,pword = ask.get()  # it returns a string list like ['user','password']

>> has_user_pass(user_pass_list)
    The method "has_user_pass(user_pass_list)" asserts whether 'user_pass_list' has a pair (user,password) correct.
    The argument "user_pass_list" may be a list/tuple of pairs like [[user1,pass1],(user2,pass2)], etc.
    It returns True whether user_pass_list has the 'user' and 'password' given by the user.


>> crypto(password)
    The method "crypto()" needs to be implemented to do encryption. Here goes the documentation:
    This method needs to be implemented to do encryption. It receives a string.
    You can implement, for example, by doing:
       def new_crypto(string):
           ans = ''
           for letter in string:
               ans += str(ord(letter)-103)
           return ans
           
       AskForPassword.crypto = new_crypto

    Now, you can use the method 'get()' and it returns [user,crypto_pass].
        


run the command or follow the url
git clone https://github.com/jeykun/AskForPassword.git
"""
from setuptools import setup,find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
try:
    with open(path.join(here,'DESCRIPTION.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


#ajuda em https://www.youtube.com/watch?v=Lb0b4ro0ze4&list=PLV7VqBqvsd_0u42lQtg4FU-rWeOSsbzOT&index=5
setup(
    # Ver PEP 426 (name)
    # Iniciar ou terminar com letra ou numero
    name='ask_for_password',
    # Ver PEP 440
    # O formato pode ser assim:
    # 1.2.0.dev1    Development release
    # 1.2.0a1       Alpha Release
    # 1.2.0b1       Beta Release
    # 1.2.0rc1      Release Candidate
    # 1.2.0         Final Release
    # 1.2.0.post1   Post Release
    # 15.10         Date based release
    # 23            Serial release
    version = '0.0.2',
    description = 'A GUI interface to get an user and a password list as [user,pass].',
    #long_description = 'Using Tkinter module, it allows the user to set any color in RGB system like "#rrggbb".',
    url = 'https://github.com/jeykun/AskForPassword.git',
    author = 'Junior R. Ribeiro',
    author_email = 'juniorribeiro2013@gmail.com',
    license = 'Free for non-commercial use',
    classifiers = [
        # How mature is this project? Common values are
        #   2   Alpha
        #   4   Beta
        #   5   Production/Stable
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        # Pick your license as you wish (should match "license" above)
        'License :: Free for non-commercial use',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    keywords = ['GUI','Tkinter','Password','Interface'],
    packages = find_packages(),
    install_requires = ['sh>=1.11'],
    data_files = []    
    )
