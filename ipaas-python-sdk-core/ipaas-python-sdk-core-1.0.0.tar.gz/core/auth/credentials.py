class AccessKeyCredential:
    def __init__(self, access_key_id, access_key_secret):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret


class RsaKeyPairCredential:
    def __init__(self, public_key_id, private_key, session_period=3600):
        self.public_key_id = public_key_id
        self.private_key = private_key
        self.session_period = session_period
