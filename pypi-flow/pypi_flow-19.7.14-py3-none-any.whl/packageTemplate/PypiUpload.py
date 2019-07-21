#UPDATE PACKAGE ON PYPI
from grtoolkit.PYPI import Upload2Pypi
Upload2Pypi()

#UPDATE LOCATE PACKAGE TO LATEST VER ON PYPI
from grtoolkit.Windows import cmd
install_package = 'pip install --upgrade $package-name$ --user'
cmd(install_package,
    install_package)