import hy.macros
import json
import csv
import sys
import fs
hy.macros.require('hy.extra.anaphoric', None, assignments='ALL', prefix='')


def fieldnames(arr):
    fields = {}
    for obj in arr:
        for key in obj:
            fields[key] = key
    return fields.keys()


def prettify(obj):
    for k, v in obj.items():
        if type(v) in [list, tuple]:
            obj[k] = ','.join(list(map(str, v)))
            _hy_anon_var_2 = None
        else:
            _hy_anon_var_2 = None
    return obj


def json_to_csv(js, name_csv=None):
    data = json.load(open(js, 'r+')) if js.endswith('.json') else json.loads(js
        )
    data = data if type(data) in [list, tuple] else [data]
    data = list(map(prettify, data))
    fields = fieldnames(data)
    file_csv = open(name_csv, 'w+') if name_csv else fs.open_fs('mem://').open(
        'tmp.csv', 'w+')
    writer = csv.DictWriter(file_csv, fieldnames=fields)
    writer.writeheader()
    for obj in data:
        writer.writerow(obj)
    return name_csv


if __name__ == '__main__':
    if not 2 <= len(sys.argv):
        print('Please, give {name.json} {name.csv} as arguments')
        _hy_anon_var_5 = sys.exit()
    else:
        _hy_anon_var_5 = None
    _hy_anon_var_6 = print(json_to_csv(*sys.argv[slice(1, None)]))
else:
    _hy_anon_var_6 = None


