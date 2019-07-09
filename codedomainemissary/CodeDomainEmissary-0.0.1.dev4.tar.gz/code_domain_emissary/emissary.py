from os import path
from subprocess import call
from urllib3 import PoolManager, exceptions
from mindmeld import configure_logs
from mindmeld.components.nlp import NaturalLanguageProcessor
from mindmeld import app_manager
from code_domain_emissary import handlers


class Emissary:

    def __init__(self):
        configure_logs()
        self.setup_env()
        app_path = path.dirname(path.realpath(__file__))
        nlp = NaturalLanguageProcessor(app_path)
        nlp.build()
        self._manager = app_manager.ApplicationManager(app_path, nlp=nlp)
        self._setup_handlers()

    def setup_env(self):
        http = PoolManager()

        url = 'http://localhost:7151/'
        try:
            _ = http.request('GET', url, timeout=1.0)
        except exceptions.HTTPError:
            call('mindmeld num-parse', shell=True)

    def _setup_handlers(self):
        self._manager.add_dialogue_rule('welcome', handlers.greet.welcome, domain='code', intent='greet')
        self._manager.add_dialogue_rule('say_goodbye', handlers.exit.say_goodbye, domain='code', intent='exit')
        self._manager.add_dialogue_rule('offer_help', handlers.confused.offer_help, domain='code', intent='confused')
        self._manager.add_dialogue_rule('default', handlers.default.default, default=True)

    def process(self, text=''):
        response_obj = self._manager.parse(text=text)
        response = ''
        for directive in response_obj.directives:
            if directive.get("name") == "reply":
                response += directive.get("payload").get("text")
                break
        if response == '':
            raise AttributeError("parsed request does not have a proper response payload")
        return response
