import sys
from .waimoku import Waimoku


def main():
    argv = sys.argv
    waimoku = Waimoku()
    waimoku.save_to_file_from_csv_file(file_path=argv[1], save_filename=argv[2])
