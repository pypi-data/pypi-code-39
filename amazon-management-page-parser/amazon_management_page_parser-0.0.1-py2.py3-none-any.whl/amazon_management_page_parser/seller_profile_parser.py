# -*- coding: utf-8 -*-

# Copyright © 2019 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from parsel import Selector

from amazon_management_page_parser import logger


class SellerProfileParser(object):
    def __init__(self, text, type='html', namespaces=None, root=None, base_url=None):
        self.selector = Selector(
            text, type=type, namespaces=namespaces, root=root, base_url=base_url)

    def parse(self):
        seller_name = self.selector.xpath('//h1[@id="sellerName"]/text()').extract_first()
        seller_storefront_url = self.selector.xpath(
            '//div[@id="storefront-link"]/a/@href').extract_first()
        return {
            'name': seller_name,
            'storefront_url': seller_storefront_url,
            'feedbacks': self.parse_feedbacks()
        }

    def parse_feedbacks(self):
        feedback_range_names = ['30days', '90days', '12mons', 'lifetime']
        feedbacks = dict()

        feedback_row_elems = self.selector.xpath('//table[@id="feedback-summary-table"]/tbody/tr')
        feedback_row_elems.pop(0)

        for feedback_row_elem in feedback_row_elems:
            column_elems = feedback_row_elem.xpath('./td')
            header_elem = column_elems.pop(0)
            header = header_elem.xpath('./text()').extract_first()
            if not header:
                raise ValueError('Could not find feedback level name!')

            header = header.strip().lower()
            for idx, feedback_range_name in enumerate(feedback_range_names):
                val = ''.join(
                    [text.strip() for text in column_elems[idx].xpath('.//text()').getall() if text.strip()])
                val = '0' if val == '-' else val

                if feedback_range_name not in feedbacks:
                    feedbacks[feedback_range_name] = dict()
                feedbacks[feedback_range_name][header] = val

        return feedbacks
