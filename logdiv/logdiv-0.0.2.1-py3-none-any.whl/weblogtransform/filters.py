
def filter_weblog_by_dates(weblog,start,end, timestamp_column):
  return weblog[(weblog[timestamp_column]>start)&(weblog[timestamp_column]<end)];
