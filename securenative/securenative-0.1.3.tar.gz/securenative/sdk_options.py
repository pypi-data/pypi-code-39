_securenative_prod = u"https://api.securenative.com"
_securenative_stg = u"https://api.securenative-stg.com"


class SecureNativeOptions:
    def __init__(self, api_url=_securenative_prod, interval=1000, max_events=1000, timeout=1500, auto_send=True):
        super().__init__()
        self.timeout = timeout
        self.max_events = max_events
        self.api_url = api_url
        self.interval = interval
        self.auto_send = auto_send
