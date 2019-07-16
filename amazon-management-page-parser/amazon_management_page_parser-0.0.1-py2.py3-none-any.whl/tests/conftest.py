# -*- coding: utf-8 -*-

# Copyright © 2019 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import os
import io
import glob

import pytest


@pytest.fixture(scope='session')
def pages_dir():
    return os.path.join(os.path.dirname(__file__), 'pages')

@pytest.fixture(scope='session')
def seller_profile_page_sources(pages_dir):
    sources = dict()

    profile_pathes = glob.glob('{}/seller_profile*.html'.format(pages_dir))
    for profile_path in profile_pathes:
        file_name, _ = os.path.splitext(os.path.basename(profile_path))
        parts = file_name.split('_')
        seller_id = parts.pop()
        marketplace = parts.pop().lower()
        sources.setdefault(marketplace, dict())

        with io.open(profile_path, 'rb') as fh:
            content = fh.read().decode('utf-8', 'ignore')
            sources[marketplace][seller_id] = content

    return sources

@pytest.fixture(scope='session')
def target_seller_profile_results():
    return {
        'us': {
            'A2PVUWGZKLDKE2': {
                'name': 'RockStream',
                'storefront_url': '/shops/A2PVUWGZKLDKE2?ref_=v_sp_storefront',
                'feedbacks': {
                    '30days': {
                        'positive': '0%',
                        'neutral': '0%',
                        'negative': '100%',
                        'count': '1'
                    },
                    '90days': {
                        'positive': '70%',
                        'neutral': '5%',
                        'negative': '25%',
                        'count': '20'
                    },
                    '12mons': {
                        'positive': '70%',
                        'neutral': '5%',
                        'negative': '25%',
                        'count': '20'
                    },
                    'lifetime': {
                        'positive': '70%',
                        'neutral': '5%',
                        'negative': '25%',
                        'count': '20'
                    }
                }
            }
        }
    }
