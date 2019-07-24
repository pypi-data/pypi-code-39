# -*- coding: utf-8 -*-
import click

from spell.api.models import RunRequest
from spell.cli.exceptions import (
    api_client_exception_handler,
)
from spell.cli.api_constants import (
    get_machine_types,
    get_machine_type_default,
)
from spell.cli.commands.logs import logs
from spell.cli.log import logger
from spell.cli.utils import LazyChoice, with_emoji, ellipses


@click.command(name="tensorboard",
               short_help="Resume tensorboard",
               hidden=True)
@click.option("-t", "--machine-type",
              type=LazyChoice(get_machine_types), default=get_machine_type_default,
              help="Machine type to run on")
@click.argument("run_id", type=int)
@click.pass_context
def tensorboard(ctx, machine_type, run_id):
    """
    The tensorboard command is used to resume tensorboard after run stops.
    """
    logger.info("starting tensorboard command")
    run_req = create_tensorboard_run_request(
        ctx=ctx,
        machine_type=machine_type,
        run_type="user",
        framework="tensorflow",
        tensorboard_enabled=True,
        tensorboard_parent_run_id=run_id,
    )

    # execute the run
    client = ctx.obj["client"]
    logger.info("sending run request to api")
    with api_client_exception_handler():
        run = client.run(run_req)

    utf8 = ctx.obj["utf8"]

    click.echo(with_emoji(u"💫", "Resuming TensorBoard for run#{}".format(run.tensorboard_parent_run_id), utf8)
               + ellipses(utf8))

    click.echo(with_emoji(u"✨", "Stop viewing logs with ^C", utf8))
    ctx.invoke(logs, run_id=str(run.id), follow=True, run_warning=True)


def create_tensorboard_run_request(ctx, machine_type, run_type, framework, tensorboard_enabled=False,
                                   tensorboard_dir=None, tensorboard_parent_run_id=None, **kwargs):

    # Tensorboard Directory set to /tensorboard
    if tensorboard_dir is None:
        tensorboard_dir = "/tensorboard"
    return RunRequest(
        machine_type=machine_type,
        run_type=run_type,
        framework=framework,
        tensorboard_enabled=tensorboard_enabled,
        tensorboard_directory=tensorboard_dir,
        tensorboard_parent_run_id=tensorboard_parent_run_id,
    )
