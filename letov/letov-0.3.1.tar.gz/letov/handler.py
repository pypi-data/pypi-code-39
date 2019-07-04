import sys
import logging

from letov.stream import ZstdChunkedWrapper


logger = logging.getLogger(__name__)


class StreamHandler(logging.StreamHandler):
    def filter(self, record):
        return super().filter(record) and not record.name.startswith('letov')

    def handleError(self, record):
        logger.exception('Fatal logging error')
        raise sys.exc_info()[1]


class ZstdChunkedHandler(StreamHandler):
    """
    Handler that compresses all input data with ZSTD and flushes it to
    wrapped stream in chunks less than specified size. Each chunk forms a json
    with metadata and valid base64-encoded ZSTD frame. Each input line is
    guaranteed to make it to the chunk entirely.
    Chunks are delimited with newline.

    :param stream: Wrapped stream
    :param group_name: Name that will be a part of chunk's metadata.
    :param size_limit: Chunk's size limit in bytes.
    :param flush_every: How many time, in seconds, should the stream wait
    before flush, if not enough data were fed to reach size limit. Zero or
    negative values disable this behavior.
    :param compression_params: Params dict to be passed to ZstdCompressor.
    """

    def __init__(
        self, stream, group_name, flush_every, size_limit,
        compression_params=None
    ):
        super().__init__(
            ZstdChunkedWrapper(
                stream, group_name, flush_every, size_limit, compression_params
            )
        )

    def emit(self, record):
        # Basically a StreamHandler.emit, but without flush
        try:
            msg = self.format(record)
            self.stream.write(msg + self.terminator)
        except Exception:
            self.handleError(record)
