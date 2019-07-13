
from lxml import html as lxml_html


class BaseHtmlParser(object):
    def __init__(self, html_string=None):
        self.html_string = html_string
        self.document_tree = lxml_html.fromstring(html_string) if html_string else None

    def to_json(self):
        raise NotImplementedError()
