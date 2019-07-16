import base64
import json
import hmac
import hashlib


def _parse_cookie(cookie_value=None):
    fp = u''
    cid = u''

    if cookie_value is None:
        return cid, fp

    try:
        base64_decoded = base64.b64decode(cookie_value)
        if base64_decoded is None:
            base64_decoded = u'{}'

        json_obj = json.loads(base64_decoded)

        if u'fp' in json_obj:
            fp = json_obj['fp']

        if u'cid' in json_obj:
            cid = json_obj['cid']
    except Exception as ex:
        pass

    return cid, fp


def verify_signature(secret, text_body, header_signature):
    try:
        key = secret.encode('utf-8')
        body = text_body.encode('utf-8')
        comparison_signature = hmac.new(key, body, hashlib.sha512).hexdigest()
        return hmac.compare_digest(comparison_signature, header_signature)
    except Exception as ex:
        return False
