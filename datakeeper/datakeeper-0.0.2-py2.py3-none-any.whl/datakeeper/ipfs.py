"""
.. note:: Before calling any of the functions in this module, it must first
    be configured using :func:`configure`.

This module provides interaction with the IPFS cluster of a datakeeper. Note that in
order to implement custom security on requests (aka `didauth`) as well as to
supporting adding of files that are accessible on the local node's file system
we implement a second REST API for typical cluster methods. This provides:

1. Total control over authentication of requests.
2. Lock-down of basic cluster API so that it isn't even reachable publicly.
3. Referencing files on the local machine for adding to IPFS (for example, from
   attached USB devices) without the overhead of using a web-browser to send
   each one to the REST API as part of a HTTP request.

However, this comes with an obvious downside: when files *are* added via a
multipart-encoded HTTP request to *this* API, we must prepare a second HTTP
request to the API hosted in IPFS cluster. This is somewhat wasteful, so we
try to mitigate the problem by pulling the byte stream from the request to this
API and sending it directly, as bytes, into the next request to IPFS cluster.
Thus, our only overhead is in constructing the packet with headers, etc.

Given the importance of the features described above, the overhead seems worth
it for now. This could be optimized later by building support for `didauth` via
a decentralized ledger into the IPFS cluster code so that the API inherently
supports it. Not likely to happen in the short term...

"""
from os import path
from flask import send_file, render_template, stream_with_context, Response
import ipfscluster
import ipfshttpclient

basedirs = {}
"""dict: base directories that files and folders are browsed from; see the
example config file and explanation in `docs/config/cluster.yml`.
"""
cluster = None
"""ipfscluster.Client: HTTP client for interacting with the IPFS cluster API.
"""
agent = None
"""ipfshttpclient.Client: HTTP client to interact with the IPFS agent for
file getting and removal from IPFS.
"""
def configure(**settings):
    """Configures the local IPFS cluster on this node.

    Args:
        settings (dict): key-value pairs defining the basic storage directories,
            agent and cluster ports, etc.
    """
    global basedirs, cluster, agent
    #First, set the basic parameters that are just strings; then construct
    #the complex objects.
    basedirs.update({k: path.abspath(path.expanduser(v))
                     for k, v in settings["basedirs"]})
    cluster = ipfscluster.connect(**settings.get("cluster", {}))
    agent = ipfshttpclient.connect(**settings.get("agent", {}))

def dirlist(reqpath=None, **kwargs):
    """Lists contents of `reqpath` if it is a directory; otherwise, serves
    the contents of the file.

    Args:
        reqpath (str): relative path to the file/directory to return.
    """
    assert reqpath is not None

    target = path.join(BASE_DIR, reqpath)
    if not path.exists(target):
        return abort(404)

    if path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    contents = os.listdir(abs_path)
    files = [f for f in contents if path.isfile(path.join(abs_path, f))]
    folders = [f for f in contents if path.isdir(path.join(abs_path, f))]
    return render_template('templates/browser.html', files=files, folders=folders)

def add(reqpath=None, _request=None, **kwargs):
    """Adds the specified file to IPFS. If the file is available from the node's
    local storage, it is added from there; otherwise, it is added from the octet
    stream in the request.

    Args:
        reqpath (str): for local files, the path to the local file on the
            server; if empty or `None`, then the files are retrieved from the
            request body.
        _request: the :class:`flask.Request` to process; used to add files sent
            in the request body.
    """
    response = []
    if reqpath is not None:
        #We are adding a local file; peel off the base directory.
        parts = reqpath.split('/')
        base = parts[0]
        target = path.join(basedirs[base], '/'.join(parts[1:]))
        response.append(cluster.add_files(target))
    elif _request.files is not None:
        #The files are part of the request object; we want to pass them through
        #so that we don't decode and then encode wastefully.
        for formid, file in _request.files:
            response.append(cluster.add_bytes(file.stream))

    return response

def get(reqpath=None, **kwargs):
    """Returns the specified file from the IPFS cluster.

    Args:
        reqpath (str): the IPFS address of the file/folder to return from the
            IPFS cluster.
    """
    assert reqpath is not None
    #Get statistics on the file size so that we can send that in the response
    #headers; that allows the browser to know download %, for example.
    stats = agent.object.stat(reqpath)
    size = stats["CumulativeSize"]
    headers = [
        ('Content-Length', str(size)),
        ('Content-Disposition', 'attachment; filename="/ipfs/%s"' % reqpath),
    ]
    return Response(agent.object.data(reqpath),
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)

def rm(reqpath=None, **kwargs):
    """Removes the specified file from the local node. Note that IPFS is the
    *permanent* web, so things never get deleted from IPFS itself. However, you
    can choose to not pin things anymore so that they are deleted locally. If
    nobody is pinning something, it is essentially deleted since a lookup will
    not return any peers that can actually serve the content.

    .. note:: This function is equivalent to calling :func:`unpin` on the cluster.

    Args:
        reqpath (str): the IPFS address of the file/folder to remove from the
            IPFS cluster.
    """
    return unpin(reqpath)

def pin(reqpath=None, **kwargs):
    """Pins the specified file to the local node. This essentially creates a
    cached copy of the local file.

    Args:
        reqpath (str): the IPFS address of the file/folder to cache locally.
    """
    #TODO: form this into the correct `dict` expected by the marshaler.
    return cluster.pins.add(reqpath)

def unpin(reqpath=None, **kwargs):
    """Pins the specified file to the local node. This essentially creates a
    cached copy of the local file.

    Args:
        reqpath (str): the IPFS address of the file/folder to cache locally.
    """
    #TODO: form the response appropriately.
    return cluster.pins.rm(reqpath)
