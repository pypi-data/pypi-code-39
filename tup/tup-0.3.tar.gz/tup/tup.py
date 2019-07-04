#!/usr/bin/env python

# Imports
from os import path
import sys
import logging
import argparse

# Arguments
parser = argparse.ArgumentParser(usage="tup [options] file",
                    description="Send files on Telegram from the command line.")

parser.add_argument("file_name", type=str, metavar="file")

parser.add_argument("-d", "--document", dest="doc",
                    help="send as a document", action="store_true")

parser.add_argument("-r", "--recipient", dest="recipient",
                    default="me", type=str,
                    help="which chat to send the file to (default: self)")

parser.add_argument("-c", "--caption", dest="caption",
                    type=str, help="file caption")

parser.add_argument("-s", "--session", dest="session",
                    default="default_user", type=str,
                    help="specify a session file to use")

args = parser.parse_args()


# Config
api_id = 25628
api_hash = "1fe17cda7d355166cdaa71f04122873c"
sys.dont_write_bytecode = True
logging.basicConfig(level=logging.WARNING)

script_dir = path.dirname(path.realpath(__file__))  # Set the location of the script
session_file = path.join(script_dir, args.session)


# Telethon
from telethon import TelegramClient, sync
client = TelegramClient(session_file, api_id, api_hash)

def main():
    with client:
        me = client.get_me()
        print(f"Logged in as {me.first_name}")
        print(f"Sending {path.basename(args.file_name)} to {args.recipient}")
        client.send_file(entity=args.recipient, file=args.file_name,
                        caption=args.caption, force_document=args.doc)
        print("Done!")

if __name__ == "__main__":
    main()
