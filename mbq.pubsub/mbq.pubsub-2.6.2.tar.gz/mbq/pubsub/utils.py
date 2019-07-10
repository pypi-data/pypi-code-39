import datetime
import enum
import functools
import importlib
import json
import re
import time
import typing

from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.models import QuerySet

import arrow
import boto3

from .exceptions import EnvelopeException
from .models import UndeliverableMessage
from .settings import project_settings


_DB_READY: typing.Dict[str, bool] = {}
PROTO_MESSAGE_PREFIX = r"^proto\."
PROTO_CLASS_PATTERN = r"\.([^.]*)$"


class PayloadType(enum.Enum):
    PROTO = "proto"
    JSON = "json"


class Envelope:
    def __init__(
        self,
        message_type: str,
        payload: typing.Union[str, dict, list, tuple],
        payload_type: PayloadType,
        envelope_created_at: typing.Optional[arrow.Arrow] = None,
        replayed_from_dlq: bool = False,
    ) -> None:
        self.message_type = message_type
        self.payload = payload
        self.payload_type = payload_type
        self.envelope_created_at = envelope_created_at
        self.replayed_from_dlq = replayed_from_dlq

    def __eq__(self, other):
        return (
            self.message_type == other.message_type
            and self.payload == other.payload
            and self.payload_type is other.payload_type
            and self.envelope_created_at == other.envelope_created_at
            and self.replayed_from_dlq == other.replayed_from_dlq
        )

    def asdict(self):
        envelope_created_at = None
        if self.envelope_created_at:
            envelope_created_at = self.envelope_created_at.format("YYYY-MM-DD HH:mm:ss.SSSSSSZZ")

        return {
            "message_type": self.message_type,
            "payload": self.payload,
            "payload_type": self.payload_type.value,
            "envelope_created_at": envelope_created_at,
            "replayed_from_dlq": self.replayed_from_dlq,
        }

    @classmethod
    def _create_envelope(cls, body):
        obj = json.loads(body["Message"])

        envelope_created_at_str = obj.get("envelope_created_at")
        envelope_created_at = None
        if envelope_created_at_str:
            envelope_created_at = arrow.get(envelope_created_at_str)

        return cls(
            # `message_type` and `payload` are the two required attributes of the envelope;
            # if they are not present in the message body, raise
            obj["message_type"],
            obj["payload"],
            # All properties following this comment are optional in the message body to
            # maintain backwards compatibility
            PayloadType(obj.get("payload_type", "json")),
            envelope_created_at,
            obj.get("replayed_from_dlq", False),
        )

    @classmethod
    def from_undeliverable_message(cls, message: UndeliverableMessage):
        try:
            body = json.loads(message.payload)
            return cls._create_envelope(body)
        except Exception as e:
            raise EnvelopeException from e

    @classmethod
    def from_sqs_message(cls, message):
        try:
            body = json.loads(message.body)
            return cls._create_envelope(body)
        except Exception as e:
            raise EnvelopeException from e


def construct_full_queue_name(queue_name):
    return f"mbq-{project_settings.SERVICE}-{queue_name}-{project_settings.ENV.short_name}"


def debounce(seconds=None, minutes=None, hours=None):
    def wrapper(func):
        func.seconds_between_runs = 0
        func.last_run = time.time()

        if seconds:
            func.seconds_between_runs += seconds
        if minutes:
            func.seconds_between_runs += minutes * 60
        if hours:
            func.seconds_between_runs += hours * 60 * 60

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if func.last_run + func.seconds_between_runs < time.time():
                func(*args, **kwargs)
                func.last_run = time.time()

        return wrapped_func

    return wrapper


def is_db_ready(database="default"):
    """Determine whether the migrations for pubsub are up to date. Can
    be used to defer hitting the database until everything is ready.

    Implementation is inspired by the `./manage.py migrate --plan` command:

       https://github.com/django/django/blob/master/django/core/management/commands/migrate.py#L140-L150
    """
    global _DB_READY

    if not _DB_READY.get(database, False):
        executor = MigrationExecutor(connections[database])
        # find the pubsub migrations
        pubsub_migrations = [
            node for node in executor.loader.graph.leaf_nodes() if node[0] == "pubsub"
        ]
        # build a plan to run all the migrations
        plan = executor.migration_plan(pubsub_migrations)
        # if there's no plan then we're fully up to date
        _DB_READY[database] = not bool(plan)

    return _DB_READY[database]


def get_proto_from_message_type(message_type: str):
    full_path = re.sub(PROTO_MESSAGE_PREFIX, "", message_type)
    proto_class_match = re.search(PROTO_CLASS_PATTERN, full_path)
    if proto_class_match is None:
        return None
    proto_class = proto_class_match.groups()[0]
    proto_path = re.sub(PROTO_CLASS_PATTERN, "", full_path)

    try:
        module = importlib.import_module(proto_path)
    except ModuleNotFoundError:
        return None

    return getattr(module, proto_class, None)


def get_name_from_topic_arn(arn):
    if arn:
        return arn.split(":")[-1]


def timedelta_to_ms(d: datetime.timedelta) -> int:
    return round(d.total_seconds() * 1000)


def replay_undeliverable_messages(queryset: QuerySet):
    sqs = boto3.client("sqs")
    queue_urls: typing.Dict[str, str] = {}

    for message in queryset:
        if message.queue not in queue_urls:
            url = sqs.get_queue_url(QueueName=construct_full_queue_name(message.queue))
            queue_urls[message.queue] = url["QueueUrl"]

        try:
            envelope = Envelope.from_undeliverable_message(message)
            envelope.replayed_from_dlq = True
            deserialized_body = json.loads(message.payload)
            deserialized_body["Message"] = json.dumps(envelope.asdict())
            message_body = json.dumps(deserialized_body)
        except EnvelopeException:
            message_body = message.payload

        sqs.send_message(QueueUrl=queue_urls[message.queue], MessageBody=message_body)
        message.delete()
