"""Class for centralizing Pub/sub operations"""
import logging

from google.cloud import pubsub_v1

__all__ = ("Pubsub",)


_LOG_PREFIX_ = "[PUBSUB]%s"


class Pubsub(object):
    """
    Class for abstracting the access of the Pubsub
    """

    def __init__(self):
        """Constructor"""
        self.client = pubsub_v1.PublisherClient()

    def publish_message(self, topic: str, message: str) -> None:
        """
        Publish message into a Pubsub topic
        """

        self.validate_topic_name(topic)

        logging.info(
            _LOG_PREFIX_,
            f"[PUBLISH_MESSAGE] Will publish the message: {message}",
        )
        if message:
            self.client.publish(topic, message.encode("utf-8"))
            logging.info(
                _LOG_PREFIX_,
                f"[PUBLISH_MESSAGE] Message published in topic {topic}",
            )

    @staticmethod
    def validate_topic_name(topic):
        """
        Validate the topic is valid and it represents the full path
        """

        # The topic name should follow the expected pattern for a full-path
        # topic name
        # Important: this was before a regex but due to lint complains it
        # was refactored to a simpler verification

        split = topic.split("/")
        valid = (
            len(split) == 4
            and all(split)
            and split[0] == "projects"
            and split[2] == "topics"
        )

        if not valid:
            raise ValueError(
                "Invalid Pub/sub topic name. "
                "The topic name should be in the format: "
                "projects/[PROJECT]/topics/[TOPIC NAME]"
            )
