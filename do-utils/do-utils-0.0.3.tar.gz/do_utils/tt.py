from do_utils import do_time

@do_time(func=True)
def main():
    return len([x for x in range(100000)])


if __name__ == '__main__':
    main()
