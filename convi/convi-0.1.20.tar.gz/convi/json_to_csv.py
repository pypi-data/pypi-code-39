import hy.macros
import sys
import json
import csv
from anarcute import *
hy.macros.require('anarcute.lib', None, assignments='ALL', prefix='')
LIMIT = None


def process(data):
    res = []
    for r, row in enumerate(data):
        print(r)
        new = {}
        for k, v in row.items():
            if type(v) in [list, tuple]:
                new['{}_json'.format(k)] = json.dumps(v)
                new[k] = ','.join(list(map(str, v)))
                _hy_anon_var_2 = None
            else:
                if type(v) in [dict]:
                    new['{}_json'.format(k)] = json.dumps(v)
                    for i, j in v.items():
                        new['{}:{}'.format(k, i)] = j
                    _hy_anon_var_1 = None
                else:
                    new[k] = str(v)
                    _hy_anon_var_1 = None
                _hy_anon_var_2 = _hy_anon_var_1
        res.append(new)
    return res


def json_to_csv(inp, out, toprocess=True):
    data = json.load(open(inp, 'r+'))[slice(0, LIMIT)]
    if toprocess:
        data = process(data)
        _hy_anon_var_4 = None
    else:
        _hy_anon_var_4 = None
    fields = fieldnames(data)
    fields = sorted(fields, key=lambda x: ':' in x)
    writer = csv.DictWriter(open(out, 'w+'), fieldnames=fields)
    writer.writeheader()
    for r, row in enumerate(data):
        print('writerow', r)
        writer.writerow(row)
    return out


def csv_to_json(fcsv, fjson):
    it = fcsv
    it = load_csv(it)
    it = json.dumps(it, indent=4, sort_keys=True)
    it = open(fjson, 'w+').write(it)
    return it


if __name__ == '__main__':
    None if not 3 >= len(sys.argv) >= print(
        'Need arguments {input.json} and {output.csv}') else None
    INPUT = sys.argv[1]
    OUTPUT = sys.argv[2]
    _hy_anon_var_7 = print(json_to_csv(INPUT, OUTPUT))
else:
    _hy_anon_var_7 = None

