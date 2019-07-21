from cnvrg.modules.errors import CnvrgError

def args_to_string(args):
    if args == None: return ''
    if isinstance(args, list): args = {k["key"]: k["value"] for k in args}
    ### expect dict of key=value
    return " ".join(map(lambda x: "--{key}='{value}'".format(key=x[0], value=x[1]), args.items()))


def validate_args(args):
    for key,value in args.items():
        if isinstance(value, list):
            raise CnvrgError("Library local run with many arguments are not supported yet.")