from .upandas import csv2dataframe
from .upandas import pd


def csv2xlsx(old: str, new: str, clean: bool = False) -> None:
    if not clean:
        if not isinstance(old, str) and not old.endswith('csv'):
            raise Exception(f'old {old} file must be csv')
        if not isinstance(new, str) and not new.endswith('xlsx'):
            raise Exception(f'old {new} file must be xlsx')
        pd.read_csv(old).to_excel('./tmp.xlsx')
    else:
        csv2dataframe(old).to_excel(new)


def trim_csv(file: str) -> None:
    csv2dataframe(file).to_csv(file)
