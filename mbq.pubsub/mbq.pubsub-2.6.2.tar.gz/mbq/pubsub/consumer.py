import base64
import json
import logging
import typing

from django.db.utils import InterfaceError

import arrow
import boto3
import rollbar

from . import _collector as collector
from . import constants, exceptions, models, utils


logger = logging.getLogger(__name__)

NOT_PROVIDED = object()


class Consumer:
    def __init__(
        self,
        queue_name: str,
        handlers: dict,
        default_handler: typing.Optional[typing.Callable[[str], None]] = None,
    ) -> None:
        self._queue_name = queue_name
        self._queue_full_name = utils.construct_full_queue_name(queue_name)
        self._handlers = handlers
        self._default_handler = default_handler

    @property
    def queue(self):
        if not hasattr(self, "_queue"):
            sqs = boto3.resource("sqs")
            self._queue = sqs.get_queue_by_name(QueueName=self._queue_full_name)
        return self._queue

    @property
    def dead_letter_queue(self):
        """
        Find the dead letter queue from the primary queue's redrive policy.

        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
        """

        if not hasattr(self, "_dead_letter_queue"):
            try:
                redrive_policy = json.loads(self.queue.attributes["RedrivePolicy"])
                dlq_name = redrive_policy["deadLetterTargetArn"].split(":")[-1]
            except Exception as e:
                raise exceptions.ConsumerException(
                    f"No dead letter queue configured for {self.queue}"
                ) from e

            sqs = boto3.resource("sqs")
            self._dead_letter_queue = sqs.get_queue_by_name(QueueName=dlq_name)
        return self._dead_letter_queue

    def process_queue(self):
        messages = self.queue.receive_messages(
            AttributeNames=["SentTimestamp"], WaitTimeSeconds=5, MaxNumberOfMessages=10
        )

        for message in messages:
            handler = None
            envelope = None

            try:
                envelope = utils.Envelope.from_sqs_message(message)
                message_type = envelope.message_type
            except exceptions.EnvelopeException as e:
                message_type = constants.DEFAULT_MESSAGE_TYPE
                if self._default_handler:
                    handler = self._default_handler
                    payload = message.body
                else:
                    logger.exception(e)

            if not handler and envelope and envelope.payload_type is utils.PayloadType.PROTO:
                proto = utils.get_proto_from_message_type(message_type)
                handler = self._handlers.get(proto)
                if handler:
                    payload = proto()
                    payload.ParseFromString(base64.b64decode(envelope.payload.encode()))

            if not handler and envelope and envelope.payload_type is utils.PayloadType.JSON:
                handler = self._handlers.get(message_type)
                payload = envelope.payload

            tags = {"message_type": message_type, "queue": self._queue_name}
            now = arrow.now()
            if envelope and not envelope.replayed_from_dlq and envelope.envelope_created_at:
                # "from_envelope_creation_ms" tracks the time from the Envelope's creation (during
                # a call to one of pubsub's publisher functions) to the pubsub consumer reading
                # it here
                collector.timing(
                    "consumer.read.from_envelope_creation_ms",
                    utils.timedelta_to_ms(now - envelope.envelope_created_at),
                    tags=tags,
                )
            timestamp = arrow.get(int(message.attributes["SentTimestamp"]) / 1000)
            # "from_message_creation_ms" tracks the time from the creation of the SQS message
            # (via publication from SNS) to the pubsub consumer reading it here
            collector.timing(
                "consumer.read.from_message_creation_ms",
                utils.timedelta_to_ms(now - timestamp),
                tags=tags,
            )
            collector.increment("consumer.read", tags=tags)

            start_process = arrow.now()

            try:
                if handler:
                    if getattr(handler, "_with_envelope", False) is True:
                        handler(payload, envelope)
                    else:
                        handler(payload)
                    result = "succeeded"
                else:
                    result = "skipped"
            except InterfaceError:
                # This exception will raise if the db connetion is unexpectedly closed. We want to
                # raise it to the top of the stack so that the process exits
                raise
            except Exception:
                result = "failed"
                messageId = json.loads(message.body)["MessageId"]
                uuid = rollbar.report_exc_info(
                    payload_data={"context": f"pubsub-message-id#{messageId}"}
                )  # is None on local container test
                url = f"https://rollbar.com/item/uuid/?uuid={uuid}"
                logger.exception(
                    f"An error occurred while processing the "
                    f"message. MessageId: {messageId} Rollbar URL: {url}"
                )
            else:
                message.delete()

            tags = {"result": result, "message_type": message_type, "queue": self._queue_name}
            collector.increment("consumer.processed", tags=tags)
            # "process_time_ms" tracks the time from the message handler call to the success or
            # failure of the handler here
            collector.timing(
                "consumer.processed.process_time_ms",
                utils.timedelta_to_ms(arrow.now() - start_process),
                tags=tags,
            )

    def process_dead_letter_queue(self):
        messages = self.dead_letter_queue.receive_messages(
            AttributeNames=["SentTimestamp"], WaitTimeSeconds=0, MaxNumberOfMessages=10
        )

        for message in messages:
            try:
                body = json.loads(message.body)
                data = json.loads(body["Message"])
                message_type = data["message_type"]
            except Exception as e:
                if self._default_handler:
                    message_type = constants.DEFAULT_MESSAGE_TYPE
                else:
                    raise e

            tags = {"queue": self._queue_name, "message_type": message_type}
            timestamp = arrow.get(int(message.attributes["SentTimestamp"]) / 1000)
            # "from_message_creation_ms" tracks the time from the creation of the SQS DLQ message
            # (after 3 failed delivery attempts on the main queue) to the pubsub DLQ consumer
            # reading it here
            collector.timing(
                "dlq_consumer.read.from_message_creation_ms",
                utils.timedelta_to_ms(arrow.now() - timestamp),
                tags=tags,
            )
            collector.increment("dlq_consumer.read", tags=tags)

            models.UndeliverableMessage.objects.create(
                message_type=message_type,
                message_timestamp=arrow.get(body.get("Timestamp")).datetime,
                payload=message.body,
                queue=self._queue_name,
                topic_arn=body.get("TopicArn"),
            )
            message.delete()

            collector.increment(
                "dlq_consumer.processed",
                tags={"message_type": message_type, "queue": self._queue_name},
            )

    def replay_dead_letter_queue(self, max_messages: int):
        if max_messages < 1:
            raise exceptions.ConsumerException("max_messages must be greater than 0")

        logger.info(
            f"Replaying at most {max_messages} messages "
            f"from {self.dead_letter_queue} to {self.queue}"
        )

        messages_processed = 0
        while True:
            messages = self.dead_letter_queue.receive_messages(
                WaitTimeSeconds=20, MaxNumberOfMessages=10
            )

            for message in messages:
                self.queue.send_message(MessageBody=message.body)
                message.delete()
                messages_processed += 1

                if messages_processed >= max_messages:
                    return
