import os
import sys
import argparse

from colorconsole import terminal

from jt64config import __version__ as __version__
from jt64config import __summary__ as __summary__

# process variables
config_dir = os.environ['JTSDK_CONFIG']
option_dict = {
    'autorun': 'Run WSJT-X after successful build',
    'clean': 'Clean build for WSJT-X',
    'hlclean': 'Clean build for Hamlib',
    'reconfigure': 'Reconfigure build tree',
    'separate': 'Separate builds by Qt version',
    'quiet': 'Suppress screen messages',
    'unix': 'Use Unix style tools'
}


def clear():
    """Clear Screen Function"""
    os.system('cls' if os.name == 'nt' else 'clear')


# TODO: move this function to jt64common
def header(text, value):
    """Print header with text and underline value"""
    screen = terminal.get_terminal(conEmu=False)
    print("-" * value)
    screen.set_color(3, 0)
    print(f"{text}")
    screen.reset_colors()
    print("-" * value)


def version():
    print(f"\n{__summary__} Version {__version__}")
    print('''Copyright (C) 2013-2019, GPLv3, Greg Beam, KI7MT
This is free software; There is NO warranty; not even
for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
''')


def option_action(option, action):
    """Enable or Disable a single option"""

    config_option = str(option)
    config_action = str(action)
    filename = os.path.join(config_dir, config_option)

    if action == 'enable':
        print(f" * enabling {option}")
        with open(filename, 'w') as f:
            f.close

    if action == 'disable':
        print(f" * disabling {option}")
        if os.path.exists(filename):
            os.remove(filename)


def default_options(action):
    """Enable or Disable All Available options"""
    for k in option_dict:
        file = os.path.join(config_dir, k)
        if action == 'enable':
            with open(file, 'w') as f:
                f.close
        else:
            if os.isfile(file):
                os.remove(file)


# TODO: create a function in jt64common: header(text,length)
def iterate_options():
    """Iterate and print supported Options"""
    for k in option_dict:
        print(f"   {k}")


def iterate_description():
    """Iterate and print options and descriptions"""
    for k, v in option_dict.items():
        print(f"   {k:<14}{v:<3}")


def iterate_env_variables():
    """Iterate env variable status"""
    for k in option_dict:
        print(f"   JTSDK_{k.upper():<12} = True or False")


# TODO: create a function in jt64common: header(text,length)
def iterate_status():
    """Print long description of options"""
    for k in option_dict:
        if os.path.isfile(os.path.join(config_dir, k)):
            value = "enabled"
        else:
            value = "disabled"
        print(f"  {k:<14} {value:<3}")


def main():
    """Prints JTSDK64 Tool Option Configuration"""
    # Check for the existence of JTSDK_CONFIG variable first
    if 'JTSDK_CONFIG' in os.environ:
        pass
    else:
        clear()
        print("\nUnable to find environment variable JTSDK_CONFIG.")
        print("Ensure you are running from JTSDK64 Tools before")
        print("setting environment options\n")
        sys.exit(0)

    # argument options, these are all simple boolean values
    parser = argparse.ArgumentParser(description=__summary__, prefix_chars='-+')
    parser.add_argument('+a', action="store_true", default=False, dest="autorun_t", help='enable autorun')
    parser.add_argument('-a', action="store_true", default=False, dest="autorun_f", help='disable autorun')

    parser.add_argument('+c', action="store_true", default=False, dest="clean_t", help='enable clean')
    parser.add_argument('-c', action="store_true", default=False, dest="clean_f", help='disable clean')

    parser.add_argument('+hc', action="store_true", default=False, dest="hlclean_t", help='enable hamlib clean')
    parser.add_argument('-hc', action="store_true", default=False, dest="hlclean_f", help='disable hamlib clean')

    parser.add_argument('+q', action="store_true", default=False, dest="quiet_t", help='enable quiet mode')
    parser.add_argument('-q', action="store_true", default=False, dest="quiet_f", help='disable quiet mode')

    parser.add_argument('+r', action="store_true", default=False, dest="reconfigure_t", help='enable reconfigure')
    parser.add_argument('-r', action="store_true", default=False, dest="reconfigure_f", help='disable reconfigure')

    parser.add_argument('+s', action="store_true", default=False, dest="separate_t", help='enable separate')
    parser.add_argument('-s', action="store_true", default=False, dest="separate_f", help='disable separate')

    parser.add_argument('+u', action="store_true", default=False, dest="unix_t", help='enable unix tools')
    parser.add_argument('-u', action="store_true", default=False, dest="unix_f", help='disable unix tools')

    # Default list options, enables or disables the full list
    parser.add_argument('+D', action="store_true", default=False, dest="default_t", help='enable default item set')
    parser.add_argument('-D', action="store_true", default=False, dest="default_f", help='disable default item set')

    # list / display options
    parser.add_argument('-l', '--list', action='store_true', dest='list_t', help='list supported options')
    parser.add_argument('-od', '--description', action='store_true', dest='description_t', help='print long descriptions')
    parser.add_argument('-status', '--status', action='store_true', dest='status_t', help='display option status')
    parser.add_argument('-v', '--version', action='store_true', dest='version_t', help='display application version')

    # process the arguments
    args = parser.parse_args()

    # -v option: display version information
    if args.version_t:
        clear()
        version()
        sys.exit(0)

    # -l option: list all available options
    if args.list_t:
        clear()
        header("Supported Options", 25)
        iterate_options()
        sys.exit(0)

    # -od option: display option descriptions and associated env variables
    if args.description_t:
        clear()
        header("Option Description and Environment Variables", 50)
        print("\n Description:")
        iterate_description()
        print("\n Environment Variables:")
        iterate_env_variables()
        sys.exit(0)

    # --status option: print the status of each options in options dictionary
    if args.status_t:
        clear()
        header("Current Configuration Status", 45)
        print("")
        iterate_status()
        sys.exit(0)

    # +D Enable Default options
    # TODO: default methods -D/+D should be combined
    if args.default_t:
        clear()
        header("Processing Default Options Enable", 35)
        for k in option_dict:
            option_action(k, 'enable')

        print("\nStatus After Change")
        iterate_status()
        sys.exit(0)

    #  -D Disable Default Options
    if args.default_f:
        clear()
        header("Processing Default Options Disable", 35)
        for k in option_dict:
            option_action(k, 'disable')

        print("\nStatus After Change")
        iterate_status()
        sys.exit(0)

    # process individual options
    clear()
    header("Individual Options", 35)

    # Autorun Options
    if args.autorun_t is True:
        option_action('autorun', 'enable')

    if args.autorun_f is True:
        option_action('autorun', 'disable')

    # Clean Options
    if args.clean_t is True:
        option_action('clean', 'enable')

    if args.clean_f is True:
        option_action('clean', 'disable')

    # Hamlib CLean
    if args.hlclean_t is True:
        option_action('hlclean', 'enable')

    if args.hlclean_f is True:
        option_action('hlclean', 'disable')

    # Quiet Options
    if args.quiet_t is True:
        option_action('quiet', 'enable')

    if args.quiet_f is True:
        option_action('quiet', 'disable')

    # Reconfigure
    if args.reconfigure_t is True:
        option_action('reconfigure', 'enable')

    if args.reconfigure_f is True:
        option_action('reconfigure', 'disable')

    # Separate
    if args.separate_t is True:
        option_action('separate', 'enable')

    if args.separate_f is True:
        option_action('separate', 'disable')

    # Unix
    if args.unix_t is True:
        option_action('unix', 'enable')

    if args.unix_f is True:
        option_action('unix', 'disable')

    # Now iterate current status
    print("\nStatus:")
    iterate_status()

if __name__ == '__main__':
    main()
    sys.exit(0)
