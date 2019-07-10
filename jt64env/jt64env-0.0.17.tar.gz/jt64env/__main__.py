import os
import sys
import argparse

from colorconsole import terminal
from jt64env import __version__
from jt64env import __summary__


def clear():
    """Clear Screen Function"""
    os.system('cls' if os.name == 'nt' else 'clear')


def env_item(value):
    """Return status of environment variable"""
    status = os.getenv(value)
    return status


def main():
    """Prints JTSDK64 Tools Environment Variables """
    clear()

    # setup the parser
    parser = argparse.ArgumentParser(add_help=True, description=__summary__)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + __version__,
                        help='display module version')

    # process the arguments
    args = parser.parse_args()

    screen = terminal.get_terminal(conEmu=False)
    print("------------------------------------------------------------")
    screen.set_color(3, 0)
    print(f"JTSDK64 Tools {os.environ['VERSION']} Environment Variables")
    screen.reset_colors()
    print("------------------------------------------------------------")
    print("\nJTSDK Variables\n")
    print(f"  JTSDK Version ....: {env_item('JTSDK_VERSION')}")
    print(f"  JTSDK Home .......: {env_item('JTSDK_HOME')}")
    print(f"  JTSDK Config .....: {env_item('JTSDK_CONFIG')}")
    print(f"  JTSDK Data .......: {env_item('JTSDK_DATA')}")
    print(f"  JTSDK Tmp ........: {env_item('JTSDK_TMP')}")
    print(f"  JTSDK Scripts ....: {env_item('JTSDK_SCRIPTS')}")
    print("\nQT Variables\n")
    print(f"  QT Version  ......: {env_item('QTV')}")
    print(f"  QT Directory .....: {env_item('QTD')}")
    print(f"  QT Plugins .......: {env_item('QTP')}")
    print(f"  GCC Directory ....: {env_item('GCCD')}")
    print("\nConfiguration Options\n")
    print(f"  Python Tools .....: {env_item('PYTOOLS')}")
    print(f"  PostgreSQL .......: {env_item('POSTGRES')}")
    print(f"  Unix Tools .......: {env_item('UNIXTOOLS')}")


if __name__ == '__main__':
    main()
    sys.exit(0)
