"""
This module wraps the Conductor API.
"""

import logging
import sys
import re
import requests
import requests.auth
import dateutil.parser
import threading
import json
import zmq

from time import sleep
from datetime import datetime, timedelta
from collections import namedtuple
from getpass import getpass
from operator import itemgetter
from copy import deepcopy
from enum import IntEnum
from ws4py.client.threadedclient import WebSocketClient

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

import conductor

CONDUCTOR_LIBRARY_VERSION = '1.6.0a2'

PRODUCTION = 'conductor'
DEVELOP = 'dev'
HOSPITALITY = 'hospitality'

INSTANCE = conductor.PRODUCTION

DEV = False

LOG = logging.getLogger(__name__)
CLIENT_EDGE_POLL_PERIOD_S = 1.0
ALLOWED_PORT_RANGE = range(0, 128)

NODE_TYPE_PATTERN = r'^\$([0-9]+)\$.*'

UplinkMessage = namedtuple('UplinkMessage', ['module', 'gateway', 'payload_hex', 'port',
                                             'receive_time', 'uuid', 'network_token',
                                             'packet_data', 'avg_signal_data'])

PacketSignalData = namedtuple('PacketSignalData', ['spreading_factor', 'snr', 'rssi', 'frequency'])

LTEPacketSignalData = namedtuple('LTEPacketSignalData', ['cell_id',
                                                         'cell_rsrp',
                                                         'cell_rsrq',
                                                         'cell_tac',
                                                         'imei'])

EventRollup = namedtuple('EventRollup', ['count', 'start_time'])
AccountActivity = namedtuple('AccountActivity', ['count', 'last_seen_time', 'subject_id'])


def ACCESS_URL():
    return 'https://access-{}.{}.com/access'.format(conductor.INSTANCE, 'link-labs' \
            if INSTANCE != HOSPITALITY else 'airfinder')

def CLIENT_EDGE_URL():
    return 'https://clientedge-{}.{}.com/clientEdge'.format(conductor.INSTANCE, 'link-labs' \
            if INSTANCE != HOSPITALITY else 'airfinder')

def NETWORK_ASSET_URL():
    return 'https://networkasset-{}.{}.com/networkAsset'.format(conductor.INSTANCE, 'link-labs' \
            if INSTANCE != HOSPITALITY else 'airfinder')

class NodeType(IntEnum):
    GATEWAY_SYMPHONY = 101
    REPEATER_SYMPHONY = 201
    MOD_SYMPHONY = 301
    MOD_LTE_M = 303
    APP_TOKEN = 401
    MOD_VIRTUAL = 501
    MOD_SYMBLE = 502
    NONE = 999


class ConductorSubject(object):
    """
    Base class for subclasses that are Conductor subjects.

    All subjects need a subject name (unique to the class),
    subject ID (unique to the object), and an authenticated session.
    """
    subject_name = None

    def __init__(self, session, subject_id, _data=None):
        self.session = session
        self.subject_id = subject_id
        self._data = _data

    def __str__(self):
        return str(self.subject_id)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.subject_id == other.subject_id
        return NotImplemented

    def __neq__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash((self.subject_name, self.subject_id))

    def rename(self, new_name):
        """ """
        raise NotImplemented

    def get_accessors(self):
        """ """
        raise NotImplemented

    def add_accessor(self, account):
        """ """
        raise NotImplemented

    def remove_accessor(self, account):
        """ """
        raise NotImplemented

    def get_owners(self):
        """ """
        raise NotImplemented

    def add_owner(self, account):
        """ """
        raise NotImplemented

    def remove_owner(self, account):
        """ """
        raise NotImplemented

    def get_sharees(self):
        """ """
        raise NotImplemented

    def add_sharee(self, account):
        """ """
        raise NotImplemented

    def set_enabled(self, enabled):
        """ """
        raise NotImplemented

    def add_metadata_property(self, key, value):
        """ """
        raise NotImplemented

    def delete_metadata_property(self, key):
        """ """
        raise NotImplemented

    def get_metadata(self):
        """ """
        url = '{}/{}/{}/metadata'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_metadata_properties(self):
        """ """
        url = '{}/{}/{}/metadata/properties'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()


class ConductorSubscription(object):
    """
    docstring for ConductorSubscription
    """

    def __init__(self, *args, **kwargs):
        super(ConductorSubscription, self).__init__()
        self.subject_name = kwargs.get('subject_name')
        self.subject_id = kwargs.get('subject_id')
        self.callback = kwargs.get('callback')
        self.session = kwargs.get('session')
        self.thread = None
        self.stop_event = threading.Event()
        self.url = '{}/data/uplinkPayload/{}/{}/subscriptions'.format(
                CLIENT_EDGE_URL(), self.subject_name, self.subject_id)
        self.data = {
            'channelRequest': {'type': ''},
            'subscriptionProperties': {'filterProperties': []}
        }

    def start(self):
        """ Start the Subscription Thread. """
        self.thread = threading.Thread(target=self._run)
        self._init_thread()
        self.thread.start()

    def _init_thread(self):
        """ initialize the thread w this function. """
        pass

    def _run(self):
        """ The Subscription Thread. """
        pass

    def stop(self):
        """ Kill the Subscription Thread. """
        pass


class WebSocketSubscription(ConductorSubscription):
    """docstring for WebSocketSubscription"""

    class WSClient(WebSocketClient):
        """
        If the connection to a websocket endpoint occurs in the context of a web browser,
        then the authentication is handled by the web browser. The credentials are the user’s
        Conductor username and password.
        """
        callback = None

        def __enter__(self):
            return self

        def set_callback(self, callback):
            self.callback = callback

        def received_message(self, message):
            """ Method called on every received message. """
            LOG.debug("Received subscription message: %s", message)
            self.callback(_result_to_uplink_message(json.loads(str(message))))

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

        def closed(self, code, reason=None):
            LOG.info("Closing subscription: %s, %s", code, reason)

    def __init__(self, *args, **kwargs):
        super(WebSocketSubscription, self).__init__(*args, **kwargs)
        self.data['channelRequest']['type'] = 'Websocket'
        self.client = None

    def _init_thread(self):
        # Send URL Request...
        resp = self.session.post(self.url, json=self.data)
        resp.raise_for_status()
        ws_url = resp.json()['websocketUrl']['href']

        # Set up the Web Socket Client
        self.client = self.WSClient(
            ws_url,
            headers=resp.request.headers.items(),
            heartbeat_freq=2.0)
        self.client.set_callback(self.callback)
        self.client.connect()

    def _run(self):
        LOG.info("Opening subscription for %s", self.subject_id)
        while not self.client.terminated and not self.client.server_terminated and not self.stop_event.is_set():
            continue

    def stop(self):
        self.stop_event.set()

        # Close the socket.
        LOG.info("Closing subscription for %s", self.subject_id)
        self.client.close()


class ZeroMQSubscription(ConductorSubscription):
    """
    ZeroMQ subscriptions provide a way for a client to set up a ZeroMQ REQ/REP
    socket pair to stream events. The client should set up a ZeroMQ REP socket
    "server" to listen for events. When the server receives an event, it must
    send a Response json object back to acknowledge receipt of the event.
    If the acknowledgment is not received within 10 seconds, the ZeroMQ socket
    will be assumed to be dead and the subscription will be closed. It is
    recommended that the client send the response right away after receiving
    the event, and not after processing the event in order to ensure the
    channel stays alive.
    """

    def __init__(self, *args, **kwargs):
        super(ZeroMQSubscription, self).__init__(*args, **kwargs)
        self.data['channelRequest']['type'] = 'ZeroMQ2'
        # self.PORT = 2555
        self.PORT = 5001

        self.RSP = {
            "requestId": None,
            "responseStatus": {"OK": None},
            "service": "Subscription",
            "method": "Subscription",
            "responseData": None
        }
        self.CLOSE_RSP = {
            "subscriptionId": None,
            "messageType": None,
            "headers": {
                "matchedEventCount": 0,
                "ClosedReason": None,
                "publishedEventCount": 0
            },
            "event": None
        }

        self.event_count = 0
        self.published_event_count = 0
        self.subscription_id = None
        self.stop_event = threading.Event()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.ip = requests.get('https://api.ipify.org').text

        # Open the ZeroMQ Server
        self.socket.bind("tcp://*:{}".format(self.PORT))
        self.data['channelRequest']['endpoint'] = self.endpoint

    def _init_thread(self):
        # Send URL Request...
        resp = self.session.post(self.url, json=self.data)
        resp.raise_for_status()
        self.subscription_id = resp.json()['id']

    def _run(self):
        LOG.info("Opening subscription for %s", self.subject_id)
        while not self.socket.closed and not self.stop_event.is_set():
            events = self.socket.poll(500)

            if not events:
                continue
            print(events)

            for event in events:
                print(event)
                self.event_count += 1
                self.callback(_result_to_uplink_message(event))

                try:
                    self._send_response(event['uuid'])
                except Exception as e:
                    LOG.error(e)
                    self.stop_event.set()

    def _send_response(self, uuid):
        """ """
        response = self.RSP
        response['requestId'] = uuid
        return self.socket.send_json(response)

    def _close_subscription(self, error=None):
        """ """
        response = self.CLOSE_RSP
        response['subscriptionId'] = self.subscription_id
        response['messageType'] = 'UnsubscribeRequest' if not error else "Error"
        response['headers']['matchedEventCount'] = self.event_count
        response['headers']['publishedEventCount'] = self.published_event_count
        response['headers']['ClosedReason'] = "Requested by user" if not error else error
        return self.socket.send_json(response)

    def stop(self):
        self.stop_event.set()

        # Close the socket.
        # LOG.info("Closing subscription for %s", self.subject_id)

        # while self.thread.is_alive():
        #     LOG.info("Thread is alive...")
        #     self.thread.join()

        # LOG.info("Thread is dead!")

        # if not self.socket.closed:
        #     self._close_subscription()
        #     self.socket.unbind("tcp://*:{}".format(self.PORT))

    @property
    def endpoint(self):
        """ The Endpoint is the protocol/address/port of the zmq server. """
        return "tcp://{}:{}".format(self.ip, self.PORT)
        # return "tcp://*:{}".format(self.PORT)
        # return "tcp://localhost:{}".format(self.PORT)


class UplinkSubjectBase(ConductorSubject):
    """
    Base class for things that can be queried against for uplink payloads.
    This should not be used directly.
    """
    uplink_type = 'uplinkPayload'

    def get_messages_time_range(self, start, stop=None):
        """
        Retrieves all messages within a start and stop time.

        The `start` and `stop` arguments must be `datetime.datetime` objects.
        If `stop` is `None`, then the current time will be used.

        Returns a list of `UplinkMessage` objects.
        """
        stop = stop or datetime.utcnow()
        base_url = '{}/data/{}/{}/{}/events/{}/{}'.format(CLIENT_EDGE_URL(),
            self.uplink_type, self.subject_name, self.subject_id, format_time(stop), format_time(start)
        )
        paged_url_ext = ''

        messages = []
        more_results = True
        while more_results:
            resp = self.session.get(base_url + paged_url_ext)
            resp.raise_for_status()
            resp_data = resp.json()

            messages.extend([_result_to_uplink_message(m) for m in resp_data['results']])
            if resp_data['moreRecordsExist']:
                paged_url_ext = '?pageId={}'.format(resp_data['nextPageId'])
            else:
                more_results = False

        messages = sorted(messages, key=lambda m: m.receive_time)
        return messages

    def get_recent_messages(self, mins_back):
        """ Gets the messages received in the last `mins_back` minutes. """
        now = datetime.utcnow()
        return self.get_messages_time_range(now - timedelta(minutes=mins_back))

    def subscribe(self, callback, channel):
        """
        Sets up a subscription. The `cb` function will be called
        with an `UplinkMessage` argument for every received message. The
        channel must be either Websocket or ZeroMQ2.

        Returns a Subscription object. Call the `close` method on
        the subscription object when done.
        """
        if channel == 'ZeroMQ2':
            sub = ZeroMQSubscription
        elif channel == 'Websocket':
            sub = WebSocketSubscription
        else:
            raise SubscriptionError(self, "Channel must be 'WebSocket' or 'ZeroMQ2'!")
        return sub(
            subject_name=self.subject_name,
            subject_id=self.subject_id,
            callback=callback,
            session=self.session)


class UplinkSubscriptionIterator(UplinkSubjectBase):
    """
    A mix-in providing a helper method for returning a synchronous
    subscription generator.
    """

    def subscribe_ws_iter(self):
        """
        Sets up a subscription, but returns a generator that yields
        `UplinkMessage` object and returns when the subscription
        is closed.
        """
        queue = Queue()

        def callback(message):
            """ Puts the message in the thread-safe queue to be received synchronously. """
            queue.put(message)

        with self.subscribe_ws(callback) as sub:
            while True:
                try:
                    msg = queue.get(timeout=0.2)
                    yield msg
                except Empty:
                    if sub.client_terminated or sub.server_terminated:
                        return


class UplinkSubject(UplinkSubscriptionIterator, UplinkSubjectBase):
    """ A class combining the mixins for all uplink subjects. """
    pass


class EventCount(ConductorSubject):
    """ A class for getting event counts for a subset of uplink subjects """
    rollup_params = ['yearly', 'monthly', 'daily', 'hourly', '5minute', '1minute']
    event_type = 'uplinkPayload'

    def get_event_count_time_range(self, start, stop=None):
        """
        Gets a count of messages within a start and stop time.

        The `start` and `stop` arguments must be `datetime.datetime` objects.
        If `stop` is `None`, then the current time will be used.

        Returns an integer count of uplinkPayload events.
        """
        stop = stop or datetime.utcnow()
        url = '{}/activity/{}/{}/{}'.format(NETWORK_ASSET_URL(),
            self.subject_id, format_time(stop), format_time(start)
        )

        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()

        event_count = data.get('eventCount')
        return event_count

    def get_recent_event_count(self, mins_back):
        """ Gets the count of messages received in the last `mins_back` minutes. """
        now = datetime.utcnow()
        return self.get_event_count_time_range(now - timedelta(minutes=mins_back))

    def get_event_count_rollup(self, start, stop=None, rollup='hourly'):
        """
        Gets a rolled-up count of events for the provided time frame and interval.
        :param start: start time datetime object
        :param stop: stop time datetime object
        :param rollup: rollup interval
        :return: list of EventRollup namedtuples
        """
        stop = stop or datetime.utcnow()
        url = '{}/activity/{}/{}/{}/{}/rollup?rollup={}'.format(NETWORK_ASSET_URL(),
            self.subject_id, self.event_type, format_time(stop), format_time(start), rollup
        )

        if rollup not in self.rollup_params:
            raise ValueError('{} is not a valid rollup interval, should be one of {}'.format(
                rollup, self.rollup_params
            ))

        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for d in data:
            ts = d.get('description')
            results.append(EventRollup(d.get('eventCount'), parse_time(ts) if ts else None))
        if results:
            return sorted(results, key=lambda e: e.start_time)
        return None


class DownlinkSubject(ConductorSubject):
    """ A class for sending downlink messages. """

    def _send_message_with_body(self, body, payload, acked=True,
                                time_to_live_s=60.0, port=0, priority=10):
        if port not in ALLOWED_PORT_RANGE:
            raise ValueError("Port must be within [0, 127]")

        url = '{}/issueCommand'.format(CLIENT_EDGE_URL())

        # We're only looking for one link to respond
        ack_ratio = sys.float_info.epsilon if acked else 0

        body['commandProperties'] = {
            "payloadHex": hexlify(payload),
            "commReqs": {
                "requiredAckRatio": ack_ratio,
                "requiredSuccessfulAckRatio": ack_ratio,
                "priority": int(priority),
                "ttlMSecs": int(time_to_live_s * 1000),
                "portNumber": port,
            }
        }
        resp = self.session.post(url, json=body)
        resp.raise_for_status()
        data = resp.json()
        issuance_id = data['issuanceId']
        return DownlinkMessage(self.session, issuance_id, _data=data)

    def query_downlink(self, start, stop=None):
        """ Queries Conductor for all downlink sent to this subject. """
        stop = stop or datetime.utcnow()
        url = '{}/commands/{}/{}/{}/{}'.format(CLIENT_EDGE_URL(),
            self.subject_name, self.subject_id, format_time(stop), format_time(start))
        resp = self.session.get(url)
        resp.raise_for_status()
        return [DownlinkMessage(self.session, result['issuanceId'], _data=result)
                for result in resp.json()]


class ConductorAccount(UplinkSubject):
    """
    This class provides methods for interacting with Conductor for a particular account.

    This is the starting point for everything else in this module. Initialize with your
    username and password. If the password is omitted the initializer will prompt for one.
    Optionally provide the account name that you're trying to access (if you don't provide
    the account, the constructor will try to figure out which account is linked to your username).
    """

    subject_name = 'accountId'

    def __init__(self, username, password=None, account_name=None):
        password = password or getpass('Conductor password for {}:'.format(username))
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(username, password)

        if account_name:
            # Find account ID for the account name, if given
            resp = self.session.get('{}/accountName/{}'.format(ACCESS_URL(), account_name))
            resp.raise_for_status()
            account = resp.json()
        else:
            # Look up all the accounts associated with this user, and use the first one.
            accounts = self._get_accounts()
            LOG.debug("Got accounts: %s", accounts)
            if len(accounts) == 0:
                raise RuntimeError("No account associated with username")
            elif len(accounts) > 1:
                LOG.warning("More than one account associated with username")
            account = accounts[0]

        self.account_id = account['id']
        self.account_name = account['name']

        super(ConductorAccount, self).__init__(self.session, self.account_id, _data=account)

    def __str__(self):
        return self.account_name

    def _get_accounts(self):
        """ Gets the accounts associated with this username. Returns a list of dictionaries. """
        url = ''.join([ACCESS_URL(), '/accounts'])
        resp = self.session.get(url, params={'username': self.session.auth.username})
        resp.raise_for_status()
        return resp.json()

    def _get_registered_asset(self, subject_name, subject_id):
        """ Base function for getting a registered asset from the Network Asset API. """
        url = '{}/{}/{}'.format(NETWORK_ASSET_URL(), subject_name, subject_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def _get_registered_assets(self, asset_name):
        """ Base function for getting list of registered assets from the Network Asset API. """
        url = '{}/{}'.format(NETWORK_ASSET_URL(), asset_name)
        params = {'accountId': self.account_id, 'lifecycle': 'registered'}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_gateways(self):
        """ Returns a list of `Gateway` objects that have been registered to this account. """
        return [Gateway(self.session, x['nodeAddress'], x['registrationToken'], _data=x)
                for x in self._get_registered_assets('gateways')]

    def get_gateway(self, gateway_addr):
        """ Opens a gateway by address. Returns a `Gateway` object. """
        asset = self._get_registered_asset('gateway', gateway_addr)
        return Gateway(self.session, gateway_addr, asset['registrationToken'], _data=asset)

    def get_modules(self):
        """ Returns a list of `Module` objects that have been registered to this account. """
        return [(LTEModule if _get_node_type(x['nodeAddress']) == NodeType.MOD_LTE_M else Module)(
                self.session, x['nodeAddress'], _data=x) for x in self._get_registered_assets('modules')]

    def get_module(self, module_addr):
        """ Opens a module by address. Returns a 'Module' object. """
        asset = self._get_registered_asset('module', module_addr)
        if _get_node_type(module_addr) == NodeType.MOD_LTE_M:
            return LTEModule(self.session, module_addr, _data=asset)
        return Module(self.session, module_addr, _data=asset)

    def get_lte_module(self, imei):
        """ Opens an LTE Module by IMEI. Returns an 'LTEModule' object. """
        asset = self._get_registered_asset('lte/imei', imei)
        return LTEModule(self.session, asset['nodeAddress'], _data=asset)

    def register_lte_module(self, imei, iccid, zipcode, app_token):
        """ Creates a Conductor instance of the LTE module. """
        url = '{}/lte/register'.format(NETWORK_ASSET_URL())
        data = {
            "account": {
                "href": self.account_id,
                "desc": ""
            },
            "token": app_token,
            "iccId": iccid,
            "imei": imei,
            "zipCode": zipcode
        }
        params = {'accountId': self.account_id, 'lifecycle': 'registered'}
        resp = self.session.get(url, params=params, json=data)
        resp.raise_for_status()
        asset = resp.json()
        return LTEModule(self.session, asset['nodeAddress'], _data=asset)

    def get_application_tokens(self):
        """ Returns a list of application tokens that have been registered to this account. """
        return [AppToken(self.session, x['hash'], _data=x)
                for x in self._get_registered_assets('applicationTokens')]

    def get_application_token(self, app_token_hash):
        """ Opens an application token object by hash. Returns an `AppToken` object. """
        asset = self._get_registered_asset('applicationToken', app_token_hash)
        return AppToken(self.session, app_token_hash, _data=asset)

    def create_network_token(self):
        """ """
        raise NotImplemented

    def get_network_tokens(self):
        """ Returns a list of network tokens that have been registered to this account. """
        return [NetToken(self.session, x['hash'], _data=x)
                for x in self._get_registered_assets('networkTokens')]

    def get_network_token(self, net_token_hash):
        """ Opens a network token object by hash. Returns a `NetToken` object. """
        asset = self._get_registered_asset('networkToken', net_token_hash)
        return NetToken(self.session, net_token_hash, _data=asset)

    def delete_network_token(self, network_token):
        """ """
        raise NotImplemented

    def create_asset_group(self, name):
        """ Create a new Asset Group. """
        url = '{}/assetGroups'.format(NETWORK_ASSET_URL())
        data = {
            "account": {
                "href": self.account_id,
                "desc": ""
            },
            "assetGroupName": name
        }
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        asset = resp.json()
        return AssetGroup(self.session, asset['id'], _data=asset)

    def get_asset_groups(self):
        """ Returns a list of asset groups that have been registered to this account. """
        return [AssetGroup(self.session, x['id'], _data=x)
                for x in self._get_registered_assets('assetGroups')]

    def get_asset_group(self, asset_group_hash):
        """ Opens an Asset Group Object by hash. Returns a 'AssetGroup' object. """
        asset = self._get_registered_asset('assetGroup', asset_group_hash)
        return AssetGroup(self.session, x['id'], _data=asset)

    def delete_asset_group(self, asset_group):
        """ """
        raise NotImplemented

    def get_downlink_message(self, issuance_id):
        """ Opens an issued command. Returns a Downlink Message. """
        asset = self._get_registered_asset('issuedCommand', issuance_id)
        return DownlinkMessage(self.session, x['hash'], _x=asset)

    def get_event_count(self, start, stop=None):
        """ Gets the event count for this account for the provided time range """
        stop = stop or datetime.utcnow()
        url = '{}/activity/account/{}/{}/{}'.format(NETWORK_ASSET_URL(),
            self.account_id, format_time(stop), format_time(start)
        )
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        filtered_data = [d for d in data if d.get('lastSeenTime')]

        results = []
        for d in filtered_data:
            ts = d.get('lastSeenTime')
            res = AccountActivity(
                d.get('eventCount'),
                parse_time(ts) if ts else None,
                d.get('subjectId')
            )
            results.append(res)
        if results:
            return sorted(results, key=lambda e: e.last_seen_time)
        return None


class AppToken(UplinkSubject, DownlinkSubject):
    """ Represents an application designated by an app token for an account. """
    subject_name = 'applicationToken'

    def send_message(self, payload, gateway_addr=None, acked=False,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a multicast message to all nodes registered to this app token.

        The 'acked' parameter is there to have the same function signature as other 'send_message'
        methods, but it must be False.
        """
        if acked:
            raise ValueError("Multicast messages cannot be acknowledged")

        body = {}
        if gateway_addr:
            body['commandRoutes'] = {
                'linkAddresses': [self._to_node_address() + '!101!' + gateway_addr]}
        else:
            body['commandTargets'] = {'targetAppToken': self.subject_id}

        return self._send_message_with_body(body, payload, False, time_to_live_s, port, priority)

    # We need to override query_downlink because we need to use the node address form
    def query_downlink(self, *args, **kwargs):
        """ Queries Conductor for all downlink sent to this subject. """
        temp = deepcopy(self)
        temp.subject_name = 'node'
        temp.subject_id = self._to_node_address()
        return super(AppToken, temp).query_downlink(*args, **kwargs)

    def _to_node_address(self):
        """
        Converts an app token to the node address format that Conductor understands.

        Example
        -------
        : app_token
        AppToken(1bcda4a2e8c1af83d330)
        : app_token._to_node_address()
        '$401$1bcda4a2-e8c1af83-0-00000d330'
        """
        app_token = str(self.subject_id)
        return '$401${}-{}-{}-{:0>9}'.format(app_token[:8], app_token[8:16], 0, app_token[16:])


class NetToken(UplinkSubject):
    """ Represents a network designated by a network token for an account. """
    subject_name = 'networkToken'

class AssetGroup(UplinkSubject, DownlinkSubject):
    subject_name = 'assetGroup'

    @property
    def name(self):
        return self._data['name']

    def rename(self, new_name):
        """ Rename the user-friendly Asset Group Name. """
        url = '{}/{}/{}/{}'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id, new_name)
        resp = self.session.put(url)
        resp.raise_for_status()

    def add_nodes(self, nodes):
        """ Bulk add tags to the Asset Group. """
        raise NotImplemented

    def add_node(self, node):
        """ Add a tag to the asset group. """
        url = '{}/{}/{}/nodes'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {
            "href": node,
            "desc": ""
        }
        resp = self.session.patch(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def remove_node(self, node):
        """ Remove a tag from the Asset Group. """
        url = '{}/{}/{}/nodes'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {
            "href": node,
            "desc": ""
        }
        resp = self.session.delete(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_nodes(self):
        """ Get a list of tags in the asset group. """
        url = '{}/{}/{}/nodes'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {'subjectId': self.subject_id}
        resp = self.session.get(url, json=data)
        resp.raise_for_status()
        return [Module(self.session, x['desc'], _data=x) for x in resp.json()]

    def get_application_tokens(self):
        """ Get the Application Tokens in the Asset Group. """
        url = '{}/{}/{}/applicationTokens'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {'subjectId': self.subject_id}
        resp = self.session.get(url, json=data)
        resp.raise_for_status()
        print(resp.json())
        return [AppToken(self.session, x['desc'], _data=x) for x in resp.json()]

    def add_application_token(self, appToken):
        """ Add an Application Token to the Asset Group. """
        url = '{}/{}/{}/applicationTokens'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {
            "href": appToken,
            "desc": ""
        }
        resp = self.session.patch(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def remove_application_token(self, appToken):
        """ Remove an Application Token from the Asset Group. """
        url = '{}/{}/{}/applicationTokens'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {
            "href": appToken,
            "desc": ""
        }
        resp = self.session.delete(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_network_tokens(self):
        """ Get the Network Tokens in the Asset Group. """
        url = '{}/{}/{}/nodes'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {'subjectId': self.subject_id}
        resp = self.session.get(url, json=data)
        resp.raise_for_status()
        return resp.json() #TODO: Create Network Token object
        #return [NetworkToken(self.session, x['desc'], _data=x) for x in resp.json()]

    def add_network_tokens(self, netToken):
        """ Add a Network Token in the Asset Group. """
        url = '{}/{}/{}/networkTokens'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {
            "href": netToken,
            "desc": ""
        }
        resp = self.session.patch(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def remove_network_tokens(self, netToken):
        """ Remove a Network Token in the Asset Group. """
        url = '{}/{}/{}/networkTokens'.format(NETWORK_ASSET_URL(), self.subject_name, self.subject_id)
        data = {
            "href": netToken,
            "desc": ""
        }
        resp = self.session.delete(url, json=data)
        resp.raise_for_status()
        return resp.json()


class Gateway(UplinkSubject, DownlinkSubject, EventCount):
    """ Represents a single Symphony gateway. """
    subject_name = 'node'

    def __init__(self, session, gateway_id, network_token, _data=None):
        self.network_token = network_token
        super(Gateway, self).__init__(session, gateway_id, _data)

    def get_status(self):
        """ Returns the most recent gateway status dictionary """
        url = '{}/data/gatewayStatus/node/{}/mostRecentEvents?f.__prop.type=EQ.status'.format(CLIENT_EDGE_URL(), self.subject_id)
        resp_data = self.session.get(url)
        return flatten_status(resp_data.json()['results'])

    def get_cell_status(self):
        """ Returns the most recent gateway cellular status dictionary if exists """
        url = '{}/data/gatewayStatus/node/{}/mostRecentEvents?f.__prop.type=EQ.misc_status'.format(CLIENT_EDGE_URL(), self.subject_id)
        resp_data = self.session.get(url)
        return flatten_status(resp_data.json()['results'])

    def get_statuses(self, start_time, stop_time):
        """ Returns the status messages for a particular time range. """
        url = '{}/data/gatewayStatus/node/{}/events/{}/{}'.format(CLIENT_EDGE_URL(),
                self.subject_id, format_time(stop_time), format_time(start_time))
        resp = self.session.get(url)
        resp.raise_for_status()
        return flatten_status(resp.json()['results'])

    def send_broadcast(self, payload, time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a broadcast message to all nodes listening to this gateway.

        Returns a `DownlinkMessage` object.
        """
        broadcast_mod_address = '$301$0-0-0-FFFFFFFFF'
        body = {'commandRoutes':
                    {'linkAddresses': [broadcast_mod_address + '!101!' + self.subject_id]}}
        return self._send_message_with_body(body, payload, False, time_to_live_s, port, priority)

    def get_last_data(self, n=1):
        url = '{}/data/uplinkPayload/node/{}/mostRecentEvents?maxResults={}'.format(CLIENT_EDGE_URL(), self.subject_id, n)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_last_status(self, n=2):
        url = CLIENT_EDGE_URL() + '/data/gatewayStatus/node/{}/mostRecentEvents?f.__prop.type=EQ.status&maxResults={}'.format(
            self.subject_id, n)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_last_cell_status(self, n=2):
        """ Returns the most recent gateway cellular status dictionary if exists """
        url = '{}/data/gatewayStatus/node/{}/mostRecentEvents?f.__prop.type='\
                                'EQ.misc_status&maxResults={}'.format(CLIENT_EDGE_URL(), self.subject_id, n)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def restart_gateway(self):
        payload = '7f' + str(hex(int(datetime.now().timestamp() * 1000)).split('x')[1]).zfill(16)
        body = {"commandRoutes": {"linkAddresses": ["{}!FFD!{}".format(
            self.subject_id, self.subject_id)]}}
        return self._send_message_with_body(body, payload, True, 60.0, 0, 10)


class Module(UplinkSubject, DownlinkSubject, EventCount):
    """ Represents a single Module (end node). """
    subject_name = 'node'

    def get_metadata(self):
        """ """
        url = '{}/module/{}/metadata'.format(NETWORK_ASSET_URL(), self.subject_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def send_message(self, payload, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a downlink message to a node. If the `gateway_addr` is specified,
        then the message will be sent through that gateway. Otherwise, Conductor
        will route the message automatically.

        `payload` should be a bytearray or bytes object.

        Returns a `DownlinkMessage` object, which can be used to poll for the message's
        status or cancel the message.
        """

        body = {}
        if gateway_addr:
            body['commandRoutes'] = {'linkAddresses': [self.subject_id + '!101!' + gateway_addr]}
        else:
            body['commandTargets'] = {'targetNodeAddresses': [self.subject_id]}

        return self._send_message_with_body(body, payload, acked, time_to_live_s, port, priority)

    def get_routes(self):
        """ Gets the routes for the subject """
        url = '{}/module/{}/routes'.format(CLIENT_EDGE_URL(), self.subject_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_last_data(self,n=1):
        url = '{}/data/uplinkPayload/node/{}/mostRecentEvents?maxResults={}'.format(CLIENT_EDGE_URL(), self.subject_id, n)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_asset_groups(self):
        """ Returns all the AssetGroups the module is a part of. """
        url = '{}/assetGroup/node/{}'.format(NETWORK_ASSET_URL(), self.subject_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return [AssetGroup(self.session, x['id'], _data=x) for x in data]


class LTEModule(Module):
    """ Represents a single LTE-M Module (end node). """
    subject_name = 'lte'

    def _post_status_update(self, status):
        """" Updates the status of an LTE module. """
        url = '{}/lte/{}/{}'.format(NETWORK_ASSET_URL(), self.subject_id, status)
        resp = self.session.post(url)
        resp.raise_for_status()
        return resp.json()

    def activate(self):
        """ Activate an LTE device. """
        return self._post_status_update('activate')

    def deactivate(self):
        """ Deactivate an LTE device. """
        return self._post_status_update('deactivate')

    def restore(self):
        """ Restore an LTE device. """
        return self._post_status_update('restore')

    def suspend(self):
        """ Suspend an LTE device. """
        return self._post_status_update('suspend')


class DownlinkMessage(ConductorSubject):
    """ This class represents a downlink message that has already been posted. """

    @property
    def issuance_id(self):
        """ The issuance ID is the subject ID from the ConductorSubject base class. """
        return self.subject_id

    def get_status(self):
        """ Gets the status of the downlink message.  """
        url = '{}/issuedCommand/{}/status'.format(CLIENT_EDGE_URL(), self.issuance_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()['status']

    def get_routes(self):
        """ Returns the routes that Conductor used for this message. """
        url = '{}/issuedCommand/{}'.format(CLIENT_EDGE_URL(), self.issuance_id)
        resp = self.session.get(url)
        resp.raise_for_status()
        return [assignment['assignedLink'] for assignment in resp.json()['routeAssignments']]

    def get_events(self, route=None):
        """
        Returns the events on the message and their timestamps.
        Returns a dictionary mapping routes to a list of (state, datetime) pairs.
        If `route` is specified, only the events for the specified route will be retrieved (the
        return type will be the same).

        Example
        -------
        : msg.get_events()
        {'$301$0-0-0-030001665!101!$101$0-0-0-db935317c': [
          ('Issued', datetime.datetime(2016, 6, 9, 21, 45, 56, 585000)),
          ('Submitting', datetime.datetime(2016, 6, 9, 21, 45, 57, 158000)),
          ('Submitted', datetime.datetime(2016, 6, 9, 21, 45, 57, 349000)),
          ('Sending', datetime.datetime(2016, 6, 9, 21, 45, 57, 403000)),
          ('Sent', datetime.datetime(2016, 6, 9, 21, 45, 57, 945000)),
          ('Expired', datetime.datetime(2016, 6, 9, 21, 47, 36, 531000))],
         '$301$0-0-0-030001665!101!$101$0-0-0-db9360dc0': [
          ('Issued', datetime.datetime(2016, 6, 9, 21, 45, 56, 585000)),
          ('Expired', datetime.datetime(2016, 6, 9, 21, 47, 36, 531000))]}
        """
        routes = [route] if route is not None else self.get_routes()
        route_urls = ['{}/issuedCommand/{}/statusDetail/{}'.format(CLIENT_EDGE_URL(),
            self.issuance_id, rte) for rte in routes]

        results = {}
        for url in route_urls:
            resp = self.session.get(url)
            resp.raise_for_status()
            resp_json = resp.json()
            route = resp_json['routeAssignment']['assignedLink']
            events = [(event['state'], parse_time(event['stateTime']))
                      for event in resp_json['downlinkEvents']]
            events.sort(key=itemgetter(1))
            results[route] = events

        return results

    def cancel(self):
        """ Cancels a pending downlink message. """
        LOG.debug("Deleting downlink message %s", self.issuance_id)
        url = '{}/command/{}'.format(CLIENT_EDGE_URL(), self.issuance_id)
        resp = self.session.delete(url)
        resp.raise_for_status()

    def is_complete(self):
        """
        Returns True if the message was successful, False if it is pending, and it will throw a
        DownlinkMessageError if the message was unsuccessful.
        """
        status = self.get_status()
        if 'Pending' in status:
            return False
        elif 'Success' in status:
            return True
        else:
            raise DownlinkMessageError(self, status)

    def wait_for_success(self):
        """
        Polls the status of the message and returns once it is successful.
        Raises a `RuntimeError` if the message is unsuccessful.
        """
        while not self.is_complete():
            sleep(CLIENT_EDGE_POLL_PERIOD_S)


class DownlinkMessageError(Exception):
    """
    Exception thrown when checking the success of a DownlinkMessage if it is
    neither successful nor pending.
    """
    pass


class SubscriptionError(Exception):
    """
    Exception thrown when a subscription reaches a fatal state.
    """
    pass


def parse_time(time_str):
    """ Parses a time string from Conductor into a datetime object. """
    return dateutil.parser.parse(time_str)


def format_time(dtime):
    """ Converts a `datetime` object into a string that Conductor understands. """
    return dtime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]


def flatten_status(results):
    """ Flattens the status message's 'properties' dictionary. """
    for status in results:
        status['value']['properties'] = {d['name']: d['value']
                                         for d in status['value']['properties']}
    return results


def _get_node_type(module):
    """
    Gets the node type from the module field
    :param module: module field from uplink event
    :return: NodeType IntEnum
    """
    types = [t.value for t in NodeType]
    p = re.compile(NODE_TYPE_PATTERN)
    m = re.match(p, module)
    if m:
        node_type = int(m.groups()[0])
        if node_type in types:
            return NodeType(node_type)
    return NodeType.NONE


def _result_to_uplink_message(result):
    """ Converts a 'result' dictionary from Conductor to an UplinkMessage object. """
    # Check node type for: SYM, LTE, SymBLE, etc.
    module = result['value']['module']
    node_type = _get_node_type(module)

    if node_type == NodeType.MOD_SYMPHONY:
        if result['value']['avgSignalMetadata']:
            packet_signal_data = PacketSignalData(
                result['value']['avgSignalMetadata'].get('sf'),
                result['value']['avgSignalMetadata'].get('snr'),
                result['value']['avgSignalMetadata'].get('rssi'),
                result['value']['avgSignalMetadata'].get('frequency')
            )
        else:
            packet_signal_data = None
    elif node_type == NodeType.MOD_LTE_M:
        if result['value']['avgSignalMetadata']:
            packet_signal_data = LTEPacketSignalData(
                result['value']['avgSignalMetadata'].get('cellId'),
                result['value']['avgSignalMetadata'].get('cellRsrp'),
                result['value']['avgSignalMetadata'].get('cellRsrq'),
                result['value']['avgSignalMetadata'].get('cellTac'),
                result['value']['avgSignalMetadata'].get('imei')
            )
        else:
            packet_signal_data = None
    elif node_type == NodeType.MOD_VIRTUAL:
        packet_signal_data = result['metadata'].get('props')
    else:
        packet_signal_data = None

    port = result['value'].get('portNumber')
    if port is not None:
        port = int(port)

    return UplinkMessage(
        module,
        result['value']['gateway'],
        result['value']['pld'],
        port,
        parse_time(result['time']), result['uuid'],
        result['metadata']['props'].get('net_tok'),
        packet_signal_data,
        result['value']['avgSignalMetadata']
    )


def hexlify(buff):
    """
    We write our own version of hexlify because python 3's version returns
    a binary string that can't be converted to JSON.
    """
    if isinstance(buff, str):
        buff = (ord(x) for x in buff)
    return ''.join('{:02X}'.format(x) for x in buff)
