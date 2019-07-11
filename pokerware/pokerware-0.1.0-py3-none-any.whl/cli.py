import argparse

from pokerware import generate

EXIT_FAILURE = 1

def main():
    parser = argparse.ArgumentParser(description='Generate Pokerware password')
    parser.add_argument('--formal', action='store_true', help="Lookup words in the 'formal' wordlist")
    parser.add_argument('--slang', action='store_true', help="Lookup words in the 'slang' wordlist")
    parser.add_argument('--custom', dest='custom_path', help="Lookup words in a custom wordlist")
    parser.add_argument('code', nargs='+',
                        help='A sequence of (Value, Suit, Value, Suit, Suit) entries')

    args = parser.parse_args()
    mode_sum = sum([args.formal, args.slang, args.custom_path is not None])
    if mode_sum > 1:
        print('Please only select one of --formal, --slang, or --custom not a combination of the three.')
        exit(EXIT_FAILURE)

    try:
        if args.formal or mode_sum == 0:
            words = generate.formal(args.code)
        elif args.slang:
            words = generate.slang(args.code)
        else:
            words = generate.custom(args.code, args.custom_path)
    except KeyError as e:
        print(e.args[0], 'is not a valid code')
        exit(EXIT_FAILURE)

    print(' '.join(words))

if __name__ == '__main__':
    main()
