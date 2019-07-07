from gerridae.field import BaseField
import requests
from lxml import etree


class ItemMeta(type):

    def __new__(cls, name, bases, attrs):
        __fields = {field_name: attrs.pop(field_name) for field_name, obj in list(attrs.items()) if
                    isinstance(obj, BaseField)}
        attrs['__fields'] = __fields
        return type.__new__(cls, name, bases, attrs)


class Item(metaclass=ItemMeta):

    def __init__(self):
        self.result = {}

    @staticmethod
    def _get_html(html, url, **kwargs):
        """获取 etree.HTML obj"""
        if html or url:
            if url:
                res = requests.get(url, **kwargs)
                html = res.text
                return etree.HTML(html)
            return etree.HTML(html)
        raise ValueError('html or url is expected')

    @classmethod
    def _parser_html(cls, *, html_etree):
        if html_etree is None:
            return ValueError('html_etree is expected')
        item_ins = cls()

        fields = getattr(item_ins, '__fields', {})
        for field_name, field_value in fields.items():
            value = field_value.extract(html_etree)
            setattr(item_ins, field_name, value)
            item_ins.result[field_name] = value
        return item_ins

    @classmethod
    def get_item(cls, html=None, url=None):
        if html or url:
            html_etree = cls._get_html(html, url)
            return cls._parser_html(html_etree=html_etree)
        raise ValueError('html or url is excepted')

    # @classmethod
    # def get_items(cls, html=None, url=None):
    #     if html or url:
    #         html_etree = cls._get_html(html, url)
    #         return cls._parser_html(html_etree=html_etree)
    #     raise ValueError('html or url is excepted')
