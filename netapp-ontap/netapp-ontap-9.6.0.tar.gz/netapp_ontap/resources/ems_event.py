# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
Queries a live collection of observed events on the system.
## Example
### Querying for the latest event received by EMS
```JSON
# API
GET /api/support/ems/events?fields=message.name&max_records=1
# Response
200 OK
# JSON Body
{
  "records": [
    {
      "node": {
        "name": "node1",
        "uuid": "f087b8e3-99ac-11e8-b5a5-005056bb4ec7",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/f087b8e3-99ac-11e8-b5a5-005056bb4ec7"
          }
        }
      },
      "index": 661,
      "message": {
        "name": "raid.aggr.log.CP.count"
      },
      "_links": {
        "self": {
          "href": "/api/support/ems/events/node1/661"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/support/ems/events?fields=message.name&max_records=1"
    },
  }
}
```
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["EmsEvent", "EmsEventSchema"]
__pdoc__ = {
    "EmsEventSchema.resource": False,
    "EmsEventSchema.patchable_fields": False,
    "EmsEventSchema.postable_fields": False,
}


class EmsEventSchema(ResourceSchema):
    """The fields of the EmsEvent object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the ems_event.
 """
    index = fields.Integer()
    r""" Index of the event. Returned by default.

Example: 1 """
    log_message = fields.Str()
    r""" A formatted text string populated with parameter details. Returned by default.
 """
    message = fields.Nested("EmsEventMessageSchema", unknown=EXCLUDE)
    r""" The message field of the ems_event.
 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the ems_event.
 """
    parameters = fields.List(fields.Nested("EmsEventParameterSchema", unknown=EXCLUDE))
    r""" A list of parameters provided with the EMS event.
 """
    source = fields.Str()
    r""" Source
 """
    time = fields.Str()
    r""" Timestamp of the event. Returned by default.
 """

    @property
    def resource(self):
        return EmsEvent

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "message",
            "node",
            "parameters",
        ]

class EmsEvent(Resource):
    """Allows interaction with EmsEvent objects on the host"""

    _schema = EmsEventSchema
    _path = "/api/support/ems/events"

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

    get_collection.__func__.__doc__ = r"""Retrieves a collection of observed events.
### Related ONTAP commands
* `event log show`

### Learn more
* [`DOC /support/ems/events`](#docs-support-support_ems_events)"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves a collection of observed events.
### Related ONTAP commands
* `event log show`

### Learn more
* [`DOC /support/ems/events`](#docs-support-support_ems_events)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)







