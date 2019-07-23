import unittest
import os.path

from npm_audit_checkmk.lib import get_vulnerabilities, process
from npm_audit_checkmk.__main__ import create_parser

with open(os.path.dirname(__file__) + '/example.json') as file:
    FILE = file.read()


class TestsLib(unittest.TestCase):
    def test_get_vulnerabilities(self):
        self.assertEqual({
            "info": 0,
            "low": 7,
            "moderate": 2,
            "high": 55,
            "critical": 0
        }, get_vulnerabilities(FILE))

    def test_process(self):
        parser = create_parser()
        args = parser.parse_args(['-s', 'frontend_vulnerabilities',
                                  '-ic', '12', '-iw', '1', '-lc', '2'])
        self.assertEqual(process({
            "info": 0,
            "low": 7,
            "moderate": 2,
            "high": 55,
            "critical": 0
        }, args),
            """<<<local>>>
P frontend_vulnerabilities INFO=0;1;12|LOW=7;20;2|MODERATE=2;10;20|HIGH=55;1;3|CRITICAL=2;0;0 See `npm audit` for more details.
""")
