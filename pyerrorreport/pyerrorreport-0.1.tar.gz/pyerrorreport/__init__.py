"""
Send error reports and other messages to a central server you control.

Create a Reporter object with your server address and the TCP port the
server is running on (1234 by default) and use it's .send method
to send a dict, made from .send()'s keyword args, to the server.

Launch the server with
$ python -m error_report --hostname HOSTNAME --port PORT --keys KEYS
Default port is 1234.

Server reads a configuration JSON file at ~/.pyerrorreport/config.json
Populate the json file with 'hostname', 'port', and 'keys'.

'keys' is a list of the keys of values the server will read out of the
report dict to place the report in a directory.

I.e. if group_by_keys is ['userid', 'operation'] and the client sends
{userid : "blabla", operation : "foobar", xyzzy : "plugh"}
then the report will be saved in [working directory]/reports/blabla/foobar/...
"""

import json
import re
import socket
import socketserver
import time
from pathlib import Path

__all__ = ["Reporter", "server_address", "server_port", "send", "JSONReportHandler", "start_server"]

class Reporter:
    """Class for sending reports to a certain server. Requires an address,
    and can be provided with an alternate TCP port to connect to."""

    def __init__(self, server_address, server_port = 1234):
        self.server_address = server_address
        self.server_port = server_port

    def send(self, **kwargs):
        """Send a report to the server at the module-level server_address
        with the given keyword arguments. The keyword dict this is passed
        will be saved on the server as a .JSON file.

        If server_addr is omitted, uses the module level server_addr.
        Raises ValueError if that has not been set.

        It's strongly recommended that you use socket.setdefaulttimeout()
        to set a connection timeout; otherwise this will hang forever
        if it can't make a connection.
        """
        tgt = self.server_address, self.server_port
        with socket.create_connection(tgt) as connection:
            connection.sendall( json.dumps(kwargs, separators = (',', ':')).encode() )

#Module level address and port for the module methods
server_address = None
server_port = 1234

class _ModuleLevelReporter(Reporter):

    def __init__(self):
        pass

    @property
    def server_address(self):
        return server_address

    @property
    def server_port(self):
        return server_port

_inst = _ModuleLevelReporter()
send = _inst.send

### Server side ###############################################################
_default_config_path = Path.home() / ".pyerrorreport" / "config.json"
def _load_server_config(config_path = _default_config_path):
    if config_path.exists():
        with open(config_path, "rt") as fp:
            return json.load(fp)

    else:
        return {}

class JSONReportHandler(socketserver.StreamRequestHandler):
    """Handler for the standard library socketserver that takes JSON data over
    TCP and writes it out to disk, organizzed by group_by_keys."""

    def handle(self):
        report = json.load(self.rfile)

        path = Path("reports")
        for thekey in self.server.group_by_keys:
            try:
                component = str( report[thekey] )
                path /= re.sub(r'[/<>"\\|*?:]', " ", component)
            except KeyError:
                path /= "NOT PROVIDED"

        path.mkdir(exist_ok = True, parents = True)

        path /= time.strftime("%d %B %Y %H-%M-%S.json")

        with open(path, "wt") as f:
            json.dump(report, f, sort_keys = True, indent = 4)
        print(f"Report written to {path}")

def start_server(hostname = "localhost", port = 1234, keys = []):
    """Start a server listening for reports and saving them out to disk.
    Does not return."""
    config = _load_server_config()

    if hostname == "localhost": hostname = config.get("hostname", "localhost")
    if port     == 1234       : port     = config.get("port",     1234)
    if keys     == []         : keys     = config.get("keys",     [])

    with socketserver.TCPServer((hostname, port), JSONReportHandler) as server:
        #We use this construction instead of .serve_forever()
        #because serve_forever doesn't respect the timeout
        server.timeout = 0.33
        server.group_by_keys = keys
        while True:
            server.handle_request()
