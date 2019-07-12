from swissarmykit.req.RequestBase import RequestBase


class HeadersUtils(RequestBase):

    def __init__(self):
        super().__init__()
        self.extra_headers = {}
        self._has_br = False  # https://stackoverflow.com/questions/49584929/unable-to-decode-python-web-request

    def set_headers(self, headers_str=None):
        ''' Header str get from Chrome console. '''
        for h in headers_str.splitlines():
            header = h.strip()
            if h:
                key_value = header.split(':', 1)
                if len(key_value) == 2:
                    self.extra_headers[key_value[0].strip()] = key_value[1].strip()
        self._validate()

    def reset_headers(self):
        self.extra_headers = {}

    def get_headers(self, override_headers: dict = None):
        '''

        :param override_headers:  override on each request
        :return: headers:
        '''
        # Clone the template.
        headers = self.extra_headers.copy()

        # Add extra User-Agent if not has
        if not (self.extra_headers.get('user-agent') and self.extra_headers.get('User-Agent')):
            ua_header = self.get_user_agent()
            for k, v in ua_header.items():
                headers[k] = v

        # Override for purpose
        if override_headers:
            for k, v in override_headers.items():
                headers[k] = str(v)  # Must str: Page: 1 , 1 is string

        return headers

    def _validate(self):
        h_ = v_ = ''

        # Remove :         accept-encoding: gzip, deflate, br
        if self.extra_headers.get('accept-encoding'):
            h_ = 'accept-encoding'
            v_ = self.extra_headers.get(h_)

        if self.extra_headers.get('Accept-Encoding'):
            h_ = 'Accept-Encoding'
            v_ = self.extra_headers.get(h_)

        if v_:
            if 'br' in v_:
                # self.log.warn('Contains         [accept-encoding: gzip, deflate, br: => br: Brotli compress]')
                # self._has_br = True

                v_ = [i.strip() for i in v_.split(',')]
                v_.remove('br')
                self.extra_headers[h_] = ', '.join(v_)
