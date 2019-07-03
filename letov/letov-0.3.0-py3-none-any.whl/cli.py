import atexit
import sys

from functools import partial

import click

from letov.stream import ZstdChunkedWrapper


@click.command()
@click.option('--name', required=True, help='Log stream name')
@click.option(
    '--size-limit', default=250000, type=int,
    help='Chunk\'s size limit in bytes'
)
@click.option(
    '--flush-every', default=60, type=int,
    help=(
        'How many time, in seconds, should the stream wait before flush, '
        'if not enough data were fed to reach size limit. '
        'Zero or negative values disable this behavior.'
    )
)
def entrypoint(name, size_limit, flush_every):
    stream = ZstdChunkedWrapper(sys.stdout, name, flush_every, size_limit)
    atexit.register(stream.flush)

    for data in iter(partial(sys.stdin.read, 8192), ''):
        stream.write(data)
