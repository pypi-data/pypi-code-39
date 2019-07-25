#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Classify topics and categories that won't be used in 'other'

def classifier(pages, classification_column, classification_wanted,pages_columns_dict):
    """
    Classify classification that won't be used in 'other'
    
    Parameters
    ----------
        pages: pandas dataframe of pages
        
        classification_column: string, classification column wanted to be classified
        
        classification_wanted: list of string, classication wanted to be kept 

        pages_columns_dict: dict

    Returns
    -------
        Pandas Series
    """
    pages = pages.copy(deep=True)
    pages.loc[~pages[classification_column].isin(classification_wanted), classification_column] = 'Other'
    return pages[classification_column];
