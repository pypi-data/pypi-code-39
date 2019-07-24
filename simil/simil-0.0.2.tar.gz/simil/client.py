import os
import sys
from tempfile import gettempdir
from rpyc.utils.factory import unix_connect

from .server import server
from .version import version
from .cli_args import args


def main():
    if args.socket:
        path = args.socket
    else:
        path = os.path.join(gettempdir(), "sim-server-socket")


    if args.kill:
        check_no_args(args)
        kill_server(path)
        return

    if args.server:
        check_no_args(args)
        if os.fork() == 0:
            server(path, load=True)
        return

    [first, second] = file_args(args.file)

    if not args.strings:
        with open(first) as first_file:
            first = first_file.read()
        with open(second) as second_file:
            second = second_file.read()

    if os.path.exists(path):
        try:
            client(path, second, first)
        except ConnectionRefusedError:
            os.unlink(path)
        else:
            return

    if os.fork() == 0:
        server(path)
    else:
        client(path, first, second, wait=True)


def client(socket_path, first, second, *, wait=False):
    while True:
        try:
            conn = unix_connect(socket_path)
        except (ConnectionRefusedError, FileNotFoundError):
            if wait:
                continue
            raise
        else:
            break
    print(conn.root.similarity(version, first, second))


def file_args(files):
    num_args = len(files)
    if num_args != 2:
        print(
            f"You must provide exactly two arguments to compare. ({num_args} provided.)",
            file=sys.stderr,
        )
        sys.exit(1)
    [first, second] = files
    return [first, second]


def kill_server(socket_path):
    try:
        conn = unix_connect(socket_path)
    except (ConnectionRefusedError, FileNotFoundError):
        print("Could not connect to server", file=sys.stderr)
        sys.exit(1)

    try:
        conn.root.kill()
    except EOFError:
        # Expected, if we kill the server.
        pass

def check_no_args(args):
    if len(args.file) > 0:
        print(f"Unexpected arguments: {', '.join(args.file)}", file=sys.stderr)
        sys.exit(1)
