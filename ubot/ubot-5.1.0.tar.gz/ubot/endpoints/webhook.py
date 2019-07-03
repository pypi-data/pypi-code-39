from ._base import Endpoint

update_types = {
    'message', 'edited_message', 'channel_post', 'edited_channel_post', 'inline_query', 'chosen_inline_result',
    'callback_query', 'shipping_query', 'pre_checkout_query'
}


class SetWebhook(Endpoint):
    def __init__(self, url):
        super().__init__()
        self.args['url'] = url

    def certificate(self, certificate):
        self.args['certificate'] = certificate
        return self

    def max_connections(self, max_connections):
        self.args['max_connections'] = max_connections
        return self

    def allowed_updates(self, allowed_updates):
        for update_type in allowed_updates:
            assert update_type in update_types

        self.args['allowed_updates'] = allowed_updates
        return self


class DeleteWebhook(Endpoint):
    pass


class GetWebhookInfo(Endpoint):
    pass
