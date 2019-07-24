import os.path


def read_key_file(host, keyfile='.panconfkeystore', splitchar=":", searchpos=0, retpos=1, includehomedir=True):
    if includehomedir == True:
        pathstring = os.path.expanduser('~') + "/" + str(keyfile)
    else:
        pathstring = keyfile
    with open(pathstring) as f:
        for line in f.readlines():
            if line.split(splitchar)[searchpos] == host:
                return line.split(":")[retpos].strip()
    raise Exception("Unable to find firewall in file, exiting now.")
