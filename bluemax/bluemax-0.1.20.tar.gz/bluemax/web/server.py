"""
    Web server with rpc handler
"""
import logging
import tornado.web
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import StaticFileHandler
from bluemax.settings import get_settings, extend
from bluemax.utils import qname_to_class
from .broadcaster import Broadcaster
from .authentication import LogoutHandler
from .auth_static_file_handler import AuthStaticFileHandler
from .rpc_websocket import RpcWebsocket, RpcHandler

BROADCASTER = Broadcaster()


def make_app(loop=None):
    """ Return a tornado app with settings and routes """
    config = get_settings("tornado", {})
    assert get_settings("procedures"), "procedures required to remote!"
    manager = qname_to_class(config.get("MANAGER", "bluemax.rpc:ContextRpc"))
    settings = {
        "debug": config.get("DEBUG", get_settings("DEBUG", False)),
        "manager": manager.rpc_for(
            get_settings("procedures"),
            services=get_settings("services"),
            loop=loop
        ),
        "cookie_name": config.get("COOKIE_NAME", "blueq-user"),
        "cookie_secret": config.get(
            "COOKIE_SECRET", "<change me - it was a dark and stormy..>"
        ),
    }
    routes = [(r"/rpc", RpcHandler), (r"/ws", RpcWebsocket)]
    if config.get("AUTH_HANDLER"):
        auth_handler = qname_to_class(config.get("AUTH_HANDLER"))
        settings["login_url"] = "/login"
        routes.insert(0, (r"/logout", LogoutHandler))
        routes.insert(0, (r"/login", auth_handler))
        if config.get("STATIC_DIR"):
            routes.append(
                (
                    r"/(.*)",
                    AuthStaticFileHandler,
                    {
                        "path": config.get("STATIC_DIR"),
                        "default_filename": "index.html",
                    },
                )
            )
            logging.info("serving from %s", config.get("STATIC_DIR"))
    elif config.get("STATIC_DIR"):
        routes.append(
            (
                r"/(.*)",
                StaticFileHandler,
                {"path": config.get("STATIC_DIR"), "default_filename": "index.html"},
            )
        )
        logging.info("serving from %s", config.get("STATIC_DIR"))
    if get_settings("urls_extend"):
        extend(get_settings("urls_extend"), routes)
    app = tornado.web.Application(routes, **settings)
    BROADCASTER.start(settings["manager"].get_broadcast_queue(), RpcWebsocket.broadcast)
    return app


def main():
    """ run the tornado web server """
    app = make_app()
    port = int(get_settings("PORT", "8080"))
    app.listen(port)
    logging.info("listening on port %s", port)
    if app.settings.get("debug") is True:
        logging.info("running in debug mode")
    ioloop = IOLoop.current()
    keep_alive_interval = int(get_settings("keep_alive_interval", "30000"))
    PeriodicCallback(RpcWebsocket.keep_alive, keep_alive_interval).start()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        logging.info("stopping")
        ioloop.stop()
