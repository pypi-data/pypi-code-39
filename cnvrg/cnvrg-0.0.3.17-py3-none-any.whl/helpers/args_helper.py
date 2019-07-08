

def args_to_string(args):
    ### expect dict of key=value
    return " ".join(map(lambda x: "--{key}={value}".format(key=x[0], value=x[1]), args.items()))
