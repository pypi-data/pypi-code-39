

def args_to_string(args):
    if args == None: return ''
    if isinstance(args, list): args = {k["key"]: k["value"] for k in args}
    ### expect dict of key=value
    return " ".join(map(lambda x: "--{key}='{value}'".format(key=x[0], value=x[1]), args.items()))
