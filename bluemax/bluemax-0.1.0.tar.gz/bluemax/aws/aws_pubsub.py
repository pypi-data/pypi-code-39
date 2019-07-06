# pylint: disable=C0103
"""
    Classes that wrap functions to publish to sns or consume sqs
"""
import asyncio
import inspect
import functools
import logging
import aiobotocore
from bluemax.web.json_utils import dumps, loads
from bluemax.settings import get_settings

LOGGER = logging.getLogger(__name__)


class AwsCache:
    """
        A cache for AWS clients and Sessions
    """

    clients = {}
    session = None
    region = None
    account_id = None

    @classmethod
    def client(cls, kind):
        """ Returns a cached client if available """
        client = cls.clients.get(kind)
        if client is None:
            if cls.session is None:
                loop = asyncio.get_event_loop()
                cls.session = aiobotocore.get_session(loop=loop)
            endpoint_urls = get_settings("endpoints", {})
            client = cls.session.create_client(
                kind, endpoint_url=endpoint_urls.get(kind)
            )
            cls.clients[kind] = client
        return client

    @classmethod
    async def get_region_account_id(cls):
        """ returns the region and account of current credentials """
        if cls.region is None or cls.account_id is None:
            if get_settings("endpoints"):
                return "us-east-1", "123456789012"
            client = cls.client("sts")
            cls.region = client.meta.region_name
            response = await client.get_caller_identity()
            cls.account_id = response["Account"]
        return cls.region, cls.account_id


def publish(topic_name, message):
    """ publish message to topic async """

    async def func(message):
        """ async callback to do the publish """
        message = dumps(message)
        stage = get_settings("STAGE")
        topic_arn = f"{topic_name}-{stage}"
        topic_arn = await aws_publish.get_topic_arn(topic_arn)
        AwsCache.client("sns").publish(TopicArn=topic_arn, Message=message)

    return asyncio.ensure_future(func(message))


class aws_publish:
    """
        decorator to publish to aws topic

        usage:
        @aws_publish
        def foo():
            # will publish 'foo' to sns:foo
            return 'foo'

        @aws_publish(topic_name='bar')
        def foo():
            # will publish 'foo' to sns:bar
            return 'foo'
    """

    TOPICS = []

    def __init__(self, method=None, topic_name=None):
        LOGGER.debug("__init__(%r, %r)", method, topic_name)
        if method and hasattr(method, "__call__"):
            self.method = method
        else:
            self.method = None
        self.topic_name = topic_name
        self.topic_arn = None

    def __get__(self, obj, type_=None):
        return functools.partial(self, obj)

    @classmethod
    async def get_topic_arn(cls, topic):
        """
            Compose an arn from session data
        """
        region, account_id = await AwsCache.get_region_account_id()
        topic_arn = f"arn:aws:sns:{region}:{account_id}:{topic}"
        return topic_arn

    async def _publish_(self, *args, **kwargs):
        if inspect.iscoroutinefunction(self.method):
            document = await self.method(*args, **kwargs)
        else:
            document = self.method(*args, **kwargs)
        LOGGER.debug("published %s -> %r", self.topic_name, document)
        if self.topic_arn is None:
            stage = get_settings("STAGE")
            topic_arn = f"{self.topic_name}-{stage}"
            self.topic_arn = await self.get_topic_arn(topic_arn)
        message = dumps(document)
        LOGGER.info("publishing: %s -> %r", self.topic_arn, message)
        response = await AwsCache.client("sns").publish(
            TopicArn=self.topic_arn, Message=message
        )
        print(response)

    def __call__(self, *args, **kwargs):
        LOGGER.debug("__call__(%r, %r) %r", args, kwargs, self.method)
        if self.method is None:
            self.method = args[0]
            return self
        if self.topic_name is None:
            self.topic_name = self.method.__name__
        asyncio.ensure_future(self._publish_(*args, **kwargs))
        return None


class aws_subscribe:
    """
        decorator subscribe to aws queue

        usage:
        @aws_subscribe
        def foo(message):
            # will subscribe to sqs:foo
            print(message)

        @aws_subscribe(queue_name='bar')
        def foo(message):
            # will subscribe to sqs:bar
            print(message)
    """

    QUEUES = []

    def __init__(self, method=None, queue_name=None):
        LOGGER.debug("__init__(%r, %r)", method, queue_name)
        if method and hasattr(method, "__call__"):
            self.method = method
        else:
            self.method = None
        self.queue_name = queue_name

    def __get__(self, obj, type_=None):
        return functools.partial(self, obj)

    async def get_queue_url(self, queue: str):
        """
            Returns the queue_url for queue_name
        """
        endpoint_urls = get_settings("endpoints", {})
        if endpoint_urls.get("sqs"):
            queue_url = f"{endpoint_urls['sqs']}/queue/{queue}"
        else:
            client = AwsCache.client("sts")
            region = client.meta.region_name
            response = await client.get_caller_identity()
            account_id = response["Account"]
            queue_url = f"https://{region}.queue.amazonaws.com/{account_id}/{queue}"
        return queue_url

    async def _subscribe_(self):
        stage = get_settings("STAGE")
        sqs_client = AwsCache.client("sqs")
        queue_url = await self.get_queue_url(f"{self.queue_name}-{stage}")
        LOGGER.info("subscribed to: %s", queue_url)
        while True:
            response = await sqs_client.receive_message(QueueUrl=queue_url)
            if "Messages" in response:
                for msg in response["Messages"]:
                    LOGGER.info("Got msg %r", msg["Body"])
                    message = loads(msg["Body"])
                    document = loads(message["Message"])
                    if inspect.iscoroutinefunction(self.method):
                        asyncio.ensure_future(self.method(document))
                    else:
                        self.method(document)
                    # Need to remove msg from queue or else it'll reappear
                    await sqs_client.delete_message(
                        QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"]
                    )
            else:
                LOGGER.debug("No messages in queue")

    def __call__(self, *args, **kwargs):
        LOGGER.debug("__call__(%r, %r) %r", args, kwargs, self.method)
        if self.method is None:
            self.method = args[0]
            return self
        if self.queue_name is None:
            self.queue_name = self.method.__name__
        asyncio.ensure_future(self._subscribe_(*args, **kwargs))
        return "subscribed"
