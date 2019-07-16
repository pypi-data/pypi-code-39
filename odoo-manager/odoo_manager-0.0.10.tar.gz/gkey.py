#!/bin/python3
import os
import sys

env = sys.argv[1]
value = os.getenv(env)

if not value:
    raise Exception("There was a problem accessing the environment variable {}".format(env))

with open("key.json", "w+") as keyfile:
    keyfile.write(value)
