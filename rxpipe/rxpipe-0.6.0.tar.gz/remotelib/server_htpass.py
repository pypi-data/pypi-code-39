from .remote_exec import REX
import os
import getpass



class Finder:

    def __init__(self, starting_dir="/home/{}".format(getpass.getuser()), *needs, frame="ca-provision"):
        self.starting_dir = starting_dir if not None else "ca-provisiontest".format(getpass.getuser())
        self.frame = frame
        self.needs = needs
        self.nkeys = [need.split(".")[len(needs)-1] for need in self.needs if "." in need]
        self.haves = dict(zip(self.nkeys, [list()*len(self.needs)]))

    def hunt(self, filter_test=False):
        for root, _d, files in os.walk(self.starting_dir):
            # root -> the abs path of cwd, files = list of files in the dir!
            for file in files:
                for x, need in enumerate(self.needs):
                    if (self.frame + "/" + file) in (root+"/"+file):
                        print("*** -> {}/{}".format(root, file))
                        self.haves[self.nkeys[x]].append(root + "/" + file)
        return self.haves


class DeployServerHTPasswd:
    ## for info about REX see remote_exec.py

    def __init__(self, connection_target):
        self.conn = REX(connection_target)
        ## assume we got the good files from above
        self.conn.rex_push("server.htpasswd", "/usr/local/eptt/download/etc/sdk.htpasswd")
        self.conn.rex_push("sdk.htpassed", "/usr/local/eptt/etc/sdk.htpasswd")
        self.conn.close()
