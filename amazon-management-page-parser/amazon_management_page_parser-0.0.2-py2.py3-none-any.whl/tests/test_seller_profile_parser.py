# -*- coding: utf-8 -*-

# Copyright © 2019 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from amazon_management_page_parser.seller_profile_parser import SellerProfileParser

import pytest

def test_parse(seller_profile_page_sources, target_seller_profile_results):
    results = dict()
    for marketplace, page_sources_by_marketplace in seller_profile_page_sources.items():
        results[marketplace] = dict()
        for seller_id, page_source in page_sources_by_marketplace.items():
            parser = SellerProfileParser(page_source)
            results[marketplace][seller_id] = parser.parse()

    for marketplace, results_by_marketplace in results.items():
        target_results_by_marketplace = target_seller_profile_results.get(marketplace, dict())
        for seller_id, result in results_by_marketplace.items():
            target_result = target_results_by_marketplace.get(seller_id, dict())
            assert result == target_result
