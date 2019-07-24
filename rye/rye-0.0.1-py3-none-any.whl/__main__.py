import click
from click import Group
from click.exceptions import Exit
from settingscascade import SettingsManager

from rye.application import Application
from rye.config import get_config


class DefaultGroup(Group):
    def parse_args(self, ctx, args):
        if not args:
            args.insert(0, "run")
        return super(DefaultGroup, self).parse_args(ctx, args)

    def resolve_command(self, ctx, args):
        base = super(DefaultGroup, self)
        cmd_name, cmd, args = base.resolve_command(ctx, args)
        if hasattr(ctx, "arg0"):
            args.insert(0, ctx.arg0)
        return cmd_name, cmd, args


@click.group(cls=DefaultGroup)
@click.pass_context
def cli(ctx):
    ctx.obj = get_config()


@cli.command()
@click.pass_obj
@click.argument("tasks", nargs=-1, default=None)
def run(config: SettingsManager, tasks):
    app = Application(config, tasks=tasks)
    Exit(code=app.run())


@cli.command()
@click.pass_obj
@click.argument("envs", nargs=-1, default=None)
def build_envs(config: SettingsManager, envs):
    app = Application(config)
    Exit(code=app.build_envs(envs))
