import pathlib
import datetime
import pytz
import pandas as pd
from datasetmaker.models import Client
from .download import NewsFetcher


class MyNewsFlashClient(Client):
    def _sync_raw_data(self, path):
        # Look up datetime of latest retrieved article
        path = pathlib.Path(path)
        fnames = sorted([x for x in path.glob('*.csv')])
        latest_month_path = fnames[-1]
        frame = pd.read_csv(latest_month_path)
        frame.indexed = pd.to_datetime(frame.indexed)
        start_time = frame.indexed.sort_values().iloc[-1]

        # Fetch data up until the current datetime
        data = self._fetch_articles(start_time)
        df = pd.DataFrame(data)
        if df.empty:
            return
        df.indexed = pd.to_datetime(df.indexed)

        # Save the data
        df['label'] = df.indexed.dt.year.astype(str)
        df.label = df.label + '-'
        df.label = df.label + (df.indexed.dt.month.astype(str).str.zfill(2))
        for label in df.label.unique():
            fname = path / f'{label}.csv'
            if fname.exists():
                month = pd.read_csv(fname)
                month.indexed = pd.to_datetime(month.indexed)
                month = pd.concat([month, df[df.label == label]].copy(),
                                  sort=True)
            else:
                month = df[df.label == label].copy()
            month = month.sort_values(['indexed', 'headline'])
            month = month.drop(['country',
                                'image',
                                'language',
                                'links',
                                'reference'], axis=1)

            month.to_csv(fname, index=False)

    def _fetch_articles(self, start_time):
        fetcher = NewsFetcher()
        end_time = datetime.datetime.now(tz=pytz.timezone('UTC'))
        data = fetcher.fetch_period(start_time, end_time)
        return data

    def get(self, raw_data_path):
        self._sync_raw_data(raw_data_path)

    def save(self, path, **kwargs):
        pass
