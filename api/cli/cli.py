import click

from api.create_app import create_app_from_env


@click.group(name="api-server")
def main():
    pass


# noinspection HttpUrlsUsage
@main.command(name="vehicle-features", help="Generate comparison images.")
@click.option(
    "--host",
    "host",
    help="The hostname to listen on.",
    default="127.0.0.1",
    type=str,
)
@click.option(
    "--port",
    "port",
    help="The port of the webserver.",
    default=8080,
    type=int,
)
def vehicle_features(host: str, port: int):
    """
    Serves an API with `Flask`.
    http://<host>:<port>/backend/
    """
    app = create_app_from_env()
    app.run(host=host, port=port, debug=True)


@click.group()
@click.pass_context
def cli(ctx):  # pragma: no cover
    ctx.ensure_object(dict)


cli.add_command(main)
