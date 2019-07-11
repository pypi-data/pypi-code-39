import signal
import subprocess
import sys

import click

from letov.stream import ZstdChunkedWrapper


@click.group()
@click.option('--name', required=True, help='Log stream name')
@click.option(
    '--hard-limit', default=255000, type=int,
    help='Size limit in bytes that must not be exceeded.',
)
@click.option(
    '--soft-limit', default=220000, type=int,
    help='Size limit in bytes that stream heuristics will work against.'
)
@click.option(
    '--flush-every', default=60, type=int,
    help=(
        'How many time, in seconds, should the stream wait before flush, '
        'if not enough data were fed to reach size limit. '
        'Zero or negative values disable this behavior.'
    )
)
@click.pass_context
def cli(context, name, hard_limit, soft_limit, flush_every):
    context.ensure_object(dict)
    context.obj.update({
        'flush_every': flush_every,
        'hard_limit': hard_limit,
        'name': name,
        'soft_limit': soft_limit,
    })


@cli.command(context_settings={'ignore_unknown_options': True})
@click.argument('exec', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def run(context, exec):
    def terminate_child(*args, **kwargs):
        # will break readline loop and letov will exit
        proc.terminate()
        proc.wait()

    stream = ZstdChunkedWrapper(
        sys.stdout,
        group_name=context.obj['name'],
        soft_limit=context.obj['soft_limit'],
        hard_limit=context.obj['hard_limit'],
        flush_every=context.obj['flush_every'],
    )

    proc = subprocess.Popen(
        exec,
        universal_newlines=True,
        stdout=subprocess.PIPE,
    )
    signal.signal(signal.SIGINT, terminate_child)
    signal.signal(signal.SIGTERM, terminate_child)

    try:
        for data in iter(proc.stdout.readline, ''):
            stream.write(data)

        stream.flush()
    finally:
        terminate_child()
