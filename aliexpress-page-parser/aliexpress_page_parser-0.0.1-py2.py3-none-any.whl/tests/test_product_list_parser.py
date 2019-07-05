from aliexpress_page_parser.product_list_parser import ProductListParser

import pytest

def test_parse_grid_products(product_grid_page_source, product_list_page_source, target_grid_products_result, target_list_products_result):
    samples = [
        {
            'product_page_source': product_grid_page_source,
            'target_products_result': target_grid_products_result
        },
        {
            'product_page_source': product_list_page_source,
            'target_products_result': target_list_products_result
        }
    ]
    for sample in samples:
        target_products_result = sample['target_products_result']

        parser = ProductListParser(sample['product_page_source'])
        products_result = parser.parse()
        assert products_result['next_page_url'] == target_products_result['next_page_url']

        products = {product['product_id']:product for product in products_result['products']}
        for target_product in target_products_result['products']:
            assert target_product['product_id'] in products

            product = products[target_product['product_id']]
            assert product['title'] == target_product['title']
            assert product['url'] == target_product['url']
            assert product['price'] == target_product['price']
            assert product['rating'] == target_product['rating']
            assert product['feedback'] == target_product['feedback']
            assert product['orders'] == target_product['orders']
