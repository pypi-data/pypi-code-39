from localbitcoins.client import Client


class Wrapper:
    def __init__(
        self, client: Client, path: str = "/api/", method: str = None
    ):
        self.client = client
        self._path = path
        self._method = method

    def __getattr__(self, item):
        if not self._method:  # POST / GET
            return Wrapper(self.client, self._path, item)

        # Some endpoints have `-` char in names: `client.post.wallet-send`
        #        (client.post.wallet - send); `send` is not defined ^-- minus
        exceptions = [
            "ad_get",
            "ad_create",
            "ad_equation",
            "ad_delete",
            "wallet_balance",
            "wallet_send",
            "wallet_send-pin",
            "wallet_addr",
        ]
        if item in exceptions:
            item = item.replace("_", "-")
        path = self._path + item + "/"
        wrapper = Wrapper(self.client, path, self._request_method)

        return wrapper

    def __call__(self, item_id, **kwargs):
        return self.client.request(self._method, self._path, kwargs)
