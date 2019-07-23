import pandas as pd

class DataFrame:

    def __new__(self, data)->pd.DataFrame:
        if isinstance(data, dict):
            return pd.DataFrame(data, index=[0])
        else:
            raise NotImplementedError()