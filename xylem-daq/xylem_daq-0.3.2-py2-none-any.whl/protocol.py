'''
This module formats messages according to the xylem protocol to
interface with ZeroMQ sockets.

The ``*_create`` methods take in parameters and return a
properly-formatted list of ZeroMQ message frames (i.e. bytes) that
follow the protocol, ready to send out with ``send_multipart``. The
``*_parse`` methods take in a list of ZeroMQ message frames received via
``recv_multipart`` and return usable Python objects, dicts, etc.

These methods do not handle any extra frames from ZeroMQ such as
ROUTER IDs or message envelopes. Those must be stripped before calling
the ``*_parse`` methods, and added on after calling ``*_create``, as
necessary.

'''
from .common import formatter

def register_intro_create(name, short_name, heartbeat_ms, connections,
        addresses, actions):
    '''
    Generate the intro message to send to the Core to register a new
    component.

    The message contains information used by the Core to track the
    component an assign it any ZeroMQ addresses specified by the network
    architecture.

    This function is the inverse of ``register_intro_parse``.

    Parameters
    ----------
    name : string
        The component's unique name.
    short_name : string
        A short name for the component, used in other components' lists
        of ``connections``.
    heartbeat_ms : number
        The number of milliseconds to wait between sending heartbeats,
        and the time to expect before receiving heartbeats.
    connections : list of strings
        The short names of the sockets the component will connect to.
    addresses : dict of string => string
        If this component binds any sockets, the addresses for other
        sockets to use to connect. The keys are the names given in the
        architecture file for each socket this component binds. If the
        component does not bind any sockets, then the dict should be
        empty.
    actions : dict of string => string
        The actions the component can take. The keys are the names of
        the actions, and the values are descriptions, preferably
        including the parameters and return values.

    Returns
    -------
    message : list of bytes
        The properly formatted intro message. The first list element is
        by definition the byte sequence ``b'NEW'``.

    '''
    introduction = {
            'name': name,
            'short_name': short_name,
            'heartbeat_ms': heartbeat_ms,
            'connections': connections,
            'addresses': addresses,
            'actions': actions,
    }
    return [b'NEW', formatter.toBytes(introduction)]

def register_intro_parse(message):
    '''
    Parse the intro message sent to register a new component.

    This function is the inverse of ``register_intro_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the introduction, stripped of any
        ZeroMQ-specific frames such as ROUTER socket IDs.

    Returns
    -------
    introduction : dict
        The introduction message, with keys ``'name'``, ``'short_name'``,
        ``'heartbeat_ms'``, ``'connections'``, ``'addresses'``, and
        ``'actions'``.

    '''
    assert message[0] == b'NEW' and len(message) == 2
    introduction = message[1]
    return formatter.fromBytes(introduction)

def register_success_create(addresses):
    '''
    Generate the success message to indicate a new component is
    successfully registered.

    The message contains any ZeroMQ addresses that the component needs
    to communicate with its peers, as specified by the network
    architecture.

    This function is the inverse of ``register_success_parse``.

    Parameters
    ----------
    addresses : dict
        The addresses for the component to connect sockets to, grouped by
        connection name as given in the architecture file. If an address is
        unavailable, then that connection name's key should have a value
        of an empty dict.

    Returns
    -------
    message : list of bytes
        The properly formatted success message. The first list element
        is by definition the byte sequence ``b'SUCCESS'``.

    '''
    return [b'SUCCESS', formatter.toBytes(addresses)]

def register_success_parse(message):
    '''
    Parse the success message sent to acknowledge a successful component
    registration.

    This function is the inverse of ``register_success_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the success acknowledgement,
        stripped of any ZeroMQ-specific frames such as ROUTER socket
        IDs.

    Returns
    -------
    addresses : dict
        The addresses for the component to connect to.

    '''
    assert message[0] == b'SUCCESS' and len(message) == 2
    addresses = message[1]
    return formatter.fromBytes(addresses)

def register_failure_create(reason):
    '''
    Generate the failure message to indicate a new component was not
    successfully registered.

    The message contains an error message specifying the reason for the
    failure.

    This function is the inverse of ``register_failure_parse``.

    Parameters
    ----------
    reason : string
        The error message.

    Returns
    -------
    message : list of bytes
        The properly formatted failure message. The first list element
        is by definition the byte sequence ``b'FAILURE'``.

    '''
    reason = {
            'reason': reason,
    }
    return [b'FAILURE', formatter.toBytes(reason)]

def register_failure_parse(message):
    '''
    Parse the failure message sent to indicate a registration failure.

    This function is the inverse of ``register_failure_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the failure notification, stripped
        of any ZeroMQ-specific frames such as ROUTER socket IDs.

    Returns
    -------
    reason : dict
        A dict whose ``reason`` item contains an error message.

    '''
    assert message[0] == b'FAILURE' and len(message) == 2
    reason = message[1]
    return formatter.fromBytes(reason)

def controller_create(header, message):
    '''
    Generate a Controller message.

    The header and payload should be recognized by both the Core and the
    Controller, and are not checked here.

    This function is the inverse of ``controller_parse``.

    Parameters
    ----------
    header : string
        The message header.
    message : dict
        The message payload.

    Returns
    -------
    message_raw : list of bytes
        The properly formatted Controller message. The first list
        element is by definition the byte sequence
        ``b'CONTROLLER MESSAGE``.

    '''
    message_dict = {
            'header': header,
            'message': message,
    }
    return [b'CONTROLLER MESSAGE', formatter.toBytes(message_dict)]

def controller_parse(message):
    '''
    Parse a Controller message and return the header and message.

    This function is the inverse of ``controller_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the Controller message, stripped
        of any ZeroMQ-specific frames such as ROUTER socket IDs.

    Returns
    -------
    message_body : dict
        A dict with keys ``'header'`` and ``'message'`` containing the
        Controller message.

    '''
    assert message[0] == b'CONTROLLER MESSAGE' and len(message) == 2
    control_message = message[1]
    return formatter.fromBytes(control_message)

def state_update_create(state):
    '''
    Generate a state update notification message.

    This function is the inverse of ``state_update_parse``.

    Parameters
    ----------
    state : string
        The state name to send in the update.

    Returns
    -------
    message : list of bytes
        The properly formatted state update message. The first list
        element is by definition the byte sequence ``b'STATE'``.

    '''
    payload = {
            'UPDATE': state,
    }
    return [b'STATE', formatter.toBytes(payload)]

def state_update_parse(message):
    '''
    Parse a state update message to get the new state.

    This function is the inverse of ``state_update_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the state update, stripped of any
        ZeroMQ-specific frames such as ROUTER socket IDs.

    Returns
    -------
    update : dict
        A dict whose sole key, 'UPDATE', specifies the state in the
        update.

    '''
    assert message[0] == b'STATE' and len(message) == 2
    payload_raw = message[1]
    payload = formatter.fromBytes(payload_raw)
    assert 'UPDATE' in payload
    return payload

def state_request_create():
    '''
    Generate a state request message.

    Returns
    -------
    message : list of bytes
        The properly formatted state request message. The first list
        element is by definition the byte sequence ``b'STATE'``.

    '''
    return [b'STATE', b'REQUEST']

def action_create(action_id, name, params):
    '''
    Generate an action message.

    This function is the inverse of ``action_parse``.

    Parameters
    ----------
    action_id : string
        A unique ID for this action message.
    name : string
        The name of the action to invoke. The name should be on the list
        of registered action names for the component receiving the
        action message.
    params : list, tuple, finite iterable
        The parameters for executing the action.

    Returns
    -------
    message : list of bytes
        The properly formatted action message. The first list element is
        by definition the byte sequence ``b'ACTION'``.

    '''
    message_body = {
            'id': action_id,
            'name': name,
            'params': params,
    }
    return [b'ACTION', formatter.toBytes(message_body)]

def action_parse(message):
    '''
    Parse an action message to get the requested action.

    This function is the inverse of ``action_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the action message, stripped of
        any ZeroMQ-specific frames such as ROUTER socket IDs.

    Returns
    -------
    action : dict
        A dict with keys 'id', 'name' and 'params' specifying the name and
        parameters of the action to execute.

    '''
    assert message[0] == b'ACTION' and len(message) == 2
    payload_raw = message[1]
    payload = formatter.fromBytes(payload_raw)
    return payload

def action_result_create(action_id, name, params, result):
    '''
    Create an action result message.

    This function is the inverse of ``action_result_parse``.

    Parameters
    ----------
    action_id : string
        The action ID of the action being reported.
    name : string
        The name of the action that was invoked.
    params : list, tuple, finite iterable
        The parameters for the action that was invoked.
    result :
        The result or return value of the action that was invoked.

    Returns
    -------
    message : list of bytes
        The properly formatted action result message. The first list
        element is by definition the byte sequence ``b'ACTION'``.

    '''
    message_body = {
            'id': action_id,
            'name': name,
            'params': params,
            'result': result,
    }
    return [b'ACTION', formatter.toBytes(message_body)]

def action_result_parse(message):
    '''
    Parse an action result message to get the message result.

    This function is the inverse of ``action_result_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the action result message,
        stripped of any ZeroMQ-specific frames such as ROUTER socket
        IDs.

    Returns
    -------
    action_result : dict
        A dict with keys ``'id``', ``'name'``, ``'params'``, and ``'result'``
        containing the action result message.

    '''
    assert message[0] == b'ACTION' and len(message) == 2
    result_raw = message[1]
    result = formatter.fromBytes(result_raw)
    return result

def data_create(header, data_bytes):
    '''
    Generate a data message.

    This function is the inverse of ``data_parse``.

    Parameters
    ----------
    header : dict
        The header associated with the data to send, e.g. timestamp, instrument ID, etc.
        It should not contain the actual data payload.
    data_bytes : bytes
        The actual data payload, already encoded into bytes.

    Returns
    -------
    message : list of bytes
        The properly formatted data message. The first list element is
        by definition the byte sequence ``b'DATA'``.

    '''
    header_bytes = formatter.toBytes(header)
    return [b'DATA', header_bytes, data_bytes]

def data_parse(message):
    '''
    Parse a data message.

    This function is the inverse of ``data_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the data message, stripped of any
        ZeroMQ-specific frames such as ROUTER socket IDs.

    Returns
    -------
    data : dict
        A dict whose ``'header'`` key contains the header data (dict), and
        whose ``'data'`` key contains the data payload (bytes).

    '''
    assert message[0] == b'DATA' and len(message) == 3
    header_raw = message[1]
    data_bytes = message[2]
    header = formatter.fromBytes(header_raw)
    return {'header': header, 'data': data_bytes}

def info_create(timestamp, component, message):
    '''
    Create an info message.

    This function is the inverse of ``info_parse``.

    Parameters
    ----------
    timestamp : int
        The time the message was created (time.time())
    component : string
        The name of the component sending the message
    message : string
        The message to send

    Returns
    -------
    message : list of bytes
        The properly formatted info message. The first list element is
        by definition the byte sequence ``b'INFO'``.

    '''
    header = {
            'timestamp': timestamp,
            'component': component,
            }
    return [b'INFO', formatter.toBytes(header),
            formatter.toBytes(message)]

def info_parse(message):
    '''
    Parse an info message.

    This function is the inverse of ``info_create``.

    Parameters
    ----------
    message : list of bytes
        The info message to parse

    Returns
    -------
    data : dict
        A dict whose ``'header'`` key contains the message header (dict)
        and whose ``'message'`` key contains the message itself
        (string).

    '''
    assert message[0] == b'INFO' and len(message) == 3
    header_raw = message[1]
    message_raw = message[2]
    header = formatter.fromBytes(header_raw)
    message_final = formatter.fromBytes(message_raw)
    return {
            'header': header,
            'message': message_final,
            }

def log_create(level, timestamp, component, message):
    '''
    Create a log message.

    This function is the inverse of ``log_parse``.

    Parameters
    ----------
    level : string
        The log level: one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', or
        'CRITICAL'
    timestamp : int or long int
        The unix timestamp of the log message (time.time())
    component : string
        The name of the component logging the message
    message : string
        The message to record in the log

    Returns
    -------
    message : list of bytes
        The properly formatted log message. The first list element is by
        definition the byte sequence ``b'LOG'``.

    '''
    metadata = {
            'timestamp': timestamp,
            'component': component,
            'level': level,
            }
    return [b'LOG', formatter.toBytes(metadata),
            formatter.toBytes(message)]

def log_parse(message):
    '''
    Parse a log message.

    This function is the inverse of ``log_create``.

    Parameters
    ----------
    message : list of bytes
        The message frames containing the log message, stripped of any
        ZeroMQ-specific frames such as ROUTER socket IDs.

    Returns
    -------
    data : dict
        A dict whose ``'metadata'`` key contains the metadata (dict) and
        whose ``'message'`` key contains the log message (string).

    '''
    assert message[0] == b'LOG' and len(message) == 3
    metadata_raw = message[1]
    message_raw = message[2]
    metadata = formatter.fromBytes(metadata_raw)
    log_message = formatter.fromBytes(message_raw)
    return {'metadata': metadata, 'message': log_message}

