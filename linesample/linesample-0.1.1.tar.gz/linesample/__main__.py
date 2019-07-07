import argparse
import linesample


def parse():
    """
    Parse arguments to the main function.

    Args:
        None.

    Returns:
        An `argparse.Namespace` instance containing the attributes resulting
        from the parsed arguments. If neither a fraction of lines or a
        number of lines is specified, the program will print an error and
        usage message and exit with status code 2.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', default='-', help='input file')
    parser.add_argument('-s', '--seed', default=None, type=int,
                        help='seed for random number generator')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--fraction', type=float,
                       help='fraction of lines to select')
    group.add_argument('-n', '--number', type=int,
                       help='number of lines to select')

    args = parser.parse_args()

    # Check if neither fraction nor number has been set after parsing.
    # Checking whether both were set is not necessary because we defined a
    # mutually exclusive group above.
    if args.fraction is None and args.number is None:
        parser.error('A value for exactly one of -f/--fraction or '
                     '-n/--number is required.')

    return args


def main():
    args = parse()
    linesample.sample_lines(args.infile, args.seed, args.fraction, args.number)


if __name__ == '__main__':
    main()
