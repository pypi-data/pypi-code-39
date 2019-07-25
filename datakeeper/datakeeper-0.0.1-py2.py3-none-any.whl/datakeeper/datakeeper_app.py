#!/usr/bin/python
import logging.config
import argparse
import signal
from os import path
from flask import Flask, Blueprint

from datakeeper.base import testmode
from datakeeper.settings import load, specs
from datakeeper import msg
from datakeeper.utility import relpath, import_fqn
from datakeeper.base import bparser, exhandler
from datakeeper.api import create_api, ServerThread
from datakeeper.writers import component_write

app = Flask('datakeeper.app')
"""flask.Flask: for the overall application.
"""
apis = {}
"""dict: keys are component names; values are the :class:`flask_restplus.Api`
instances for the component.
"""
server = None
"""datakeeper.api.ServerThread: server for the REST API.
"""

logging.config.fileConfig(relpath('datakeeper/templates/logging.conf'))
log = logging.getLogger(__name__)

def examples():
    """Prints examples of using the script to the console using colored output.
    """
    script = "Data Keeper REST API for Local Node"
    explain = ("This scripts starts a REST API on the local machine for each "
               "of the application configuration specifications. See examples "
               "in `docs/configs/*.yml`.")
    contents = [(("Start the local REST API server for two applications."),
                 "app.py records.yml consent.yml",
                 "Each application will run on the same port, but under a "
                 "different URL prefix, as specified in the configuration for the app.")]
    required = ("'app.yaml' file with REST application configuration.")
    output = ("")
    details = ("")
    outputfmt = ("")

    msg.example(script, explain, contents, required, output, outputfmt, details)

script_options = {
    "appspec": {"help": "File containing the root endpoint specifications.",
                "nargs": '+'},
    "--overwrite": {"help": "Recreate generated module files from scratch.",
                "action": "store_true"},
    "--generate": {"help": ("Generate the package code; when not specified, "
                            "only the server will run on existing code."),
                "action": "store_true"}
    }
"""dict: default command-line arguments and their
    :meth:`argparse.ArgumentParser.add_argument` keyword arguments.
"""

def _parser_options():
    """Parses the options and arguments from the command line."""
    pdescr = "Data Keeper REST API"
    parser = argparse.ArgumentParser(parents=[bparser], description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)

    args = exhandler(examples, parser)
    if args is None:
        return

    return args

def _get_subspec(key, d, ref=None, source=None):
    """Retrieves a sub-specification from the `d`

    Args:
        key (str): name of the attribute to retrieve, if it exists.
        d (dict): specification dictionary to check attributes for.
        ref: if specified and not `None`, then a warning will be printed that
            the attribute is being overridden.
        source (str): source of `d` to use in the warning message if generated.

    Returns:
        The reference object `ref` if the key does not exist; this avoids
        overwriting previous specs that were good with `None`.
    """
    if key in d:
        if ref is not None:
            wmsg = "{} specification is overridden by {}"
            log.warning(wmsg.format(key.capitalize(), source))
        #We use the getattr call here so that a :class:`AttrDict` is returned
        #regular key access returns a regular dict.
        return getattr(d, key)
    else:
        return ref

def _stop_server(signal, frame): # pragma: no cover
    """Cleans up the serial communication and logging.
    """
    global server
    msg.warn("SIGINT >> cleaning up API server.", -1)
    server.shutdown()

def run(args):
    """Initializes the REST application with all configured component endpoints.
    """
    if args is None:
        return

    #Read the global application specification recursively and then update
    #the main flask app's parameters.
    global app
    srvspec, packspec, appspec = None, None, None

    for compfile in args["appspec"]:
        aspec = load(compfile)
        srvspec = _get_subspec("server", aspec, ref=srvspec, source=compfile)
        packspec = _get_subspec("package", aspec, packspec, compfile)
        appspec = _get_subspec("app", aspec, appspec, compfile)
        if "components" in aspec:
            for compspec in aspec.components:
                specs[compspec.name] = compspec

    if srvspec is not None:
        app.config.update(srvspec)

    #Now, iterate over the components defined for the application and create
    #a python namespace for each, then configure them on the global flask
    #application object at their registered URL prefixes.
    for compname, compspec in specs.items():
        #Create the API object to connect the component to. It is cached in
        #datakeeper.api and datakeeper.app
        api = create_api(appspec, compspec)
        apis[compspec.name] = api
        if args["generate"]:
            component_write(packspec, compspec, overwrite=args["overwrite"])
        if testmode:
            #Make sure that a second call without overwrite enabled triggers the
            #right logic paths in the code.
            component_write(packspec, compspec, overwrite=False)

        #Import the blueprint object that has been initialized for the component.
        fqn = "{}.{}.blueprint".format(packspec.name, compname)
        mod, obj = import_fqn(fqn)
        app.register_blueprint(obj)

    global server
    app.debug = appspec.get("debug", False) or args["debug"]
    server = ServerThread(app, srvspec.SERVER_NAME)
    signal.signal(signal.SIGINT, _stop_server)

    #Now that the cleanup code is done, we can start the server thread.
    server.start()

if __name__ == '__main__': # pragma: no cover
    run(_parser_options())
