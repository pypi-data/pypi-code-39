from setuptools import setup

setup(
     author='Qwakka',
     name='qwackchat',    # This is the name of your PyPI-package.
     version='1.0.0.0',                          # Update the version number for new releases
     scripts=['qwackchat','sqwackchat','gui.py'],                  # The name of your scipt, and also the command you'll be using for calling it
     description='a basic multi_client chatbot that works over tcp sockets the github repository can be found at: https://github.com/kwajo/CA_Assignments/tree/master/one'
)
