def interceptor(payload, monkeypatch):
    def payloader(x, method, *args, **kwargs):
        return payload[method]
    monkeypatch.setattr(
        'auger.api.cloud.rest_api.RestApi.call_ex', payloader)
