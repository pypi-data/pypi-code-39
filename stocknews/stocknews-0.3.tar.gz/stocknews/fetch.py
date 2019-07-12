import os
import pandas
import feedparser
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

YAHOO_URL = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=US&lang=en-US'


def touch(path):
    """
    Check if file exists, if not, create it
    """
    if not os.path.isfile(path):
        with open(path, 'a') as file:
            os.utime(path, None)
            file.write('guid,stock,title,summary,published, sentiment_summary, sentiment_title')


def read_rss(stocks, use_csv=True, file='data/news.csv'):
    """
    :param stocks: list of stocks to check from yahoo
    :param use_csv: read/save to csv
    :param file: csv to save to
    :return: pandas.DataFrame
    """

    """Create the file"""
    if use_csv:
        touch(file)
        df = pandas.read_csv(file, header=0)
    else:
        df = pandas.DataFrame(
            columns=['guid', 'stock', 'title', 'summary', 'published', 'sentiment_summary', 'sentiment_title']
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

            """Add new entry to DF"""
            row = [entry.guid, stock, entry.title, entry.summary, entry.published, _summary, _title]
            df.loc[len(df)] = row

        """Save to CSV"""
        if use_csv:
            df.to_csv(file, index=False)

    return df
