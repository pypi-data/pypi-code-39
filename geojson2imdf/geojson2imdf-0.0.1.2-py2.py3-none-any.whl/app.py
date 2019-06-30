import os


def run():
    print(f"running in {os.getcwd()}")
    # TODO: discover a folder named venue
    p = os.path.join(os.getcwd(), "venue")
    if(os.path.exists(p)):
        print("found venue folder")
    else:
        print("NO VENUE FOLDER")


def version():
    print("version")


if __name__ == '__main__':
    run()
