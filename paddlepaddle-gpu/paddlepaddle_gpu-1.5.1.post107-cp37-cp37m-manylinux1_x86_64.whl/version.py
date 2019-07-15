# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.5.1'
major           = '1'
minor           = '5'
patch           = '1'
rc              = '0'
istaged         = False
commit          = 'bc9fd1fc10f5ff3a2310cd1e04b40309ce508cf7'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
