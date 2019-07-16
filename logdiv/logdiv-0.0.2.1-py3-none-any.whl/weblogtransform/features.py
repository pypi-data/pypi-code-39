import pandas as pd

def assign_page_classification(weblog,pages,weblog_columns_dict,pages_columns_dict):
    """
    Associate each category and topic of requested and referrer pages of weblog using pages.csv file
    """
    weblog['requested_category']=weblog[weblog_columns_dict['requested_page_column']].map(pd.Series(index=pages[pages_columns_dict['page_id_column']].\
                                                                       values, data=pages[pages_columns_dict['category_column']].values))
    weblog['referrer_category']=weblog[weblog_columns_dict['referrer_page_column']].map(pd.Series(index=pages[pages_columns_dict['page_id_column']].\
                                                                       values,data=pages[pages_columns_dict['category_column']].values))
    weblog['requested_topic']=weblog[weblog_columns_dict['requested_page_column']].map(pd.Series(index=pages[pages_columns_dict['page_id_column']].\
                                                                       values,data=pages[pages_columns_dict['topic_column']].values))
    weblog['referrer_topic'] = weblog[weblog_columns_dict['referrer_page_column']].map(pd.Series(index=pages[pages_columns_dict['page_id_column']].\
                                                                       values,data=pages[pages_columns_dict['topic_column']].values))
    return weblog;
