try:
    import thread
except ModuleNotFoundError:
    import _thread as thread  # TODO use threading

from datetime import datetime as dt

import getpass
import json
import requests
import web_log


WEBLOG_VERSION = "1.1.0"


def LogSync(application, event, user=None, extra_info=None, url=None):
    """This method is synchronous, and will halt execution for a few milliseconds.

    @application should be a unique identifier for an application.  @event
    should be 'launch', 'exit', 'error', 'exception' or any other easily
    recognizable event identifier.

    @user can be left empty, in which case getpass.getuser() will be used to
    determine username from OS.

    @extra_info can be (preferably) a dictionary, or a string, or any other
    object that can be read as a string (implements __str__).

    """
    if url is None:
        url = "http://%s:%s%s" % (
            web_log.constants.WEBLOG_SERVER,
            web_log.constants.WEBLOG_PORT,
            web_log.constants.WEBLOG_PATH,
        )
    log_dict = fill_standard_event(application, event, extra_info, user)

    headers = {"content-type": "application/json"}
    proxies = {"http": None, "https": None}

    # There seems to be some issues when there are multiple log
    # requests from the same executable, we just look another way.
    try:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    except ImportError:
        pass

    try:
        data = json.dumps(log_dict)
        response = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
            timeout=web_log.constants.WEBLOG_TIMEOUT,
            proxies=proxies,
        )
        return True
    except Exception as err:
        print(err)
        return False


def fill_standard_event(application, event, extra_info=None, user=None):
    """
    Generates a dictionary with standard information all log-calls should contain, adding extra_info either as a string
    if it is a string, or flatten it out if it is a dictionary.
    """
    if user is None:
        user = getpass.getuser()
    extra_dict = {}
    extra = ""
    if extra_info:
        if isinstance(extra_info, str):
            extra = extra_info
        elif isinstance(extra_info, dict):
            extra_dict = extra_info
        else:
            extra = str(extra_info)
    log_dict = {
        "application": application,
        "event": event,
        "user": user,
        "node_timestamp": dt.utcnow().isoformat(),
        "logger": "%s %s" % (__file__, WEBLOG_VERSION),
    }
    log_dict.update(extra_dict)
    if extra:
        log_dict["extra_info"] = extra
    return log_dict


def LogAsync(application, event, user=None, extra_info=None, url=None):
    """This function is asynchronous. To log application shutdown, use log_sync instead """
    thread.start_new_thread(LogSync, (application, event, user, extra_info, url))


def log(
    application, event, user=None, extra_info=None, url=None, async_=False, **kwargs
):
    """Shorthand for either LogSync or LogAsync.  Will log asynchronously if
    async=True, that is, it will start a new thread for performing requests.
    Otherwise it blocks until the logging request is performed.
    """

    if async_ or "async" in kwargs and kwargs["async"]:
        LogAsync(application, event, user=user, extra_info=extra_info, url=url)
    else:
        LogSync(application, event, user=user, extra_info=extra_info, url=url)
