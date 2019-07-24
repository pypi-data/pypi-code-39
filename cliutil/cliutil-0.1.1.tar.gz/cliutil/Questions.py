def yesnoquestion(text, verify=False):
    """
    Ask a yes or no question
    :param text: String; The text of the question asked
    :param verify: Boolean; Should the user be given a chance to correct any mistakes?
    :return: Boolean; True or False depending on the y/N input of the user
    """
    answer = None

    # Strip a trailing question mark if present
    text = text.rstrip('?')

    # Append the options to the question
    text += "? y/N "

    # Loop forever until a good answer is given
    while True:
        test = input(text).lower()
        if test == "y":
            answer = True
        elif test == "n":
            answer = False
        else:
            print("Please enter y/N")
        if verify:
            if not yesnoquestion("Is this answer correct"):
                continue
        return answer


def stringquestion(text, verify=False):
    """
    Ask for a string from the user
    :param text: String; The text of the question asked
    :param verify: Boolean; Should the user be given a chance to correct any mistakes?
    :return: String; The user input
    """

    # Append the whitespacae to the question
    text += " "

    while True:
        test = input(text)
        if verify:
            if not yesnoquestion("Is this answer correct", False):
                continue
        return test


def numberquestion(text, verify=False):
    """
    Ask for a numerical input from the user
    :param text: tring; The text of the question asked
    :param verify:Boolean; Should the user be given a chance to correct any mistakes?
    :return: Float; The user input cast as a float
    """

    # Append the whitespace to the question
    text += " "

    while True:
        test = input(text)
        # Test if the input can be cast as a float
        try:
            test = float(test)
        except ValueError:  # Cannot cast as float
            print("Please enter a number as an answer")
            continue
        except OverflowError:
            print("Number too large")
            continue
        if verify:
            if not yesnoquestion("Is this answer correct", False):
                continue
        return test
