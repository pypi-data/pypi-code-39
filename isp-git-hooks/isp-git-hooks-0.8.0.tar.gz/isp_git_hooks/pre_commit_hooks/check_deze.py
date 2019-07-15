import argparse
from typing import Optional, Sequence

TEST_STATEMENTS = [
    b'"deze"'
]
WARNING_MSG = 'Test tag "{0}" found in {1}:{2}'


def main(argv=None):  # type: (Optional[Sequence[str]]) -> int
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retcode = 0
    for filename in args.filenames:
        with open(filename, 'rb') as inputfile:
            for i, line in enumerate(inputfile):
                for pattern in TEST_STATEMENTS:
                    if pattern in line:
                        print(WARNING_MSG.format(
                            pattern.decode(), filename, i + 1,
                        ))
                        retcode = 1

    return retcode


if __name__ == '__main__':
    exit(main())
