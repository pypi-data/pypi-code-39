"""
TODO:
    Error handling
"""
import argparse
import json
import sys
import subprocess

from .lib import get_vulnerabilities, process


def create_parser():
    parser = argparse.ArgumentParser(prog='npm-audit-checkmk',
                                     description='Creates checkmk local check file for npm audit output.'
                                     'warning levels need to be lower or equal than critical levels.'
                                     'checkmk uses > for level comparisons.')
    parser.add_argument('-f', '--file',
                        default=sys.stdin,
                        type=argparse.FileType('r'),
                        help='Input file name. Optional. Otherwise read from stdin (-).')
    parser.add_argument('-o', '--output',
                        default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='Output file name. Optional. Otherwise write to stdout'
                        )
    parser.add_argument('-s', '--service-name',
                        default='npm_audit',
                        help='The service name to be used inside the file (default: "npm_audit".',
                        )
    parser.add_argument('-d', '--directory',
                        help='The directory to run `npm audit` in, if given. Only in Python >= 3.5.',
                        )

    parser.add_argument('-iw', '--info-warning',
                        default=None,
                        type=int,
                        help='The warning level for info vulnerabilities (default: None)')
    parser.add_argument('-ic', '--info-critical',
                        default=None,
                        type=int,
                        help='The critical level for info vulnerabilities (default: None)')
    parser.add_argument('-lw', '--low-warning',
                        default=20,
                        type=int,
                        help='The warning level for low vulnerabilities (default: 20)')
    parser.add_argument('-lc', '--low-critical',
                        default=None,
                        type=int,
                        help='The critical level for low vulnerabilities (default: None)')
    parser.add_argument('-mw', '--moderate-warning',
                        default=10,
                        type=int,
                        help='The warning level for moderate vulnerabilities (default: 10)')
    parser.add_argument('-mc', '--moderate-critical',
                        default=20,
                        type=int,
                        help='The critical level for moderate vulnerabilities (default: 20)')
    parser.add_argument('-hw', '--high-warning',
                        default=1,
                        type=int,
                        help='The warning level for high vulnerabilities (default: 1)')
    parser.add_argument('-hc', '--high-critical',
                        default=3,
                        type=int,
                        help='The critical level for high vulnerabilities (default: 3)')
    parser.add_argument('-cw', '--critical-warning',
                        default=0,
                        type=int,
                        help='The warning level for critical vulnerabilities (default: 0)')
    parser.add_argument('-cc', '--critical-critical',
                        default=0,
                        type=int,
                        help='The critical level for critical vulnerabilities (default: 0)')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.directory:
            if sys.version_info < (3, 5):
                print('-d is only available for Python >= 3.5', file=sys.stderr)
                return 2
            proc = subprocess.run('npm audit --json'.split(' '),
                                  cwd=args.directory,
                                  stdout=subprocess.PIPE,
                                  )
            if proc.returncode > 1:
                raise subprocess.CalledProcessError('Return code was %d' % proc.returncode)
        data = json.loads(proc.stdout)
    except Exception as exc:
        print('Error executing `npm audit`: %s' % exc, file=sys.stderr)
        return 2
    try:
        data = json.loads(args.file.read())
    except Exception as exc:
        print('Error reading input (file): %s' % exc, file=sys.stderr)
        return 2

    evaluation = get_vulnerabilities(dict_data=data)
    result = process(evaluation, args)

    args.output.write(result)


if __name__ == '__main__':
    sys.exit(main())
