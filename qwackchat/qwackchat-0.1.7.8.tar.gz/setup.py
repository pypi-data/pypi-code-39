from setuptools import setup
 
setup(
     name='qwackchat',    # This is the name of your PyPI-package.
     version='0.1.7.8',                          # Update the version number for new releases
     scripts=['qwackchat','sqwackchat','gui.py'],                  # The name of your scipt, and also the command you'll be using for calling it
     description='A chatroom server and client written in python3. Comes with a gui.Only works on lan'
)
