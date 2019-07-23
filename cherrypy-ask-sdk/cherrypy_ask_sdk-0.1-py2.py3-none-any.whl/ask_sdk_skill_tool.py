import json

import cherrypy

from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler
from ask_sdk_webservice_support.verifier import VerificationException
from ask_sdk_webservice_support import verifier_constants
from ask_sdk_core.exceptions import AskSdkException
from ask_sdk_core.skill import CustomSkill


class AskRequestHandler:

    def __init__(self, skill, verifiers=None, verify_signature=True, verify_timestamp=True):
        self._skill = skill
        self._verify_signature = verify_signature
        self._verify_timestamp = verify_timestamp
        if verifiers is None:
            verifiers = []
        self._verifiers = verifiers
        if not isinstance(skill, CustomSkill):
            raise TypeError(
                "Invalid skill instance provided. Expected a custom "
                "skill instance.")
        self._create_webservice_handler()

    def _create_webservice_handler(self):
        self._webservice_handler = WebserviceSkillHandler(
            skill=self._skill,
            verify_signature=self._verify_signature,
            verify_timestamp=self._verify_timestamp,
            verifiers=self._verifiers
        )
        self._webservice_handler._add_custom_user_agent("cherrypy-ask-sdk")

    def dispatch(self):
        """Dispatch the POST request coming from an alexa (Ask SDK).

        We are directly decoding/encoding the request and responses and just
        passing along the request body and responses with the expected encoding
        for the ask_sdk.

        If everything goes well, we remove any possible next handler for the
        request, given that is considered full server when is handler by the
        ask_sdk.

        Something to keep in mind, is that we are not modifying the default
        request processors, these are there to handle regular form inputs, but
        because the request that the ask_sdk uses to communicate are POST
        with JSON bodies, those are basically ignored (unless we use the JSON tool).
        """
        request = cherrypy.serving.request
        if request.method != "POST":
            raise cherrypy.HTTPError(405)
        try:
            response = self._webservice_handler.verify_request_and_dispatch(
                request.headers,
                request.body.read().decode(verifier_constants.CHARACTER_ENCODING)
            )
        except VerificationException:
            cherrypy.log.error("Request verification failed", traceback=True)
            raise cherrypy.HTTPError(400, "Incoming request failed verification")
        except AskSdkException:
            cherrypy.log.error("Skill dispatch exception", traceback=True)
            raise cherrypy.HTTPError(message="Exception occurred during skill dispatch")
        else:
            cherrypy.serving.response.body = json.dumps(response).encode(
                verifier_constants.CHARACTER_ENCODING
            )
            # remove the request handler if the request was handled as expected
            # using the ask sdk
            cherrypy.serving.request.handler = None


class AskSdkSkillTool:

    def __init__(self):
        self._registry = {}

    def _new_handler(self, skill, verifiers, verify_signature, verify_timestamp):
        handler = self._registry[skill] = AskRequestHandler(
            skill, verifiers, verify_signature, verify_timestamp
        )
        return handler

    def __call__(self, skill, verifiers=None, verify_signature=True, verify_timestamp=True):
        try:
            handler = self._registry[skill]
        except KeyError:
            handler = self._new_handler(
                skill, verifiers, verify_signature, verify_timestamp
            )
        return handler.dispatch()
