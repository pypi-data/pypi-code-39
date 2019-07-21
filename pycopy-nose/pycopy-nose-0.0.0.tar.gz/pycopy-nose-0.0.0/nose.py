import sys
import os


def main():
    for path, dirs, files in os.walk("."):

        # Skip dirs with leading dot, like ".venv", etc.
        dirs_new = []
        for d in dirs:
            if d[0] == ".":
                continue
            if d in ("uasyncio",):
                continue
            dirs_new.append(d)
        dirs[:] = dirs_new

        for f in files:
            if not f.startswith("test_") or not f.endswith(".py"):
                continue
            fullname = path + "/" + f
            print(fullname)
            res = os.system("micropython " + fullname)
            if res:
                sys.exit(res >> 8)


if __name__ == "__main__":
    main()
