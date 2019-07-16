# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
Manages a specific filter instance.
See the documentation for [/support/ems/filters](#/docs/support/support_ems_filters) for details on the various fields.
## Examples
### Retrieving a specific filter instance
```JSON
# API
GET /api/support/ems/filters/no-info-debug-events
# Response
200 OK
# JSON Body
{
  "name": "no-info-debug-events",
  "rules": [
    {
      "index": 1,
      "type": "include",
      "message_criteria": {
        "name_pattern": "*",
        "severities": "emergency,alert,error,notice",
        "snmp_trap_types": "*",
        "_links": {
          "related": {
            "href": "/api/support/ems/messages?name=*&severity=emergency,alert,error,notice&snmp_trap_type=*"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/ems/filters/no-info-debug-events/rules/1"
        }
      }
    },
    {
      "index": 2,
      "type": "exclude",
      "message_criteria": {
        "name_pattern": "*",
        "severities": "*",
        "snmp_trap_types": "*",
        "_links": {
          "related": {
            "href": "/api/support/ems/messages?name=*&severity=*&snmp_trap_type=*"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/ems/filters/no-info-debug-events/rules/2"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/support/ems/filters/no-info-debug-events"
    }
  }
}
```
### Updating an existing filter with a new rule
```JSON
# API
PATCH /api/support/ems/filters/test-filter
# JSON Body
{
  "rules": [
    {
      "type": "include",
      "message_criteria": {
        "name_pattern": "wafl.*",
        "severities": "error"
      }
    }
  ]
}
# Response
200 OK
```
### Deleting an existing filter
```JSON
# API
DELETE /api/support/ems/filters/test-filter
# Response
200 OK
```
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["EmsFilter", "EmsFilterSchema"]
__pdoc__ = {
    "EmsFilterSchema.resource": False,
    "EmsFilterSchema.patchable_fields": False,
    "EmsFilterSchema.postable_fields": False,
}


class EmsFilterSchema(ResourceSchema):
    """The fields of the EmsFilter object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the ems_filter.
 """
    name = fields.Str()
    r""" Filter name

Example: snmp-traphost """
    rules = fields.List(fields.Nested("EmsFilterRuleSchema", unknown=EXCLUDE))
    r""" Array of event filter rules on which to match.
 """

    @property
    def resource(self):
        return EmsFilter

    @property
    def patchable_fields(self):
        return [
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name",
            "rules",
        ]

class EmsFilter(Resource):
    """Allows interaction with EmsFilter objects on the host"""

    _schema = EmsFilterSchema
    _path = "/api/support/ems/filters"
    @property
    def _keys(self):
        return ["name"]

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

    get_collection.__func__.__doc__ = r"""Retrieves a collection of event filters.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    # pylint: disable=bad-continuation
    # pylint: disable=missing-docstring
    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._patch_collection(body, *args, connection=connection, **kwargs)

    patch_collection.__func__.__doc__ = r"""Updates an event filter.
### Recommended optional properties
* `new_name` - New string that uniquely identifies a filter.
* `rules` - New list of criteria used to match the filter with an event. The existing list is discarded.
### Related ONTAP commands
* `event filter create`
* `event filter delete`
* `event filter rename`
* `event filter rule add`
* `event filter rule delete`
* `event filter rule reorder`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    # pylint: disable=bad-continuation
    # pylint: disable=missing-docstring
    @classmethod
    def delete_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._delete_collection(*args, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ = r"""Deletes an event filter.
### Related ONTAP commands
* `event filter delete`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves a collection of event filters.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves an event filter.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

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

    post.__doc__ = r"""Creates an event filter.
### Required properties
* `name` - String that uniquely identifies the filter.
### Recommended optional properties
* `rules` - List of criteria which is used to match a filter with an event.
### Related ONTAP commands
* `event filter create`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    # pylint: disable=missing-docstring
    # pylint: disable=bad-continuation
    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ = r"""Updates an event filter.
### Recommended optional properties
* `new_name` - New string that uniquely identifies a filter.
* `rules` - New list of criteria used to match the filter with an event. The existing list is discarded.
### Related ONTAP commands
* `event filter create`
* `event filter delete`
* `event filter rename`
* `event filter rule add`
* `event filter rule delete`
* `event filter rule reorder`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    # pylint: disable=missing-docstring
    # pylint: disable=bad-continuation
    def delete(
        self,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._delete(
            poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ = r"""Deletes an event filter.
### Related ONTAP commands
* `event filter delete`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



