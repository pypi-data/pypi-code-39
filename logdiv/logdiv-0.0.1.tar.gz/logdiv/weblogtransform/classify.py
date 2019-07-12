#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Classify topics and categories that won't be used in 'other'

def classifier(pages, topics, categories,pages_columns_dict):
    """
    Classify topics and categories that won't be used in 'other'
    """
    pages = pages.copy(deep=True)
    pages.loc[~pages[pages_columns_dict['topic_column']].isin(topics), pages_columns_dict['topic_column']] = 'Other'
    pages.loc[~pages[pages_columns_dict['category_column']].isin(categories), pages_columns_dict['category_column']] = 'other'
    return pages[[pages_columns_dict['topic_column'],pages_columns_dict['category_column']]];
