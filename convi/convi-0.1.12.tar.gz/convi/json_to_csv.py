import hy.macros
from hy.core.shadow import hyx_Xplus_signX
import sys
import json
import csv
from anarcute import *
hy.macros.require('anarcute.lib', None, assignments='ALL', prefix='')
LIMIT = None


def fieldnames(arr):
    return list(set(hyx_Xplus_signX(*list(map(lambda x: list(x.keys()), arr))))
        )


def process(data):
    res = []
    for r, row in enumerate(data):
        print(r)
        new = {}
        for k, v in row.items():
            if type(v) in [list, tuple]:
                new[k] = ','.join(list(map(str, v)))
                _hy_anon_var_3 = None
            else:
                if type(v) in [dict]:
                    for i, j in v.items():
                        new['{}_{}'.format(k, i)] = j
                    _hy_anon_var_2 = None
                else:
                    new[k] = str(v)
                    _hy_anon_var_2 = None
                _hy_anon_var_3 = _hy_anon_var_2
        res.append(new)
    return res


def json_to_csv(inp, out):
    data = json.load(open(inp, 'r+'))[slice(0, LIMIT)]
    data = process(data)
    fields = fieldnames(data)
    fields = sorted(fields, key=lambda x: '_' in x)
    writer = csv.DictWriter(open(OUTPUT, 'w+'), fieldnames=fields)
    writer.writeheader()
    for r, row in enumerate(data):
        print('writerow', r)
        writer.writerow(row)
    return out


if __name__ == '__main__':
    None if not 3 >= len(sys.argv) >= print(
        'Need arguments {input.json} and {output.csv}') else None
    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]
    _hy_anon_var_6 = print(json_to_csv(INPUT, OUTPUT))
else:
    _hy_anon_var_6 = None

