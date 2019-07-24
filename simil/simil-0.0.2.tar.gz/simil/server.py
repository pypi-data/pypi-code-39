import atexit
import os
import signal
import sys
import time
from functools import lru_cache
from threading import Thread

import rpyc
from rpyc.utils.server import ThreadedServer

from .cli_args import args
from .version import version


def server(socket_path, *, load=False):
    # Fork again, to disassociate from process group
    if os.fork() > 0:
        return

    daemonize()
    set_exit_handlers(socket_path)

    t = ThreadedServer(SimilarityServer(load=load), socket_path=socket_path)
    t.start()


class SimilarityServer(rpyc.Service):
    spacy_models = [
        "en_vectors_web_lg",
        "en_core_web_lg",
        "en_core_web_md",
    ]

    def __init__(self, *, load=False):
        self.active()
        self.loaded = False

        Thread(target=self.timeout, daemon=True).start()

        if load:
            Thread(target=self.load, daemon=True).start()

    def load(self):
        if self.loaded:
            return

        self._nlp = self._load_spacy_model()
        self.loaded = True

    def _load_spacy_model(self):
        import spacy

        for model in self.spacy_models:
            try:
                loaded_model = spacy.load(model)
            except IOError as e:
                continue
            return loaded_model

        raise FileNotFoundError(
            "No spacy vector model found. "
            "Try running `python3 -m spacy download en_vectors_web_lg`. "
            "(Or you can try with `en_core_web_lg` or `en_core_web_md`.)")

    def active(self):
        self.last_active = time.time()

    @lru_cache(10)
    def nlp(self, text):
        return self._nlp(text)

    def exposed_similarity(self, client_version, first, second):
        if client_version != version:
            raise ValueError(
                "Version mismatch between client and server: try restarting the server with `simil -k`."
            )

        self.load()
        self.active()
        return self.nlp(first).similarity(self.nlp(second))

    def exposed_kill(self):
        os.kill(os.getpid(), signal.SIGINT)

    def timeout(self):
        while True:
            if time.time() - self.last_active > args.timeout:
                os.kill(os.getpid(), signal.SIGINT)
            else:
                time.sleep(1)


def set_exit_handlers(socket_path):
    def exit_handler():
        import contextlib

        with contextlib.suppress(FileNotFoundError):
            os.remove(socket_path)

    atexit.register(exit_handler)
    signal.signal(signal.SIGTERM | signal.SIGINT, lambda s, f: sys.exit(1))


def daemonize():
    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()
    os.close(0)
    os.close(1)
    os.close(2)
    os.chdir("/")
    os.setsid()
    os.umask(0)
