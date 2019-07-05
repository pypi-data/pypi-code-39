import re

from parsel import Selector

from aliexpress_page_parser import logger


class ProductListParser(object):
    def __init__(self, text, type='html', namespaces=None, root=None, base_url=None):
        self.selector = Selector(
            text, type=type, namespaces=namespaces, root=root, base_url=base_url)

    def parse(self):
        result = {'products': []}

        next_page_elem = self.selector.xpath(
            '//div[@id="pagination-bottom"]/div[contains(@class, "ui-pagination-navi")]/a[contains(@class, "page-next")]')
        next_page_url = next_page_elem.xpath('./@href').extract_first()
        if next_page_url:
            if next_page_url.startswith('//'):
                next_page_url = 'https:' + next_page_url

            result['next_page_url'] = next_page_url

        grid_elems = self.selector.xpath('//ul[@id="hs-below-list-items"]/li')
        list_elems = self.selector.xpath('//ul[@id="hs-list-items"]/li')
        list_products_template = self.selector.xpath(
            '//div[@id="hs-below-list-items"]/script/text()').extract_first()
        if list_products_template:
            list_elems.extend(Selector(text=list_products_template).xpath('//ul/li'))

        for product_elem in grid_elems:
            try:
                result['products'].append(self.parse_grid_product(product_elem))
            except Exception as e:
                logger.exception(e)

        for product_elem in list_elems:
            try:
                result['products'].append(self.parse_list_product(product_elem))
            except Exception as e:
                logger.exception(e)

        return result

    def parse_grid_product(self, product_elem):
        info_elem = product_elem.xpath('./div[@class="item"]/div[@class="info"]')
        if not info_elem:
            raise ValueError('Could not find product information!')

        title = info_elem.xpath('./h3/a/@title').extract_first()
        if not title:
            raise ValueError('Could not parse title.')

        url = info_elem.xpath('./h3/a/@href').extract_first()
        if url.startswith('//'):
            url = 'https:' + url

        matched = re.match(r".*www\.aliexpress\.com\/item\/.*\/([0-9]+)\.html\?.*", url)
        if matched and len(matched.groups()) > 0:
            product_id = matched.groups()[0]
        else:
            raise ValueError('Could not find product_id - %s' % url)

        try:
            price_str = info_elem.xpath(
                './span[contains(@class, "price")]/span[@itemprop="price"]/text()').extract_first()
            price = float(price_str.split('$').pop().strip().split('-').pop(0).strip())
        except:
            price = 0

        star_str = info_elem.xpath(
            './div[@class="rate-history"]/span[contains(@class, "star")]/@title').extract_first()
        if star_str:
            rating = float(star_str.split(':').pop().strip().split().pop(0))
        else:
            rating = 0

        feedback_str = info_elem.xpath(
            './div[@class="rate-history"]/a[contains(@class, "rate-num")]/@title').extract_first()
        if feedback_str:
            matched = re.match(r"Feedback\((.+)\)", feedback_str)
            if matched:
                feedbacks = int(matched.group(1))
            else:
                feedbacks = 0
        else:
            feedbacks = 0

        orders_str = info_elem.xpath(
            './div[@class="rate-history"]/span[contains(@class, "order-num")]/a/em/text()').extract_first()
        if orders_str:
            try:
                orders = int(
                    orders_str.strip().split(' ').pop().replace('(', '').replace(')', ''))
            except:
                orders = 0
        else:
            orders = 0

        return {
            'product_id': product_id,
            'title': title,
            'url': url,
            'price': price,
            'rating': rating,
            'feedback': feedbacks,
            'orders': orders
        }

    def parse_list_product(self, product_elem):
        detail_elem = product_elem.xpath('.//div[contains(@class, "detail")]/h3/a')

        title = detail_elem.xpath('./@title').extract_first().strip()
        if not title:
            raise ValueError('Could not parse title.')

        url = detail_elem.xpath('./@href').extract_first()
        if url.startswith('//'):
            url = 'https:' + url

        matched = re.match(r".*www\.aliexpress\.com\/item\/.*\/([0-9]+)\.html\?.*", url)
        if matched and len(matched.groups()) > 0:
            product_id = matched.groups()[0]
        else:
            raise ValueError('Could not find product_id - %s' % url)

        info_elem = product_elem.xpath('.//div[contains(@class, "infoprice")]')
        try:
            price_str = info_elem.xpath(
                './span[contains(@class, "price")]/span[@itemprop="price"]/text()').extract_first()
            price = float(price_str.split('$').pop().strip().split('-').pop(0).strip())
        except:
            price = 0

        star_str = info_elem.xpath(
            './div[@class="rate-history"]/span[contains(@class, "star")]/@title').extract_first()
        if star_str:
            try:
                rating = float(star_str.split(':').pop().strip().split().pop(0))
            except:
                rating = 0
        else:
            rating = 0

        feedback_str = info_elem.xpath(
            './div[@class="rate-history"]/a[contains(@class, "rate-num")]/text()').extract_first()
        if feedback_str:
            matched = re.match(r"Feedback\((.+)\)", feedback_str)
            if matched:
                feedbacks = int(matched.group(1))
            else:
                feedbacks = 0
        else:
            feedbacks = 0

        orders_str = info_elem.xpath(
            './div[@class="rate-history"]/span[contains(@class, "order-num")]/a/em/text()').extract_first()
        if orders_str:
            try:
                orders = int(
                    orders_str.strip().split(' ').pop().replace('(', '').replace(')', ''))
            except:
                orders = 0
        else:
            orders = 0

        return {
            'product_id': product_id,
            'title': title,
            'url': url,
            'price': price,
            'rating': rating,
            'feedback': feedbacks,
            'orders': orders
        }
