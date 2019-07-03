import json
import time

from base64 import b64encode
from io import BytesIO
from math import inf
from typing import Iterator, List

import zstd


class _LineBuffer:
    def __init__(self):
        self.buffer = ''

    def write(self, data: str) -> List[str]:
        if not data:
            return []

        self.buffer += data
        lines = self.buffer.splitlines(keepends=True)
        if lines[-1].endswith('\n'):
            self.buffer = ''
        else:
            self.buffer = lines.pop(-1)

        return lines

    def flush(self) -> str:
        data, self.buffer = self.buffer, ''
        return data


class ZstdChunkedWrapper:
    """
    Stream wrapper that compresses all input data with ZSTD and flushes it to
    wrapped stream in chunks less than specified size. Each chunk forms a json
    with metadata and valid base64-encoded ZSTD frame. Each input line is
    guaranteed to make it to the chunk entirely. This class is not intended
    to use with small size limits (orders of size of compressed log message).
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
        self.stream = stream
        self.group_name = group_name
        self.flush_every = flush_every if flush_every > 0 else inf
        self.size_limit = size_limit
        self.last_flush = time.monotonic()
        self.compression_params = compression_params or {}

        self._output = BytesIO()  # buffer with compressed data
        self._line_buffer = _LineBuffer()
        # considering base64 (hence multiplying by 0.75)
        # 14 is zstd frame header maximum size
        self._raw_size_limit = (
            size_limit * 3 // 4
            - 14
            - self._get_formatting_overhead()
        )
        # compression
        self._compressor = zstd.ZstdCompressor(**self.compression_params)
        self._decompressor = zstd.ZstdDecompressor(**self.compression_params)
        self._zstd_stream = self._compressor.stream_writer(self._output)
        self._frame_progression = self._compressor.frame_progression()
        self._consumed = 0
        self._produced = 0

        self._chunk_first_write_ts = None

    @property
    def avg_compression_ratio(self):
        try:
            return self._consumed / self._produced
        except ZeroDivisionError:
            # first block ¯\_(ツ)_/¯
            return 2

    def write(self, data: str):
        for line in self._line_buffer.write(data):
            self._write(line)

    def flush(self):
        residue = self._line_buffer.flush()
        if residue:
            self._write(residue)
        self._flush()

    def close(self):
        self._zstd_stream.close()

    def _write(self, line: str):
        if not self._chunk_first_write_ts:
            self._chunk_first_write_ts = time.time()

        if self._write_will_overflow(line):
            self._flush()

        if self._zstd_stream.write(line.encode('utf-8')):
            # internal buffer was flushed
            self._update_stats()

        if time.monotonic() - self.last_flush >= self.flush_every:
            self._flush()

    def _flush(self):
        if self._chunk_first_write_ts:  # its not empty
            self._zstd_stream.flush(zstd.FLUSH_FRAME)

            raw_chunk = self._output.getvalue()
            for chunk in self._split_chunk(raw_chunk):
                self.stream.write(self._format_chunk(chunk))
                self.stream.flush()

            self._output.seek(0)
            self._output.truncate()
            self._chunk_first_write_ts = None

        self.last_flush = time.monotonic()

    def _update_stats(self):
        _, prev_consumed, prev_produced = self._frame_progression
        self._frame_progression = _, consumed, produced = (
            self._compressor.frame_progression()
        )
        self._consumed += (consumed - prev_consumed)
        self._produced += (produced - prev_produced)

    def _format_chunk(self, chunk: bytes) -> str:
        return json.dumps({
            'data': b64encode(chunk).decode('ascii'),
            'end_ts': time.time(),
            'name': self.group_name,
            'start_ts': self._chunk_first_write_ts,
        }) + '\n'

    def _get_formatting_overhead(self):
        self._chunk_first_write_ts = time.time()
        overhead = len(self._format_chunk(b''))
        self._chunk_first_write_ts = None
        return overhead

    def _write_will_overflow(self, data: str) -> bool:
        ingested, consumed, produced = self._compressor.frame_progression()

        zstd_buffer_size = ingested - consumed
        estimated_compressed_size = (
            produced
            + (zstd_buffer_size + len(data)) / self.avg_compression_ratio
        )

        return self._raw_size_limit <= estimated_compressed_size

    def _split_chunk(self, chunk: bytes) -> Iterator[bytes]:
        if len(chunk) <= self._raw_size_limit:
            yield chunk
            return

        # recompress biggest lines separately until it fits size limit
        data = self._decompressor.stream_reader(BytesIO(chunk)).readall()

        lines = data.splitlines(keepends=True)
        while len(chunk) >= self._raw_size_limit:
            # avoid searching for a line through list
            biggest_line_index = max(
                range(len(lines)),
                key=lambda index: len(lines.__getitem__(index))
            )
            yield self._compressor.compress(lines.pop(biggest_line_index))
            chunk = self._compressor.compress(b''.join(lines))

        yield chunk
