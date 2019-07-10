from django.apps import AppConfig

from mbq import metrics
from mbq.pubsub.settings import project_settings

from . import decorators


class PubSubConfig(AppConfig):
    name = "mbq.pubsub"
    verbose_name = "PubSub"

    def ready(self):
        from . import publishers, utils

        self.module._collector = metrics.Collector(
            namespace="mbq.pubsub",
            tags={"env": project_settings.ENV.long_name, "service": project_settings.SERVICE},
        )

        self.module.publish_proto = publishers.publish_proto
        self.module.publish_json = publishers.publish_json
        self.module.with_envelope = decorators.with_envelope
        self.module.replay_undeliverable_messages = utils.replay_undeliverable_messages
