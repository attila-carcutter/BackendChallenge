import click

from api.api_server import cli as api_server


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


cli.add_command(api_server)
