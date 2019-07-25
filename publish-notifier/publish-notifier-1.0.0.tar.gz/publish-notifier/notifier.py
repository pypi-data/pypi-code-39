from base import NotifierBase
from compressor import Compressor
from errors import Error, ErrorCodes
from stream_connect.connector import StreamPublisher

REPUBLISH_METHOD = 'KAFKA'

class Notifier(NotifierBase):

    @staticmethod
    def _compress(payload):
        compressor = Compressor(payload)
        return compressor.compress()

    @staticmethod
    def _get_publishing_payload(topic, payload, status, timestamp, offset, partition, **kwargs):
        """Returns the publishing payload"""
        data = dict(
            topic=topic,
            offset=offset,
            partition=partition,
            timestamp=timestamp,
            status=status,
            payload=payload
        )
        data.update(**kwargs)
        return data

    def _publish(self, data):
        """Publishes the data to the republisher"""
        try:
            publisher = StreamPublisher(REPUBLISH_METHOD, self.host, self.topic)
            publisher_response = publisher.publish({
                'payload': data
            })
            if not publisher_response.success:
                self.response.errors.extend(publisher_response.errors)
                raise Error(ErrorCodes.StreamConnectError)
        except Exception as e:
            raise Error(ErrorCodes.StreamConnectError)

    def process(self, topic, payload, status, timestamp, offset=None,
            partition=None, compression=True, **kwargs):
        """
        Generates the re-publishing payload and publishes it to the republisher
        """
        try:
            data = Notifier._get_publishing_payload(
                topic, payload, status, timestamp, offset, partition, **kwargs)
            compressed_data = Notifier._compress(data) if compression else data
            self._publish(compressed_data)
            self.response.success = True
        except Error as e:
            self.response.errors.append(e.get_error())
