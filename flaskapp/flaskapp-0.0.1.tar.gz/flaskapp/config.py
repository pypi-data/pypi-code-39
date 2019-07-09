from pathlib import Path
p = Path(__file__)

BASE_DIR = p.parent.resolve()
TEMP_DIR = BASE_DIR.joinpath('temp')

if __name__ == '__main__':
    _locals = dict(locals())
    for k, v in _locals.items():
        if '_DIR' in k:
            print(k, ':', v)

