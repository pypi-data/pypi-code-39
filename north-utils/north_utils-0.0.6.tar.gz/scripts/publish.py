from os import path, chdir
from subprocess import call

# move to project root
chdir(path.join(path.dirname(path.realpath(__file__)), '..'))
# build
call('python setup.py sdist')
# deploy
call('python -m twine upload dist/*')