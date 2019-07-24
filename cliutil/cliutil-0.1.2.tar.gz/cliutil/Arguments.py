import sys


def clarguments():
    """
    Handle arguments passed to the script through the command line
    :return: dict; Contains the variables and all the values assigned to them. Flags will have a None type.
    """
    output = {"_args": None}
    arguments = sys.argv[1:]

    for arg in arguments:
        arg = str(arg)
        if arg[0] == "-":
            if arg[1] == "-":  # Double dashey bois
                output.update({arg[2:]: None})
                continue
            # Single dashey boi
            arg = [char for char in arg[1:]]
            for char in arg:
                output.update({char: None})
            continue
        # No dashey boi
        current_element = list(output.keys())[-1]
        if output[current_element] is None:
            output[current_element] = arg
        else:
            if output["_args"] is not None:
                args = output["_args"].split(',')
                args.append(arg)
                args = ','.join(args)
                output["_args"] = args
            else:
                output["_args"] = arg
    return output
