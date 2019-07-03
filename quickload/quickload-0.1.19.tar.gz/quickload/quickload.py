import os
import json
def first(x):
	return x[0]
def last(x):
	return x[-1]

def load(package):
    current_version = None
    res = os.popen('pip3 search {}'.format(package)).read()
    lines = res.split('\n')
    for i, line in enumerate(lines):
        n = 1 + i
        if first(line.split(' ')).lower().startswith(package.lower()):
            version = first(last(line.split('(')).split(')'))
            if len(lines) > n and 'INSTALLED' in lines[n]:
                current_version = first(last(lines[n].split(': ')).split(' '))
                _hy_anon_var_1 = None
            else:
                _hy_anon_var_1 = None
            cmd = 'pip3 install --upgrade {}'.format(package)
            print(cmd)
            os.popen(cmd).read() if version != current_version else None
            return True
            _hy_anon_var_2 = None
        else:
            _hy_anon_var_2 = None


def ql(*args):
    for package in args:
        load(package)


def un(package):
    return os.popen('pip3 uninstall {}'.format(package))

