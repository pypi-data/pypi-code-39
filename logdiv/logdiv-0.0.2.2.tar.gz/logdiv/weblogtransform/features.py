import pandas as pd

def assign_page_classification(weblog,pages,classification_columns,weblog_columns_dict,pages_columns_dict):
    """
    Associate each category and topic of requested and referrer pages of weblog using pages.csv file
        
    Parameters
    ----------
        weblog: pandas dataframe of requests

        pages: pandas dataframe of pages
            
        classification_columns: list of string, associate each classification wanted to each page in weblog file

        weblog_columns_dict: dict

        pages_columns_dict: dict

    Returns
    -------
        Pandas Dataframe
    """
    for classification_column in classification_columns:
        
        weblog['requested_'+classification_column]=weblog[weblog_columns_dict['requested_page_column']].map(pd.Series(index=pages\
                          [pages_columns_dict['page_id_column']].values, data=pages[classification_column].values))
        weblog['referrer_'+classification_column]=weblog[weblog_columns_dict['referrer_page_column']].map(pd.Series(index=pages\
                          [pages_columns_dict['page_id_column']].values,data=pages[classification_column].values))
    return weblog;
