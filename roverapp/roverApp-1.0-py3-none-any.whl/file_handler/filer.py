import os

#home = os.environ("HOME")
#os.chdir(home)


def make_file(data):
    """ """
    with open("COMMANDS_FILE", mode="w") as file:
        file.write("=======list of commands========\n")
        file.write(data)
        file.write("\n============================\n")


def read_file():
    """ """
    with open("COMMANDS_FILE") as file:
        temp_list = []
        for line in file:
            temp_list.append(line.strip())
        return temp_list
