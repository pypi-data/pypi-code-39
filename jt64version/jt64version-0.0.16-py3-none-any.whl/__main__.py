import os
import sys

from jt64version import __version__
from colorconsole import terminal
from subprocess import PIPE
from subprocess import run


def clear():
    """Clear Screen Function"""
    os.system('cls' if os.name == 'nt' else 'clear')


def cmd(command):
    """Default Subprocess Command"""
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout


def get_asciidoctor_version():
    """Return Asciidoctor Version"""
    output = cmd("asciidoctor -V")
    ver = " ".join(output.split()[1:2])
    return ver.strip()


def get_cmake_version():
    """Return CMake Version"""
    output = cmd("cmake --version")
    ver = " ".join(output.split()[2:3])
    return ver.strip()


def get_bash_version():
    """Return Bash Version"""
    output = cmd("bash --version")
    ver = " ".join(output.split()[3:4])
    return ver.strip()


def get_fftw_version():
    """Return FFTW Version"""
    output = cmd("fftw-wisdom.exe --version")
    ver = " ".join(output.split()[5:6])
    ver = ver[:-1]
    return ver.strip()


def get_git_version():
    """Return Git Version"""
    output = cmd("git --version")
    ver = " ".join(output.split()[2:3])
    return ver.strip()


def get_libusb_version():
    """Get Libsub Version"""
    base_path = os.environ['JTSDK64_HOME']
    file_name = "libusb-1.0.def"
    file_path = os.path.join(base_path, "tools", "libusb", "1.0.22", file_name)

    with open(file_path) as f:
        first_line = f.readline()

    ver = str(first_line.split('"')[1])
    return ver.strip()


def get_nsis_version():
    """Return NSIS Version"""
    output = cmd("makensis /VERSION")
    return output.strip()[1:]


def get_pkgconfig_version():
    """Return PKG_Config Version"""
    output = cmd("pkg-config --version")
    return output.strip()


def get_psql_version():
    """Return PostgreSQL Version"""
    if os.environ['POSTGRES'] == "Not Installed":
        ver = "Not Installed"
    else:
        output = cmd("psql --version")
        ver = " ".join(output.split()[2:3])

    return ver.strip()


def get_sqlite_version():
    """Return SQLite Version"""
    output = cmd("sqlite3 --version")
    ver = " ".join(output.split()[0:1])
    return ver.strip()


def get_subversion_version():
    """Return Subversion Version"""
    output = cmd("svn --version")
    ver = " ".join(output.split()[2:3])
    return ver.strip()


def get_qmake_version():
    """Return Qmake Version"""
    output = cmd("qmake --version")
    ver = " ".join(output.split()[2:3])
    return ver.strip()


def get_gcc_version():
    """Return GCC Version"""
    output = cmd("gcc --version")
    ver = " ".join(output.split()[6:7])
    return ver.strip()


def list_tcfiles():
    file_path = os.path.join(os.environ["JTSDK64_HOME"], "tools", "tcfiles")
    files = os.listdir(file_path)
    return files


def get_mingw32_make_version():
    """Return Mingw32-Make Version"""
    output = cmd("mingw32-make --version")
    ver = " ".join(output.split()[2:3])
    return ver.strip()


def main():
    clear()
    """JTSDK Main Menu Headder Message"""
    list = ', '.join(list_tcfiles())
    qtver = os.environ["QTV"]
    clear()
    screen = terminal.get_terminal(conEmu=False)
    print("--------------------------------------------------")
    screen.set_color(3, 0)
    print(f"JTSDK64 Tools {os.environ['VERSION']} Version Check")
    screen.reset_colors()
    print("--------------------------------------------------\n")
    print(f" QT {os.environ['QTV']} Tool Chain\n")
    print(f"   JT64 Version  : {__version__}")
    print(f"   Qt Version    : {qtver}")
    print(f"   Qt Version    : {qtver}")
    print(f"   Qmake         : {get_qmake_version()}")
    print(f"   GCC           : {get_gcc_version()}")
    print(f"   Mingw32-Make  : {get_mingw32_make_version()}")
    print(f"   TC Files      : {list}")
    print("\n General Purpose Tools\n")
    print(f"   Cmake         : {get_cmake_version()}")
    print(f"   Asciidoctor   : {get_asciidoctor_version()}")
    print(f"   Bash          : {get_bash_version()}")
    print(f"   FFTW          : {get_fftw_version()}")
    print(f"   Git           : {get_git_version()}")
    print(f"   Libusb        : {get_libusb_version()}")
    print(f"   NSIS          : {get_nsis_version()}")
    print(f"   Pkg-Config    : {get_pkgconfig_version()}")
    print(f"   PostgreSQL    : {get_psql_version()}")
    print(f"   SQLite3       : {get_sqlite_version()}")
    print(f"   Subversion    : {get_subversion_version()}")
    print('''
 JTSDK64 Tools Version v3.1.0
 Copyright (C) 2013-2019, GPLv3, Greg Beam, KI7MT
 This is free software; There is NO warranty; not even
 for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    ''')


if __name__ == '__main__':
    main()
    sys.exit(0)
