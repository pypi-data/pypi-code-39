"""Overrides the request method of the :class:`ipfshttpclient.http.HTTPClient`
so that `delete` HTTP methods can be used. Updates the client factory of the
base Client class to use this HTTPClient instead.
"""
from ipfshttpclient.http import HTTPClient, pass_defaults
from ipfshttpclient import encoding

class HTTPClusterClient(HTTPClient):
    """An HTTP client for interacting with the IPFS cluster.

    Args:
        addr(str, multiaddr.Multiaddr): The address where the IPFS daemon may
            be reached.
        base(str): The path prefix for API calls.
    	timeout(numbers.Real, tuple(numbers.Real, numbers.Real), NoneType):
    		The default number of seconds to wait when establishing a connection to
    		the daemon and waiting for returned data before throwing
    		:exc:`~ipfshttpclient.exceptions.TimeoutError`; if the value is a tuple
    		its contents will be interpreted as the values for the connection and
    		receiving phases respectively, otherwise the value will apply to both
    		phases; if the value is ``None`` then all timeouts will be disabled
    	defaults(dict): The default parameters to be passed to
    		:meth:`~ipfscluster.http.HTTPClusterClient.request`.
    """
    def __init__(self, addr, base, **defaults):
        super(HTTPClusterClient, self).__init__(addr, base, **defaults)

    @pass_defaults
    def request(self, path, method=None,
                args=[], files=[], opts={}, stream=False,
                decoder=None, headers={}, data=None,
                timeout=120, offline=False, return_result=True):
        """Makes an HTTP request to the IPFS cluster.

        This function returns the contents of the HTTP response from the IPFS
        cluster endpoint.

        Raises:
        		~ipfshttpclient.exceptions.ErrorResponse
        		~ipfshttpclient.exceptions.ConnectionError
        		~ipfshttpclient.exceptions.ProtocolError
        		~ipfshttpclient.exceptions.StatusError
        		~ipfshttpclient.exceptions.TimeoutError

        Args:
        		path(str): The REST command path to send.
                method (str): Specify the HTTP method to use; otherwise, it will
                    be "auto-detected" for most cases.
        		args(list): Positional parameters to be sent along with the HTTP request.
        		files(str, io.RawIOBase, collections.abc.Iterable): The file object(s)
                    or path(s) to stream to the daemon.
        		opts(dict): Query string paramters to be sent along with the HTTP
                    request.
        		decoder(str): The encoder to use to parse the HTTP response.
        		timeout(float): How many seconds to wait for the server to send data
        			before giving up (default 120).
        		offline(bool): Execute request in offline mode, i.e. locally without
                    accessing the network.
        		return_result(bool): Default True. If the return is not relevant,
                    such as in gc(), passing False will return None and avoid
                    downloading results.
        """
        url = self.base + path

        params = []
        params.append(('stream-channels', 'true'))
        if offline:
            params.append(('local', 'true'))

        #The no cover tags below are because the IPFS cluster API doesn't
        #require this advanced functionality *for now*.
        for opt in opts.items():# pragma: no cover
            params.append(opt)
        for arg in args:# pragma: no cover
            params.append(('arg', arg))

        if method is None:
            if (files or data):
                method = 'post'
            elif not return_result:# pragma: no cover
                method = 'head'
            else:
                method = 'get'

        # Don't attempt to decode response or stream
        # (which would keep an iterator open that will then never be waited for)
        if not return_result:# pragma: no cover
            decoder = None
            stream = False

        parser = encoding.get_encoding(decoder if decoder else "none")
        ret = self._request(method, url, params, parser, stream,
                            files, headers, data, timeout=timeout)

        return ret if return_result else None
