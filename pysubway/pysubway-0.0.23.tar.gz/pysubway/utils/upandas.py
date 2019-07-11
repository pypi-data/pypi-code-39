import os
import secrets

import pandas as pd

from .file import Open

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def csv2dataframe(file: str) -> pd.DataFrame:
    tmp_csv = os.path.join(THIS_DIR, '.'.join((secrets.token_hex(), 'csv')))
    with Open(file) as f:
        with open(tmp_csv, mode='w', encoding='utf-8') as fc:
            fc.write(f.read())
        tmp = pd.read_csv(tmp_csv).iterrows()
        frame = []
        for i in tmp:
            series = {}
            for w in i[1].iteritems():
                k = "".join(str(w[0]).split())
                v = "".join(str(w[1]).split())
                series[k] = v.strip('"')
            frame.append(series)
        return pd.DataFrame(frame)


def csv2xlsx(old: str, new: str, clean: bool = False) -> None:
    if not clean:
        if not isinstance(old, str) and not old.endswith('csv'):
            raise Exception(f'old {old} file must be csv')
        if not isinstance(new, str) and not new.endswith('xlsx'):
            raise Exception(f'old {new} file must be xlsx')
        pd.read_csv(old).to_excel('./tmp.xlsx')
    else:
        csv2dataframe(old).to_excel(new)
