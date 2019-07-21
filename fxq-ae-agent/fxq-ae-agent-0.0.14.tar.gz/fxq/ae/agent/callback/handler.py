import json
import logging
import threading
from http import HTTPStatus

import requests
from fxq.core.beans.factory.annotation import Autowired

from fxq.ae.agent.constants import JSON_HEADERS, URI_LIST_HEADERS
from fxq.ae.agent.service.consul import ConsulService

LOGGER = logging.getLogger(__name__)

consul_service: ConsulService = Autowired(type=ConsulService)
callback_host = None


def get_callback_host():
    global callback_host
    try:
        callback_host = f'{consul_service.get_callback_host()}'
        LOGGER.info(f'Configuring callback host as {callback_host}')
    except Exception as e:
        LOGGER.error(e)
    finally:
        t = threading.Timer(30.0, get_callback_host)
        t.start()


get_callback_host()


def get_callback_url(ref_object):
    if ref_object.__class__.__name__ == "Run":
        return f'{callback_host}/api/data/runs'
    if ref_object.__class__.__name__ == "Step":
        return f'{callback_host}/api/data/steps'
    if ref_object.__class__.__name__ == "Command":
        return f'{callback_host}/api/data/commands'


def register_new_object(ref_object, callback_url):
    '''
    Registers the object with the callback URL by posting the to_dict()
    content of the referenced object to the callback_url.

    Once the response is received from the server links are added showing the object
    has previously been created.

    :param ref_object: The Object to be serialized for the endpoint
    :param callback_url: The Endpoint to receive the POST request
    :return: NA
    '''
    LOGGER.debug(f"Registering New Object: {ref_object} at {callback_url}")
    r = requests.post(
        "%s" % callback_url,
        data=json.dumps(ref_object.to_dict()),
        headers=JSON_HEADERS)
    if r.status_code == HTTPStatus.CREATED:
        ref_object._links = r.json()["_links"]
    else:
        LOGGER.error("Post Callback Failed with Status Code %s" % r.status_code)
        LOGGER.debug("%s - %s" % (r.status_code, r.text))
        raise Exception("Post Callback Failed with Status Code %s" % r.status_code)

    update_links(ref_object)


def update_existing_object(ref_object, callback_url):
    '''
    Simply Sends a PATCH request with the serialized representation of the object to update assocaited
    fields on their change.

    :param ref_object: The Object to be serialized for the endpoint
    :param callback_url: The Endpoint to receive the POST request
    :return: NA
    '''
    LOGGER.debug(f"Updating Existing Object: {ref_object} at {ref_object._links['self']['href']}")
    r = requests.patch(
        ref_object._links["self"]["href"],
        data=json.dumps(ref_object.to_dict()),
        headers=JSON_HEADERS)
    if r.status_code != HTTPStatus.OK:
        LOGGER.error("Post Callback Failed with Status Code %s" % r.status_code)
        LOGGER.debug("%s - %s" % (r.status_code, r.text))
        raise Exception("Post Callback Failed with Status Code %s" % r.status_code)


def update_links(ref_object):
    '''
    Scans the _links definition as returned by the server, if it finds an attribute
    of the same name it will get the href from that linked attribute and associate it
    with this object.

    i.e. If ObjectA has links to self, objectA and objectB, this will look for an attribute
    by the name of objectB in the python objectA, it then get its link and uses a PUT request
    to associate the two together server side.

    :param ref_object: The object to scan for links and references
    :return: NA
    '''
    _link_exclusion = ['self', str(ref_object.__class__.__name__).lower()]
    for link_name, link_value in ref_object._links.items():
        if link_name not in _link_exclusion:
            try:
                associated_object = getattr(ref_object, link_name)
                LOGGER.info(
                    "%s is being linked to %s" % (link_value["href"], associated_object._links["self"]["href"]))
                requests.put(link_value["href"], data=associated_object._links["self"]["href"],
                             headers=URI_LIST_HEADERS)
            except AttributeError:
                LOGGER.info("No associated object exists of type %s for type %s" % (
                    link_name, ref_object.__class__.__name__))


def do_callback(ref_object):
    callback_url = get_callback_url(ref_object)
    if callback_url:
        LOGGER.info(f"Performing Callback for {ref_object.__class__.__name__} - {ref_object.to_dict()}")
        if ref_object._links:
            update_existing_object(ref_object, callback_url)
        elif ref_object._links is None:
            register_new_object(ref_object, callback_url)
    else:
        LOGGER.warning("No Callback URL could be determined")
