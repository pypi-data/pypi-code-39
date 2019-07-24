from cliutil.Questions import yesnoquestion


def listselection(list, prompt="Please select an item from the list", startatone=False, verify=False):
    """
    Allow a user to select an item from a list
    :param list: List; list of items for a user to select one from
    :param prompt: String; Prompt to ask the user
    :param startatone: Boolean; Does the list start at one?
    :param verify; Should the user be given a chance to correct any mistakes?
    :return: Int; index of user selection
    """
    if startatone:
        list.insert(0, "")
    for index in range(len(list)):
        if startatone and index == 0:
            continue
        print(f"({index}) - {list[index]}")
    while True:
        test = input(prompt + ": ")
        try:
            test = int(test)
        except ValueError:
            print("Input must be a number")
        if verify:
            if not yesnoquestion("Is this answer correct", verify=False):
                continue
        return test
