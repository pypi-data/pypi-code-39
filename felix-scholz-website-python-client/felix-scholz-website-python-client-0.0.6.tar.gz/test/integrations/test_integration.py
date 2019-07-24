# coding: utf-8

"""
    Test the python client integrated

    Contact: felix@felix-scholz.org
"""
from __future__ import absolute_import

import hashlib
import os
import random
from typing import Optional
from unittest import TestCase

import requests

from website_python_client.configuration import Configuration


class IntegrationTestCase(TestCase):

    def setUp(self) -> None:
        self.config = Configuration()
        self.config.api_key['X-API-FELIX-SCHOLZ-WEBSITE'] = 'a8bcf73eb05a5084b0f0a38516814d07'
        self.config.api_key['API-READ-TOKEN'] = 'ccaf46b363fbc9d89819a2c31974a7f9'
        self.config.api_key['API-WRITE-TOKEN'] = '839e34d435821ae335d208fbee79bd91'
        self.config.host = 'http://localhost:8000/api/1.0.0'

    @staticmethod
    def generate_test_image(text: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None,
                            bg: Optional[str] = None, color: Optional[str] = None) -> str:
        url: str = 'https://dummyimage.com'
        if height is None:
            height = random.randint(100, 1000)
        url += '/' + str(height)
        if width is None:
            width = random.randint(100, 1000)
        url += 'x' + str(width)
        if bg is None:
            bg = ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        url += '/' + bg
        if color is None:
            color = ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        url += '/' + color

        extension = random.choice(['png', 'gif', 'jpg'])
        url += '.' + extension

        if text is not None:
            url += '&text=' + text

        response = requests.get(url)

        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        filename = m.hexdigest() + '.' + extension
        if not os.path.isdir('/tmp/website-client'):
            os.mkdir('/tmp/website-client')
        filename = '/tmp/website-client/' + filename
        with open(filename, "wb") as file:
            file.write(response.content)
            file.close()

        return filename

    @staticmethod
    def generate_test_markdown(text: Optional[str] = None) -> str:
        if text is None:
            text = """
            # Test Content
            This is a test description.
            * test 1
            * test 3
            * test 3
            """

        m = hashlib.md5()
        m.update(text.encode('utf-8'))
        filename = m.hexdigest() + '.md'

        if not os.path.isdir('/tmp/website-client'):
            os.mkdir('/tmp/website-client')

        filename = '/tmp/website-client/' + filename
        with open(filename, "wb") as file:
            file.write(bytes(text))
            file.close()

        return filename
