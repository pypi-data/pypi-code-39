import requests
import zope.interface

from acme import challenges
from certbot import interfaces
from certbot import reverter
from certbot.plugins import common


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(common.Plugin):
    description = "Kubernetes Authenticator Plugin"

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.reverter = reverter.Reverter(self.config)
        self.reverter.recovery_routine()
        self.env = dict() \
            # type: Dict[achallenges.KeyAuthorizationAnnotatedChallenge, Dict[str, str]]
        self.subsequent_dns_challenge = False
        self.subsequent_any_challenge = False

    @classmethod
    def add_parser_arguments(cls, add):
        add('kube-url',
            help='url or ip of the related kubernates server')

    def prepare(self):
        pass

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            'This plugin can be used to authenticate custom domain '
        )

    def get_chall_pref(self, domain):
        return [challenges.HTTP01]

    def perform(self, achalls):
        achall = achalls[0]
        validation = achall.validation(achall.account_key)
        self._create_challenge_content(achall.chall.encode('token'), validation)
        self.subsequent_any_challenge = True

        return [achall.response(achall.account_key)]

    def _create_challenge_content(self, challenge_id, challenge_content):
        URL = "http://" + self.conf('kube-url') + "/challenges"
        data = {
            "challenge_content": challenge_content,
            "challenge_id": challenge_id
        }
        print "url: " + URL
        print "challenge id: " + challenge_id
        print "challenge content: " + challenge_content
        r = requests.post(url=URL, json=data)
        print r

    def cleanup(self, achalls):
        self.reverter.recovery_routine()
