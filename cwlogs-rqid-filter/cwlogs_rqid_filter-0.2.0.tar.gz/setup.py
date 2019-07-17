# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cwlogs_rqid_filter']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0', 'ciso8601>=2.1,<3.0']

entry_points = \
{'console_scripts': ['cwlogs-rqid-filter = cwlogs_rqid_filter.console:run']}

setup_kwargs = {
    'name': 'cwlogs-rqid-filter',
    'version': '0.2.0',
    'description': 'Fetch all log events messages related to a single request (by AWS Request ID) that in any message of any event match a custom python regex pattern',
    'long_description': "# cwlogs-rqid-filter.py\n_Ever wanted to filter AWS CloudWatch logs and not only keep the matching events, but also all events that have the same Request ID that the matching event(s)?_\n\nThis python script fetches all log events messages related to requests (by AWS Request ID) that in any message of any event match a custom python regex pattern.\nIt fetches all events for the period, searching their messages with the custom regex pattern and filters only events that have the request IDs that have a message matching.\n\nChanges are described in CHANGELOG.md.\n\n## Installation\n`pip install cwlogs-rqid-filter`\n\n## Usage\nDo not forget to perform AWS Credentials configuration for boto3 beforehand (https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).\n\n### Console\nInstall the library as described above, and run it, either with `cwlogs-rqid-filter` or `python -m cwlogs_rqid_filter`\n\n\n```\n    python -m cwlogs_rqid_filter [-h] --group GROUP_NAME --filter FILTER\n                                 [--streams [STREAM_NAMES [STREAM_NAMES ...]]]\n                                 [--stream-prefix STREAM_NAME_PREFIX]\n                                 [--start-ts START_TIMESTAMP] [--start START]\n                                 [--stop-ts STOP_TIMESTAMP] [--stop STOP] [--limit LIMIT]\n                                 [--prefix-timestamp | --prefix-iso] [--debug]\n\n\nFilter AWS CloudWatch logs while keeping all events that have the same Request\nID as events that match the filter.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --group GROUP_NAME    Log group name\n  --filter FILTER       Python regular expression pattern that will match\n                        events messages\n  --streams [STREAM_NAMES [STREAM_NAMES ...]]\n                        Log stream names\n  --stream-prefix STREAM_NAME_PREFIX\n                        Log stream name prefix\n  --start-ts START_TIMESTAMP\n                        Start timestamp in milliseconds, UTC timezone\n  --start START         Start date and time, ISO8601 format, UTC timezone\n  --stop-ts STOP_TIMESTAMP\n                        Stop timestamp in milliseconds, UTC timezone\n  --stop STOP           Stop date and time, ISO8601 format, UTC timezone\n  --limit LIMIT         Event limit count\n  --prefix-timestamp    Prefix the logs with event timestamp between\n                        parentheses\n  --prefix-iso          Prefix the logs with ISO8601 formatted event timestamp\n                        between parentheses\n  --debug               Print debug information\n```\n\n### Script import\n```\nfrom cwlogs_rqid_filter import fetch_events, filter_events\n\n# Any parameters set accepted by the Boto3 logs client filter_log_events() function\nrequest_parameters = {\n    'logGroupName': 'xxx',\n    'logStreamNames': ['yyy', 'zzz', ...],\n    'logStreamNamePrefix': 'xyz',\n    'startTime': 123,                       # Unix timestamp\n    'endTime': 456,                         # Unix timestamp\n    ...\n}\n\nfilter_regex_pattern = r'*'\n\nall_events = fetch_events(request_parameters)\nfiltered_events = filter_events(all_events, filter_regex_pattern)\n```\n\n## Examples\nTo get all log events of lambda requests that took at least 1000ms, prefixed by ISO8601-formatted timestamps:\n`python -m cwlogs_rqid_filter --group /aws/lambda/someLambdaName --start 2018-11-30T05:04:00Z --stop 2018-11-30T05:05:00Z --filter 'Billed Duration: [0-9]{4,}' --prefix-iso`\n\nYou can also specify start and stop timestamps in any timezone, formatted following ISO8601: `--start 2018-11-30T14:04:00+09:00 --stop 2018-11-30T14:05:00+09:00`\n",
    'author': 'Sylvain Pascou',
    'author_email': 'sylvain@pascou.net',
    'url': 'https://github.com/spascou/cwlogs-rqid-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
