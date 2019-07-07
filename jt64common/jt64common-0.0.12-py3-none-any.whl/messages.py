import os
import sys
import glob

from colorconsole import terminal
from . utils import clear


def main_header_message():
    """JTSDK64 Main Menu Headder Message"""
    screen = terminal.get_terminal(conEmu=False)
    clear()
    print("--------------------------------------------------")
    screen.set_color(3, 0)
    print(f"JTSDK64 Tools {os.environ['VERSION']}")
    screen.reset_colors()
    print("--------------------------------------------------")
    print('{0:18}  {1}'.format("\nQT Version", os.environ["QTV"]))
    print('{0:17}  {1}'.format("Core Tools", os.environ["CORETOOLS"]))
    print('{0:17}  {1}'.format("Python", os.environ["PYTOOLS"]))
    print('{0:17}  {1}'.format("Postgres", os.environ["POSTGRES"]))
    print('{0:17}  {1}'.format("Unix Tools", os.environ["UNIXTOOLS"]))
    screen.cprint(14, 0, "\nFor Command List, Type: jt64help\n")
    screen.reset_colors()

