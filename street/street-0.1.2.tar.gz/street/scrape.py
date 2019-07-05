from bs4 import BeautifulSoup
import pandas as pd
import requests

from .exceptions import (
    DistilIdentificationBlocked,
    EarningsTableEmpty,
    EarningsTableNotFound,
    RequestBlocked,
    ResourceMovedTemporarily,
    UnforeseenResponseStatusCode,
)


class StreetScraper:
    REFERER = 'https://www.google.com/'

    def __init__(self, user_agent, cookie):
        self.user_agent = user_agent
        self.cookie = cookie


    def scrape(self, ticker_symbol):
        url = f'https://www.streetinsider.com/ec_earnings.php?q={ticker_symbol}'

        headers = {
            'User-Agent': self.user_agent,
            'Referer': self.__class__.REFERER,
            'Cookie': self.cookie,
        }

        r = requests.get(url, headers=headers)
        if r.status_code == 416:
            raise RequestBlocked
        elif r.status_code == 302:
            raise ResourceMovedTemporarily
        elif r.status_code != 200:
            raise UnforeseenResponseStatusCode

        page = r.text
        soup = BeautifulSoup(page, 'lxml')

        distil_id_block = soup.find('div', {'id': 'distilIdentificationBlock'})
        if distil_id_block:
            raise DistilIdentificationBlocked


        tables = soup.find_all('table', {'class': 'earning_history'})
        if not tables:
            raise EarningsTableNotFound


        TARGET_ROW_CLASSES = ['is_hilite', 'is_future', 'LiteHover']

        data = []
        for table in tables:
            rows = table.find_all('tr', {'class': TARGET_ROW_CLASSES})
            for row in rows:
                cells = row.find_all('td')
                row_text = [cell.text for cell in cells]
                data.append(row_text)
        earn = pd.DataFrame(data)

        if earn.empty:
            raise EarningsTableEmpty

        dropped_cols = [1, 8, 9, 10, 11]
        earn = earn.drop(dropped_cols, axis=1)

        renamed_cols = {
            0: 'DATE',
            2: 'QTR',
            3: 'EPS',
            4: 'EPS_CONSENSUS',
            5: 'SURPRISE',
            6: 'REVENUE',
            7: 'REVENUE_CONSENSUS',
        }
        earn = earn.rename(index=str, columns=renamed_cols)

        earn['DATE'] = pd.to_datetime(earn['DATE'])
        earn = earn.sort_values('DATE', ascending=False)

        return earn