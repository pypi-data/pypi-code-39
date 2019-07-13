import os
import datetime as dt
import pandas
import feedparser
import quandl
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

YAHOO_URL = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=US&lang=en-US'
DATA_FOLDER = 'data'
NASDAQ_CLOSING_HOUR = 12
quandl.ApiConfig.api_key = "INSERT_KEY"


def touch(file):
    """
    Check if file exists, if not, create it
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    path = '%s/%s' % (DATA_FOLDER, file)
    if not os.path.isfile(path):
        with open(path, 'a') as file:
            os.utime(path, None)
            file.write('guid,stock,title,summary,published,stock_open,stock_close,sentiment_summary, sentiment_title')


def read_rss(stocks, use_csv=True, file='news.csv'):
    """
    :param stocks: list of stocks to check from yahoo
    :param use_csv: read/save to csv
    :param file: csv to save to
    :return: pandas.DataFrame
    """

    """Create the file"""
    if use_csv:
        touch(file)
        df = pandas.read_csv(DATA_FOLDER + '/' + file, header=0)
    else:
        df = pandas.DataFrame(
            columns=['guid', 'stock', 'title', 'summary', 'published', 'stock_open', 'stock_close', 'sentiment_summary',
                     'sentiment_title']
        )

    """Download VADER"""
    try:
        nltk.data.find('vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon')

    for stock in stocks:

        """Init new Parser"""
        feed = feedparser.parse(YAHOO_URL % stock)

        for entry in feed.entries:

            """Find guid and skip if exists"""
            guid = df.loc[df['guid'] == entry.guid]
            if len(guid) > 0:
                continue

            """Analyze the sentiment"""
            sia = SentimentIntensityAnalyzer()
            _summary = sia.polarity_scores(entry.summary)['compound']
            _title = sia.polarity_scores(entry.title)['compound']

            """Set opening and closing values. These will be updated later"""
            _open = 0
            _close = 0

            """Add new entry to DF"""
            row = [entry.guid, stock, entry.title, entry.summary, entry.published, _open, _close, _summary, _title]
            df.loc[len(df)] = row

        """Save to CSV"""
        if use_csv:
            df.to_csv(DATA_FOLDER + '/' + file, index=False)

    return df


def update_stock_values(file='news.csv'):
    """
    Check for zero values in opening and closing values for the past and update them
    :param file:
    :return:
    """
    df = pandas.read_csv(DATA_FOLDER + '/' + file, header=0)

    for index, row in df.iterrows():

        """Parse the Date from CSV"""
        date_time_check = dt.datetime.strptime(row['published'], '%a, %d %b %Y %H:%M:%S +0000')

        """Adjust the closing of NASDAQ (if after, the news has no influence of the news date)"""
        date_time_close = dt.datetime(date_time_check.year, date_time_check.month, date_time_check.day,
                                      NASDAQ_CLOSING_HOUR, 0, 0)

        """If it was after opening hours, select next day"""
        if date_time_check > date_time_close:
            date_time_check += dt.timedelta(days=1)

        """TODO: CHECK FOR WEEKEND"""

        stock_value = quandl.get('WIKI/' + row['stock'], start_date=date_time_check, end_date=date_time_check)
        print(stock_value)

        exit()
