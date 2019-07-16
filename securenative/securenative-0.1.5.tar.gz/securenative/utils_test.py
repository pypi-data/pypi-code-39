import unittest

from securenative.utils import _parse_cookie, verify_signature


class UtilsTest(unittest.TestCase):
    def test_parse_cookie_valid_cookie(self):
        cookie = u'eyJjaWQiOiI2ZTQxOTgxNi01M2Q5LTRjNDktYWRhNy0zMzJjNDE0Y2ZjNzkiLCJmcCI6Ijc0NjUzN2Q5ZmRhZTI' \
                 u'wNjNmZjY2ZjRlYmZlZmYwYjRjLjI0NzAwZjlmMTk4NjgwMGFiNGZjYzg4MDUzMGRkMGVkIn0= '

        cid, fp = _parse_cookie(cookie)
        self.assertEqual(cid, u'6e419816-53d9-4c49-ada7-332c414cfc79')
        self.assertEqual(fp, u'746537d9fdae2063ff66f4ebfeff0b4c.24700f9f1986800ab4fcc880530dd0ed')

    def test_parse_cookie_invalid_cookie(self):
        cookie = u'syJjaWQiOiI2ZTQxOTgxNi01M2Q5LTRjNDktYWRhNy0zMzJjNDE0Y2ZjNzkiLCJmcCI6Ijc0NjUzN2Q5ZmRhZTI' \
                 u'wNjNmZjY2ZjRlYmZlZmYwYjRjLjI0NzAwZjlmMTk4NjgwMGFiNGZjYzg4MDUzMGRkMGVkIn0= '

        cid, fp = _parse_cookie(cookie)
        self.assertEqual(cid, u'')
        self.assertEqual(fp, u'')

    def test_parse_cookie_none_cookie(self):
        cookie = None

        cid, fp = _parse_cookie(cookie)
        self.assertEqual(cid, u'')
        self.assertEqual(fp, u'')

    def test_verify_signature_should_pass(self):
        secret = u'abc'
        text_body = u'{"key":"test1","value":"test2"}'
        header_sig = u'95a5de7fa0a9f8d1904b530d08b47bbb3a8236fec3409a1fb268dae6' \
                     u'36ba7582e5490154297e575a80bc9b1fd73ab82e8d606197f8db7f92e98e4dadd2910ef2'

        result = verify_signature(secret, text_body, header_sig)
        self.assertTrue(result)

    def test_verify_signature_should_not_pass(self):
        secret = u'abc'
        text_body = u'{"key":"test1","value":"test2"}'
        header_sig = u'85a5de7fa0a9f8d1904b530d08b47bbb3a8236fec3409a1fb268dae6' \
                     u'36ba7582e5490154297e575a80bc9b1fd73ab82e8d606197f8db7f92e98e4dadd2910ef2'

        result = verify_signature(secret, text_body, header_sig)
        self.assertFalse(result)
