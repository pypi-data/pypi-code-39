import os
import sys

from colorconsole import terminal
from . utils import clear


def jt64_main_help():
    """Prints Main Help Message"""
    clear()
    screen = terminal.get_terminal(conEmu=False)
    print("------------------------------------------------------------")
    screen.set_color(3, 0)
    print(f"JTSDK64 Tools {os.environ['VERSION']} Help Menu")
    screen.reset_colors()
    print("------------------------------------------------------------")
    print("")
    print("The following commands are available throughout the JTSDK64")
    print("Tools Environment.")
    print("\nScripts Commands\n")
    print('{0:15}  {1}'.format("  jthelp", "Print This Help Menu"))
    print('{0:15}  {1}'.format("  jtenv", "Lists All Environment Variables"))
    print('{0:15}  {1}'.format("  jtgentc", "Generate Tool Chain Files"))
    print('{0:15}  {1}'.format("  jtversion", "Checks Tool-Chain Versions"))
    print('{0:15}  {1}'.format("  jtsetqt", "Set Qt Version"))
    print("\nShortcut Commands\n")
    print('{0:15}  {1}'.format("  home", "Return back to home directory"))
    print('{0:15}  {1}'.format("  msys2", "Launch the MSYS2 Console"))
