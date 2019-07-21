import logging

import click

from fxq.ae.agent.constants import LOGGING_FORMAT
from fxq.ae.agent.fxq_ae_agent_app import app


@click.command()
@click.option('--debug', is_flag=True, help="Enable debug Logging for the application")
def main(debug: bool):
    logging.basicConfig(format=LOGGING_FORMAT, level=(logging.DEBUG if debug else logging.INFO))
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
