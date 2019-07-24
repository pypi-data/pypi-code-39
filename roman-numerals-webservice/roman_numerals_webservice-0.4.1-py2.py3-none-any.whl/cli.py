# -*- coding: utf-8 -*-

"""Console script for roman_numerals_webservice."""
import sys
import click
import cherrypy

from .roman_numerals_webservice import RomanNumeralsWebservice

msg = r"""
================================================================================
  ____                              _   _                                _     
 |  _ \  ___  _ __ ___   __ _ _ __ | \ | |_   _ _ __ ___   ___ _ __ __ _| |___ 
 | |_) |/ _ \| '_ ` _ \ / _` | '_ \|  \| | | | | '_ ` _ \ / _ \ '__/ _` | / __|
 |  _ <| (_) | | | | | | (_| | | | | |\  | |_| | | | | | |  __/ | | (_| | \__ \
 |_| \_\\___/|_| |_| |_|\__,_|_| |_|_| \_|\__,_|_| |_| |_|\___|_|  \__,_|_|___/
 __        __    _                          _           
 \ \      / /___| |__  ___  ___ _ ____   __(_) ___  ___ 
  \ \ /\ / // _ \ '_ \/ __|/ _ \ '__\ \ / /| |/ __|/ _ \
   \ V  V /|  __/ |_) \__ \  __/ |   \ V / | | (__|  __/
    \_/\_/  \___|_.__/|___/\___|_|    \_/  |_|\___|\___|       
================================================================================                   
"""


@click.command()
@click.option("--port", default=8080, help="socket port")
@click.option("--host", default="0.0.0.0", help="socket host")
@click.option(
    "--dry_run",
    default=False,
    type=bool,
    help="""if True, server is started with and closed immediately afterwards.\
This is only useful for testing purposes""",
)
def main(port, host, dry_run):
    """Console script for roman_numerals_webservice."""
    click.echo(msg)
    config = {
        "server.socket_port": port,
        "server.socket_host": host,
        "environment": "production",
    }
    if not dry_run:  # pragma: no cover
        cherrypy.config.update(config)
        cherrypy.quickstart(RomanNumeralsWebservice())
    else:
        cherrypy.engine.signals.subscribe()
        cherrypy.engine.start()
        cherrypy.engine.wait(cherrypy.engine.states.STARTED)
        cherrypy.tree.mount(RomanNumeralsWebservice())
        cherrypy.engine.exit()
        cherrypy.engine.block()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
