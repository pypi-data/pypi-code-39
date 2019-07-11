"""
    Qt Version Selection

        Presents user with a list of available Qt versions based on valid
        installation paths. If the folder exists, its classed as installed.

        Sets, by way of creating a null holding file, the Qt version which is
        used by the main JTSDK64 Tools Environment script to set the global
        variable: os.environ['QTV']

        The qtlist [] is pulled in from jt64common __qt_version_list__
"""
import os
import sys
from colorconsole import terminal
from jt64common import __qt_version_list__ as qtlist

available = []
home = os.environ['JTSDK_HOME']
qthome = os.path.join(home, 'tools', 'Qt')
configd = os.path.join(home, 'config')
screen = terminal.get_terminal(conEmu=False)
current_version = os.environ['QTV']


def valid_versions():
    print("\nValid Qt Versions")
    for i in available:
        print(f"  {i}")


def update_version(user_entry):
    """Remove all previously set versions, then set the users selections."""
    # remove all old set files
    for i in qtlist:
        file_name = "qt" + i
        old_file = os.path.join(configd, file_name)
        if os.path.isfile(old_file):
            os.remove(old_file)

    # create the new set file
    file_name = "qt" + user_entry
    new_file = os.path.join(configd, file_name)

    #  this is the same as, in effect, using: touch <filename> in Linux
    with open(new_file, 'w') as f:
        f.close()

    change_message()


def change_message():
    """Print message alterting the user to a required restart"""
    print("\nImportant: Changing QT Versions requires restarting")
    print("the main JTSDK64 Tools Environment.\n")


def main():
    """
        Set Qt Version Function
            - Generates a list of installed components
            - Checks is said list is > 0
            - Prompts user for input for setting new version
            - Validates the user selection
            - If a new version is set, updates the version tag file
    """
    # print the header
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-" * 35)
    screen.set_color(3, 0)
    print("JTSDK64 Tools QT Version Selection")
    screen.reset_colors()
    print("-" * 35)

    # find installed verisons of Qt by checking fir directories
    if os.path.isdir(qthome):
        for i in qtlist:
            path = os.path.join(qthome, i)
            if os.path.isdir(path):
                available.append(str(i))
    else:
        print("Qt Does not appear to be installed yet.")
        sys.exit(0)

    # check if available list is > 0
    if len(available) > 0:
        valid_versions()
    else:
        print("\nSorry, there are no Qt component folders found :=(")
        print("Us the qtsetup or postinstall scripts to perform the")
        print("required installation.\n")
        sys.exit(0)

    # prompt user for put
    print("\nAt the prompt, type the version number\nyou wish to use.\n")

    # loop to type in the right selection
    while True:
        user_entry = input('Selection : ')
        if user_entry not in available:
            print(f"Qt ({user_entry}) is an invalid entry, please try again")
        else:
            isValid = True
            print(f"Setting Qt version to => {user_entry}")
            break

    if current_version == user_entry:
        print(f"\nYour selection ({user_entry}) is the same as the current version.")
        print(f"If you intended to set a difference version, re-run the script.\n")
    else:
        update_version(user_entry)


if __name__ == "__main__":
    main()
    sys.exit(0)
