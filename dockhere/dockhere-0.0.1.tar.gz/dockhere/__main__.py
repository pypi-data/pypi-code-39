"""
Run a command in docker in the current folder using a bind mount
"""

import argparse
import os
import getpass
import shutil
import sys
import tempfile
import subprocess


parser = argparse.ArgumentParser(
    prog="dockhere",
    description="Run a docker container in the current directory almost as though it was just a shell"
)
parser.add_argument("--priv", default=False, action="store_true",
                    help="Run docker with --privileged")
parser.add_argument("--root", default=False, action="store_true",
                    help="Run as root inside the container")
parser.add_argument("IMAGE", default="busybox:latest",
                    help="Docker image to run (default busybox)", nargs="?")


args, extra = parser.parse_known_args()
uid = os.getuid()
gid = os.getgid()

if args.root:
    uid = 0
    gid = 0

envs = {
    "USER": os.getenv("USER", "user")
}


def start(image, folder, envs, priv):
    """
    Run a container as root and leave it in the background
    :param image:
    :param folder:
    :return:
    """
    cmdline = ["docker", "run", "-d", "--rm",
               "-u", str(uid),
               "-w", folder,
               "-v", "{}:{}".format(folder, folder)
               ]

    for env in envs:
        cmdline.extend(["-e", "{}={}".format(env, envs[env])])

    if priv:
        cmdline.append("--privileged")

    cmdline.extend(["-it", image])

    id = subprocess.check_output(cmdline).decode().strip()

    return id


def add_user(container, uid, gid, username):
    """
    Add a user to the container by editing it's etc passwd
    :param container:
    :param uid:
    :param username:
    :return:
    """
    temp = tempfile.mkdtemp()
    try:
        cmdline = ["docker", "cp", "{}:/etc/passwd".format(container), temp]
        subprocess.check_call(cmdline)
        with open(os.path.join(temp, "passwd"), "a") as tf:
            tf.write("{}:x:{}:{}:docker user:/tmp:/bin/sh\n".format(
                username, uid, gid
            ))
        cmdline = ["docker", "cp", os.path.join(temp, "passwd"), "{}:/etc/passwd".format(container)]
        subprocess.check_call(cmdline)
    finally:
        shutil.rmtree(temp)


def stop(container):
    """
    Kill a container
    :param container:
    :return:
    """
    cmdline = ["docker", "kill", container]
    subprocess.call(cmdline)


def execute(container, uid, workdir, priv, envs, commandline):
    """
    Execute a command with interactive tty
    :param container:
    :param uid:
    :param workdir:
    :param priv:
    :return:
    """
    if not commandline:
        commandline = ["/bin/sh"]

    cmdline = ["docker", "exec", "-u", str(uid), "-w", workdir]

    if priv:
        cmdline.append("--privileged")

    for env in envs:
        cmdline.extend(["-e", "{}={}".format(env, envs[env])])
    cmdline.append("-it")
    cmdline.append(container)
    cmdline.extend(commandline)

    rv = subprocess.call(cmdline)

    stop(container)

    return rv


id = start(args.IMAGE, os.getcwd(), envs, args.priv)

if not args.root:
    add_user(id, uid, gid, getpass.getuser())

sys.exit(execute(id, uid, os.getcwd(), args.priv, envs, extra))

