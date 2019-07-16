# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
This API is used to invoke and retrieve AutoSupport messages from the nodes in the cluster.<p/>
This API supports POST and GET calls. A POST call is used to invoke AutoSupport and a GET call is used to retrieve AutoSupport messages.
---
## Examples
### Invoking an AutoSupport on all nodes in the cluster
The following example invokes an AutoSupport on every node in the cluster.
Note that AutoSupport is invoked on all nodes in the cluster if the `node` param is omitted. Also, note that the `subject` line is the same when invoking on all nodes.<p/>
By default, the response is an empty object. If `return_records=true` is passed in the request, the response includes information about the node and the index of the invoked AutoSupport message.
```JSON
# The API:
POST /support/autosupport/messages
# The call:
curl -X POST "https://<mgmt-ip>/api/support/autosupport/messages?return_records=true" -H "accept: application/hal+json" -H "Content-Type: application/json" -d "{ \"message\": \"test_msg\", \"type\": \"all\"}"
# The response:
201 CREATED
{
  "num_records": 2,
  "records": [
    {
      "index": 4,
      "node": {
        "name": "node1",
        "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/092e0298-f250-11e8-9a05-005056bb6666/4"
        }
      }
    },
    {
      "index": 2,
      "node": {
        "name": "node2",
        "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/e47d2630-f250-11e8-b186-005056bb5cab/2"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/support/autosupport/messages/"
    }
  }
}
```
---
### Invoking an AutoSupport on a single node
The following examples invoke an AutoSupport on a single node in the cluster.
Note that AutoSupport is invoked on all nodes in the cluster if the `node` param is omitted. You can specify the node-name with either `node` or `node.name` parameter. You can also specify UUID of the node with the `node.uuid` parameter.<p/>
By default, the response is an empty object. If `return_records=true` is passed in the request, the response includes information about the node and the index of the invoked AutoSupport message.
```JSON
# The API:
POST /support/autosupport/messages
# The call:
curl -X POST "https://<mgmt-ip>/api/support/autosupport/messages?return_records=true" -H "accept: application/hal+json" -H "Content-Type: application/json" -d "{ \"message\": \"test_msg\", \"type\": \"test\", \"node\":\"node1\"}"
# The response:
201 CREATED
{
  "num_records": 1,
  "records": [
    {
      "index": 8,
      "node": {
        "name": "node1",
        "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/092e0298-f250-11e8-9a05-005056bb6666/8"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/support/autosupport/messages/"
    }
  }
}
# The call:
curl -X POST "https://<mgmt-ip>/api/support/autosupport/messages?return_records=true" -H "accept: application/hal+json" -H "Content-Type: application/json" -d "{ \"message\": \"test_msg\", \"type\": \"test\", \"node.name\":\"node2\"}"
# The response:
201 CREATED
{
  "num_records": 1,
  "records": [
    {
      "index": 4,
      "node": {
        "name": "node2",
        "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/e47d2630-f250-11e8-b186-005056bb5cab/4"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/support/autosupport/messages/"
    }
  }
}
# The call:
curl -X POST "https://<mgmt-ip>/api/support/autosupport/messages?return_records=true" -H "accept: application/hal+json" -H "Content-Type: application/json" -d "{ \"message\": \"test_msg\", \"type\": \"test\", \"node.uuid\":\"092e0298-f250-11e8-9a05-005056bb6666\"}"
# The response:
201 CREATED
{
  "num_records": 1,
  "records": [
    {
      "index": 5,
      "node": {
        "name": "node1",
        "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/092e0298-f250-11e8-9a05-005056bb6666/5"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/support/autosupport/messages/"
    }
  }
}
```
---
### Retrieving AutoSupport messages from all nodes in the cluster
The following example retrieves AutoSupport messages from every node in the cluster.
Note that if the <i>fields=*</i> parameter is not specified, only node, index, and destination fields are returned.
Filters can be added on the fields to limit the results.
```JSON
# The API:
GET /support/autosupport/messages
# The call:
curl -X GET "https://<mgmt-ip>/api/support/autosupport/messages?fields=*&return_timeout=15" -H "accept: application/hal+json"
# The response:
200 OK
{
  "records": [
    {
      "node": {
        "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        "name": "node1",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
          }
        }
      },
      "index": 1,
      "destination": "smtp",
      "subject": "USER_TRIGGERED (TEST:test_msg)",
      "state": "ignore",
      "generated_on": "2019-03-28T10:18:04-04:00",
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/092e0298-f250-11e8-9a05-005056bb6666/1/smtp"
        }
      }
    },
    {
      "node": {
        "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        "name": "node1",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
          }
        }
      },
      "index": 1,
      "destination": "http",
      "subject": "USER_TRIGGERED (TEST:test_msg)",
      "state": "sent_successful",
      "generated_on": "2019-03-28T10:18:04-04:00",
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/092e0298-f250-11e8-9a05-005056bb6666/1/http"
        }
      }
    },
    {
      "node": {
        "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        "name": "node1",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
          }
        }
      },
      "index": 1,
      "destination": "noteto",
      "subject": "USER_TRIGGERED (TEST:test_msg)",
      "state": "ignore",
      "generated_on": "2019-03-28T10:18:04-04:00",
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/092e0298-f250-11e8-9a05-005056bb6666/1/noteto"
        }
      }
    },
    {
      "node": {
        "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
        "name": "node2",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
          }
        }
      },
      "index": 1,
      "destination": "smtp",
      "subject": "USER_TRIGGERED (TEST:test_msg)",
      "state": "ignore",
      "generated_on": "2019-03-28T10:18:06-04:00",
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/e47d2630-f250-11e8-b186-005056bb5cab/1/smtp"
        }
      }
    },
    {
      "node": {
        "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
        "name": "node2",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
          }
        }
      },
      "index": 1,
      "destination": "http",
      "subject": "USER_TRIGGERED (TEST:test_msg)",
      "state": "sent_successful",
      "generated_on": "2019-03-28T10:18:06-04:00",
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/e47d2630-f250-11e8-b186-005056bb5cab/1/http"
        }
      }
    },
    {
      "node": {
        "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
        "name": "node2",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
          }
        }
      },
      "index": 1,
      "destination": "noteto",
      "subject": "USER_TRIGGERED (TEST:test_msg)",
      "state": "ignore",
      "generated_on": "2019-03-28T10:18:06-04:00",
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/e47d2630-f250-11e8-b186-005056bb5cab/1/noteto"
        }
      }
    }
  ],
  "num_records": 6,
  "_links": {
    "self": {
      "href": "/api/support/autosupport/messages?fields=*&return_timeout=15"
    }
  }
}
```
---
### Retrieving AutoSupport messages from a specific node and has 'sent_succesful' state
The following example retrieves AutoSupport messages from a specific node in the cluster.
Note that if the `fields=*` parameter is not specified, only node, index, and destination fields are returned.
This example uses a filter on the `node.name` and `state` fields. Similar to this, filters can be added to any fields in the response.
```JSON
# The API:
GET /support/autosupport/messages
# The call:
curl -X GET "https://<mgmt-ip>/api/support/autosupport/messages?node.name=node1&state=sent_successful&fields=*&return_timeout=15" -H "accept: application/hal+json"
# The response:
200 OK
{
  "records": [
    {
      "node": {
        "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        "name": "node1",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
          }
        }
      },
      "index": 1,
      "destination": "http",
      "subject": "USER_TRIGGERED (TEST:test_msg)",
      "state": "sent_successful",
      "generated_on": "2019-03-28T10:18:04-04:00",
      "_links": {
        "self": {
          "href": "/api/support/autosupport/messages/092e0298-f250-11e8-9a05-005056bb6666/1/http"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/support/autosupport/messages?node.name=node1&state=sent_successful&fields=*&return_timeout=15"
    }
  }
}
```
---
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["AutosupportMessage", "AutosupportMessageSchema"]
__pdoc__ = {
    "AutosupportMessageSchema.resource": False,
    "AutosupportMessageSchema.patchable_fields": False,
    "AutosupportMessageSchema.postable_fields": False,
}


class AutosupportMessageSchema(ResourceSchema):
    """The fields of the AutosupportMessage object"""

    destination = fields.Str(validate=enum_validation(['smtp', 'http', 'noteto', 'retransmit']))
    r""" Destination for the AutoSupport

Valid choices:

* smtp
* http
* noteto
* retransmit """
    error = fields.Nested("AutosupportMessageErrorSchema", unknown=EXCLUDE)
    r""" The error field of the autosupport_message.
 """
    generated_on = fields.DateTime()
    r""" Date and Time of AutoSupport generation in ISO-8601 format

Example: 2019-03-25T21:30:04.000+0000 """
    index = fields.Integer()
    r""" Sequence number of the AutoSupport

Example: 9 """
    message = fields.Str()
    r""" Message included in the AutoSupport subject

Example: invoked_test_autosupport_rest """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the autosupport_message.
 """
    state = fields.Str(validate=enum_validation(['initializing', 'collection_failed', 'collection_in_progress', 'queued', 'transmitting', 'sent_successful', 'ignore', 're_queued', 'transmission_failed', 'ondemand_ignore', 'cancelled']))
    r""" State of AutoSupport delivery

Valid choices:

* initializing
* collection_failed
* collection_in_progress
* queued
* transmitting
* sent_successful
* ignore
* re_queued
* transmission_failed
* ondemand_ignore
* cancelled """
    subject = fields.Str()
    r""" Subject line for the AutoSupport

Example: WEEKLY_LOG """
    type = fields.Str(validate=enum_validation(['test', 'performance', 'all']))
    r""" Type of AutoSupport collection to issue

Valid choices:

* test
* performance
* all """
    uri = fields.Str()
    r""" Alternate destination for the AutoSupport

Example: http://1.2.3.4/delivery_uri """

    @property
    def resource(self):
        return AutosupportMessage

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "error",
            "message",
            "node",
            "type",
            "uri",
        ]

class AutosupportMessage(Resource):
    """Allows interaction with AutosupportMessage objects on the host"""

    _schema = AutosupportMessageSchema
    _path = "/api/support/autosupport/messages"

    # pylint: disable=bad-continuation
    # pylint: disable=missing-docstring
    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ = r"""Retrieves AutoSupport message history from all nodes in the cluster.<p/>
There can be a short delay on invoked AutoSupport messages showing in history, dependent on processing of other AutoSupports in the queue.
### Related ONTAP commands
* `system node autosupport history show`
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)
"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves AutoSupport message history from all nodes in the cluster.<p/>
There can be a short delay on invoked AutoSupport messages showing in history, dependent on processing of other AutoSupports in the queue.
### Related ONTAP commands
* `system node autosupport history show`
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)


    # pylint: disable=missing-docstring
    # pylint: disable=bad-continuation
    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ = r"""Generates and sends an AutoSupport message with the provided input parameters.<p/>
Important note:
* By default, the response is an empty object. If `return_records=true` is passed in the request, the response includes information about the node and the index of the invoked AutoSupport message.
### Recommended optional properties
* `message` - Message included in the AutoSupport subject. Use to identify the generated AutoSupport message.
### Default property values
If not specified in POST, the following default property values are assigned:
* `type` - _all_
* `node.name` or `node.uuid` - Not specifying any of these properties invokes the AutoSupport on all nodes in the cluster.
### Related ONTAP commands
* `system node autosupport invoke`
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)
"""
    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)





