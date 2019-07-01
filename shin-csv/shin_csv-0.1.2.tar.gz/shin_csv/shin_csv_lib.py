from hy.core.language import first, name
import os


def escape(name):
    return '"{}"'.format(name.replace('"', '\\"').replace('(', '\\(').
        replace(')', '\\)')) if ' ' in name else name


def file_len(fname):
    return int(first(os.popen('wc -l {}'.format(escape(fname))).read().
        split(' ')))


def file_get(fname, n):
    return os.popen('sed -n {}p {}'.format(n, fname)).read()


def csv_to_arr(cstr, delimiter=',', quotation='"'):
    arr = []
    buffer = ''
    escape = False
    for i, c in enumerate(cstr):
        if i == len(cstr) - 1 or c == delimiter and not escape:
            arr.append(((int if 0 == float(buffer) % 1 else float) if not
                escape and buffer.isdigit() else str)(buffer))
            buffer = ''
            _hy_anon_var_5 = None
        else:
            if c == quotation:
                escape = not escape
                _hy_anon_var_4 = None
            else:
                buffer = buffer + c
                _hy_anon_var_4 = None
            _hy_anon_var_5 = _hy_anon_var_4
    return arr


def csv_get(fname, n):
    obj = {}
    fieldnames = csv_to_arr(file_get(fname, 1))
    row = csv_to_arr(file_get(fname, n))
    for i in range(0, min(len(fieldnames), len(row))):
        obj[fieldnames[i]] = row[i]
    return obj


class LineReader(object):

    def __init__(self, fname):
        self.next_num = 2
        self.fname = fname
        return None

    def next(self):
        row = csv_get(self.fname, self.next_num)
        if row or self.next_num <= file_len(self.fname):
            self.next_num = 1 + self.next_num
            _hy_anon_var_9 = None
        else:
            row = None
            _hy_anon_var_9 = None
        return row




