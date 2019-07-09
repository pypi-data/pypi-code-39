# -*- coding: utf-8 -*-

import csv


def get_csv_data(path):
    with open(path, 'r', encoding="utf-8") as f:
        from_reader = csv.reader(f)
        data = []
        for row in from_reader:
            data.append(row)
    return data


def merge_csv(paths: list):
    header = []
    body_dic = dict()
    for path in paths:
        f_csv = get_csv_data(path)
        if not check_header(f_csv[0]):
            return False, path
        header = merge_header(header, f_csv[0])
        for row in f_csv[1:]:
            if row[0] in body_dic:  # update row
                body_dic[row[0]] = merge_row(zip(f_csv[0], row), header)
            else:  # add row
                body_dic[row[0]] = row
    retval = [header]
    for value in body_dic.values():
        while len(value) < len(header):
            value.append("")
        retval.append(value)
    return True, retval


def check_header(header):
    if header[0] == 'uuid':
        return True
    else:
        return False


def merge_header(header1, header2):
    row = header1 + header2
    retval = list(set(row))
    retval.sort(key=row.index)
    return retval


def merge_row(f_row, header):
    f_row_dic = {}
    for key, value in f_row:
        f_row_dic[key] = value

    retval = []
    for key in header:
        retval.append(f_row_dic.get(key, ""))
    return retval


if __name__ == "__main__":
    pass
