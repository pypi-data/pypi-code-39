import base64
import json
from datetime import date, datetime
from typing import Union

import arrow
import boto3
from google.protobuf import message

from mbq import atomiq

from . import utils


def _json_dumps_with_iso_datetimes(data: Union[dict, list, tuple]):
    def _default(obj):
        if isinstance(obj, (datetime, date, arrow.Arrow)):
            return obj.isoformat()
        else:
            raise TypeError("{} is not JSON serializable".format(obj))

    return json.dumps(data, default=_default, sort_keys=True)


def _publish(payload: dict, topic_arn: str, use_atomiq: bool):
    if use_atomiq:
        atomiq.sns_publish(topic_arn=topic_arn, payload=payload)
    else:
        sns = boto3.client("sns")
        sns.publish(
            TargetArn=topic_arn,
            MessageStructure="json",
            Message=json.dumps({"default": _json_dumps_with_iso_datetimes(payload)}),
        )


def _collect_metrics(envelope: utils.Envelope, topic_arn: str, used_atomiq: bool):
    from . import _collector as collector

    collector.increment(
        "publisher.published",
        tags={
            "message_type": envelope.message_type,
            "payload_type": envelope.payload_type.value,
            "topic": utils.get_name_from_topic_arn(topic_arn),
            "used_atomiq": used_atomiq,
        },
    )


def publish_proto(proto: message.Message, topic_arn: str, use_atomiq: bool = True):
    message_type = f"proto.{proto.__module__}.{proto.DESCRIPTOR.name}"
    payload = base64.b64encode(proto.SerializeToString()).decode()
    envelope = utils.Envelope(
        message_type=message_type,
        payload=payload,
        payload_type=utils.PayloadType.PROTO,
        envelope_created_at=arrow.now(),
    )

    _publish(envelope.asdict(), topic_arn, use_atomiq)
    _collect_metrics(envelope, topic_arn, use_atomiq)


def publish_json(
    message_type: str, data: Union[dict, list, tuple], topic_arn: str, use_atomiq: bool = True
):
    envelope = utils.Envelope(
        message_type=message_type,
        payload=data,
        payload_type=utils.PayloadType.JSON,
        envelope_created_at=arrow.now(),
    )

    _publish(envelope.asdict(), topic_arn, use_atomiq)
    _collect_metrics(envelope, topic_arn, use_atomiq)
