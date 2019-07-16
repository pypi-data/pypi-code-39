import imp
import sys
import subprocess


def urllib_model(u, host, path):
    ssh = subprocess.Popen(['ssh', host, 'cat', path],
                           stdout=subprocess.PIPE)
    u = ssh.stdout.read()

    source = u.decode('utf-8')
    mod = sys.modules.setdefault(path, imp.new_module(path))
    code = compile(source, path, 'exec')
    mod.__file__ = path
    mod.__package__ = ''
    exec(code, mod.__dict__)
    return mod

