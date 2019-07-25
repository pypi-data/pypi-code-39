import pandas as pd

# Convert string timestamp in pandas timestamp

def pd_timestamp_convertor(weblog, timestamp_column):
    """
    Convert string timestamp in pandas timestamp
    """
    weblog = weblog.copy(deep=True)
    weblog[timestamp_column]=weblog[timestamp_column].apply(lambda x: pd.Timestamp(x))
    return weblog[timestamp_column];

