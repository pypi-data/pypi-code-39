class BaseField:
    """base field"""

    def __init__(self, default=None):
        self.default = default

    def extract(self, *args, **kwargs):
        raise NotImplementedError('extract is not implemented.')


class _LXMLElementField(BaseField):
    """usage TextField Attribute """

    def __init__(self, css_select=None, default=None):
        super(_LXMLElementField, self).__init__(default)
        self.css_select = css_select

    def _get_elements(self, *, html_etree):
        if self.css_select:
            elements = html_etree.cssselect(self.css_select)
        else:
            raise ValueError(f'{self.__class__.__name__} field css_select is expected')
        return elements

    def _parser_element(self, element):
        raise NotImplementedError

    def extract(self, html_etree):
        elements = self._get_elements(html_etree=html_etree)
        if elements:
            result = [self._parser_element(element) for element in elements]
        else:
            result = []
        return result


class TextField(_LXMLElementField):
    """text filed"""

    def __init__(self, css_select=None, default=None):
        super(TextField, self).__init__(css_select, default)

    def _parser_element(self, element):
        strings = [node.strip() for node in element.itertext()]
        string = ''.join(strings)
        return string if string else self.default


class AttrField(_LXMLElementField):
    """attribute field"""

    def __init__(self, css_select=None, attr=None, default=None):
        super(AttrField, self).__init__(css_select, default)
        self.attr = attr

    def _parser_element(self, element):
        pass
