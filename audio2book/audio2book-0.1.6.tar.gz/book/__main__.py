from book import convert, cli, logging


def main():  # pragma: no mutate
    parse = cli.parser()  # pragma: no mutate
    args = parse.parse_args()  # pragma: no mutate
    logging.log.notice(f'Running the program with args: {args}.')  # pragma: no mutate
    print(convert.run(args.completed, args.overall, args.pages))  # pragma: no mutate


if __name__ == '__main__':  # pragma: no mutate
    main()  # pragma: no mutate
