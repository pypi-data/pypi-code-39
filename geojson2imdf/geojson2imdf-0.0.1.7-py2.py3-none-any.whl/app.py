import os
import venue.Venue


def run():
    print(f" geojson2imdf is running in {os.getcwd()}")
    p = os.path.join(os.getcwd(), "venue")
    if(os.path.exists(p)):
        print(f"👍 Found a folder named 'venue' in {p}")
        v = os.path.join(p, "venue.geojson")
        if(os.path.exists(v)):
            print(f"👍 Found 'venue.geojson' in {p}")
            v = Venue()

        else:
            print(f"😢 No 'venue.geojson' found in {p}")

        subfolders = [f.name for f in os.scandir(p) if f.is_dir()]
        for folder in subfolders:
            print(f"found a folder called {folder} in {p}")

    else:
        print(f"😢 No folder named 'venue' found in {p}")


def version():
    print("version")


if __name__ == '__main__':
    run()
