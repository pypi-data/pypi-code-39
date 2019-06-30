import os


def run():
    print(f"running in {os.getcwd()}")
    # TODO: discover a folder named venue
    p = os.path.join(os.getcwd(), "venue")
    if(os.path.exists(p)):
        print("found venue folder")
        v = os.path.join(p, "venue.geojson")
        if(os.path.exists(v)):
            print(f"found venue.geojson in {p}")
        else:
            print(f"no venue.geojson found in {p}")

        subfolders = [f.path for f in os.scandir(p) if f.is_dir()]
        for folder in subfolders:
            print(f"found folder {folder} in {p}")

    else:
        print("NO VENUE FOLDER")


def version():
    print("version")


if __name__ == '__main__':
    run()
