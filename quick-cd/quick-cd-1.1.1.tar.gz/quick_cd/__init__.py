import appdirs
import argparse
import json
import sys
import os
import fcntl
import termios


app_name = 'quick-cd'
bookmarks_file_name = 'bookmarks.dat'
actionTag = 'action'
cdTag = 'cd'
createTag = 'create'
deleteTag = 'delete'
listTag = 'list'
actions = ['create', 'delete', 'list']


def set_action(args):
    for action in actions:
        if getattr(args, action, None):
            setattr(args, actionTag, action)
            return
    setattr(args, actionTag, cdTag)


def parse_arguments():
    parser = argparse.ArgumentParser()
    options = parser.add_mutually_exclusive_group()
    options.add_argument('-c', '--create', action='store_true')
    options.add_argument('-d', '--delete', action='store_true')
    options.add_argument('-l', '--list', action='store_true')
    parser.add_argument('label', nargs='?')
    parser.add_argument('path', nargs='?')
    args = parser.parse_args()
    set_action(args)
    if args.path is not None and args.action != createTag:
        raise Exception('[path] argument can only be used with --create')
    return args


def main():
    args = parse_arguments()
    data_dir = appdirs.user_data_dir(app_name)
    data_path = os.path.join(data_dir, bookmarks_file_name)
    bookmarks = None

    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    try:
        with open(data_path) as bookmarks_file:
            bookmarks = json.load(bookmarks_file)
    except FileNotFoundError:
        bookmarks = {}

    if args.action == cdTag:
        if not args.label in bookmarks:
            print(f'No bookmark labeled "{args.label}"', file=sys.stderr)
            exit(1)
        for char in f'cd "{bookmarks[args.label]}"\n':
            fcntl.ioctl(0, termios.TIOCSTI, char)
    elif args.action == createTag:
        path = args.path
        if not path:
            path = os.getcwd()
        path = os.path.abspath(path)
        bookmarks[args.label] = path
        with open(data_path, 'w') as bookmark_file:
            json.dump(bookmarks, bookmark_file)
    elif args.action == listTag:
        for bookmark, path in bookmarks.items():
            print(bookmark, path)
    else:
        del bookmarks[args.label]
        with open(data_path, 'w') as bookmark_file:
            json.dump(bookmarks, bookmark_file)