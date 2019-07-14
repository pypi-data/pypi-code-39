from tornado.options import define, parse_command_line, options
from tornado import web, ioloop, log, gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class ProxyHandler(web.RequestHandler):

    @property
    def options(self):
        return self.settings['options']

    @gen.coroutine
    def _execute(self, transforms, *args, **kwargs):
        """Executes this request with the given output transforms."""
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            self.path_args = [self.decode_argument(arg) for arg in args]
            self.path_kwargs = dict((k, self.decode_argument(v, name=k))
                                    for (k, v) in kwargs.items())
            # If XSRF cookies are turned on, reject form submissions without
            # the proper cookie
            if self.request.method not in ("GET", "HEAD", "OPTIONS") and \
                    self.application.settings.get("xsrf_cookies"):
                self.check_xsrf_cookie()

            result = self.prepare()
            if result is not None:
                result = yield result
            if self._prepared_future is not None:
                # Tell the Application we've finished with prepare()
                # and are ready for the body to arrive.
                future_set_result_unless_cancelled(self._prepared_future, None)
            if self._finished:
                return

            

            # method = getattr(self, self.request.method.lower())
            # result = method(*self.path_args, **self.path_kwargs)
            remote_url = self.options.remote_url
            _client = AsyncHTTPClient()
            target_url = remote_url.rstrip("/") + self.request.uri
            if self.request.body:
                proxy_request = HTTPRequest(
                    url=target_url,
                    method=self.request.method.upper(),
                    headers=self.request.headers,
                    body=self.request.body
                )
            else:
                proxy_request = HTTPRequest(
                    url=target_url,
                    method=self.request.method.upper(),
                    headers=self.request.headers,
                )
            result = yield _client.fetch(proxy_request)
            code, body = result.code, result.body
            if code != 200:
                self.set_status(code)
            self.write(body)
            if self._auto_finish and not self._finished:
                self.finish()
        except Exception as e:
            try:
                self._handle_request_exception(e)
            except Exception:
                app_log.error("Exception in exception handler", exc_info=True)
            finally:
                # Unset result to avoid circular references
                result = None
            if (self._prepared_future is not None and
                    not self._prepared_future.done()):
                # In case we failed before setting _prepared_future, do it
                # now (to unblock the HTTP server).  Note that this is not
                # in a finally block to avoid GC issues prior to Python 3.4.
                self._prepared_future.set_result(None)

def empty_loop():
    pass

define("remote_url", help="remote url")
define("port", type=int)

def entry():
    parse_command_line()
    app = web.Application(default_handler_class=ProxyHandler,options=options)
    
    if not options.port:
        raise ValueError("port is required")
    if not options.remote_url:
        raise ValueError("missing remote_url")
    log.gen_log.info("port:{}, remote_url:{}".format(options.port, options.remote_url))
    app.listen(options.port)
    _loop = ioloop.IOLoop.current()
    check_scheduler = ioloop.PeriodicCallback(empty_loop, 500)
    check_scheduler.start()
    _loop.start()
    
if __name__ == "__main__":
    entry()
    