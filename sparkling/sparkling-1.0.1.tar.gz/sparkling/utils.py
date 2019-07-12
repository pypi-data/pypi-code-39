import datetime as dt
import os


def get_flat_pair(detail):
    length = len(detail.split('/'))
    return f"{length}X1" if length != 1 else 'FSGL'

def get_filelist(file_dir, range_start, range_end):
    filelist = []
    start_time = dt.datetime.strptime(str(range_start), '%Y%m%d')
    end_time = dt.datetime.strptime(str(range_end), '%Y%m%d')
    for f in os.listdir(f'{file_dir}'):
        if start_time <= dt.datetime.strptime(str(f.split('.')[0][2:]), '%Y%m%d')\
                and dt.datetime.strptime(str(f.split('.')[0][2:]), '%Y%m%d') <= end_time:
            filelist.append(f)
    return [f'{file_dir}/{x}' for x in filelist]



if __name__ == '__main__':
    # fl = get_filelist('c:/cslo/data/ticket', 20180501, 20180503)
    print(get_flat_pair('1'))