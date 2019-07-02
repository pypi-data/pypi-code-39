# -*-coding:utf-8-*-

from pathlib import Path
import argparse
from sys import exit


def touch_not_exists_and_print(path):
    if path.exists():
        print("file %s already exists." % path.resolve())
        exit()
    path.touch()
    print("touch file %s" % path.resolve())


def main():
    parser = argparse.ArgumentParser(description="Local Judge Creator")
    parser.add_argument("src", help="source file")

    args = parser.parse_args()

    src_path = Path(args.src)
    stem = str(src_path.stem)
    suffix = str(src_path.suffix)
    if suffix not in [".c", ".cxx", ".cc", ".cpp"]:
        print("invalid suffix %s" % suffix)
        exit()

    touch_not_exists_and_print(src_path)

    data_dir = src_path.parent / stem
    data_dir.mkdir(parents=True)

    creation_list = ["1.in", "2.in", "1.out", "2.out", "README.md"]
    for file in creation_list:
        touch_not_exists_and_print(data_dir / file)


if __name__ == "__main__":
    main()
