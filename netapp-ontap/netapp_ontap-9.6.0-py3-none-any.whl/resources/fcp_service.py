# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
A Fibre Channel Protocol (FC Protocol) service defines the properties of the FC Protocol target for an SVM. There can be at most one FC Protocol service for an SVM. An SVM FC Protocol service must be created before FC Protocol initiators can log in to the SVM.<br/>
The FC Protocol service REST API allows you to create, update, delete, and discover FC services for SVMs.
## Examples
### Creating an FC Protocol service for an SVM
The simplest way to create an FC Protocol service is to specify only the SVM, either by name or UUID. By default, the new FC Protocol service is enabled.<br/>
In this example, the `return_records` query parameter is used to retrieve the new FC Protocol service object in the REST response.
<br/>
```
# The API:
POST /api/protocols/san/fcp/services
# The call:
curl -X POST 'https://<mgmt-ip>/api/protocols/san/fcp/services?return_records=true' -H 'accept: application/hal+json' -d '{ "svm": { "name": "svm1" } }'
# The response:
{
  "num_records": 1,
  "records": [
    {
      "svm": {
        "uuid": "5c659d90-c01a-11e8-88ed-005056bbb24b",
        "name": "svm1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/5c659d90-c01a-11e8-88ed-005056bbb24b"
          }
        }
      },
      "enabled": true,
      "target": {
        "name": "20:00:00:50:56:bb:b2:4b"
      },
      "_links": {
        "self": {
          "href": "/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b"
        }
      }
    }
  ]
}
```
---
### Retrieving the FC Protocol services for all SVMs in the cluster
```
# The API:
GET /api/protocols/san/fcp/services
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/san/fcp/services' -H 'accept: application/hal+json'
# The response:
{
  "records": [
    {
      "svm": {
        "uuid": "5c659d90-c01a-11e8-88ed-005056bbb24b",
        "name": "svm1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/5c659d90-c01a-11e8-88ed-005056bbb24b"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b"
        }
      }
    },
    {
      "svm": {
        "uuid": "6011f874-c01a-11e8-88ed-005056bbb24b",
        "name": "svm2",
        "_links": {
          "self": {
            "href": "/api/svm/svms/6011f874-c01a-11e8-88ed-005056bbb24b"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/protocols/san/fcp/services/6011f874-c01a-11e8-88ed-005056bbb24b"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/protocols/san/fcp/services"
    }
  }
}
```
---
### Retrieving details for a specific FC Protocol service
The FC Protocol service is identified by the UUID of its SVM.
<br/>
```
# The API:
GET /api/protocols/san/fcp/services/{svm.uuid}
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b' -H 'accept: application/hal+json'
# The response:
{
  "svm": {
    "uuid": "5c659d90-c01a-11e8-88ed-005056bbb24b",
    "name": "svm1",
    "_links": {
      "self": {
        "href": "/api/svm/svms/5c659d90-c01a-11e8-88ed-005056bbb24b"
      }
    }
  },
  "enabled": true,
  "target": {
    "name": "20:00:00:50:56:bb:b2:4b"
  },
  "_links": {
    "self": {
      "href": "/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b"
    }
  }
}
```
---
### Disabling an FC Protocol service
Disabling an FC Protocol service shuts down all active FC Protocol logins for the SVM and prevents new FC Protocol logins.<br/>
The FC Protocol service to update is identified by the UUID of its SVM.
<br/>
```
# The API:
PATCH /api/protocols/san/fcp/services/{svm.uuid}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b' -H 'accept: application/hal+json' -d '{ "enabled": "false" }'
```
<br/>
You can retrieve the FC Protocol service to confirm the change.<br/>
In this example, the `fields` query parameter is used to limit the response to the `enabled` property and FC Protocol service identifiers.
<br/>
```
# The API:
GET /api/protocols/san/fcp/services/{svm.uuid}
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b?fields=enabled' -H 'accept: application/hal+json'
# The response:
{
  "svm": {
    "uuid": "5c659d90-c01a-11e8-88ed-005056bbb24b",
    "name": "svm1",
    "_links": {
      "self": {
        "href": "/api/svm/svms/5c659d90-c01a-11e8-88ed-005056bbb24b"
      }
    }
  },
  "enabled": false,
  "_links": {
    "self": {
      "href": "/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b"
    }
  }
}
```
---
### Deleting an FC Protocol service
The FC Protocol service must be disabled before it can be deleted.<br/>
The FC Protocol service to delete is identified by the UUID of its SVM.
<br/>
```
# The API:
DELETE /api/protocols/san/fcp/services/{svm.uuid}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/protocols/san/fcp/services/5c659d90-c01a-11e8-88ed-005056bbb24b' -H 'accept: application/hal+json'
```
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["FcpService", "FcpServiceSchema"]
__pdoc__ = {
    "FcpServiceSchema.resource": False,
    "FcpServiceSchema.patchable_fields": False,
    "FcpServiceSchema.postable_fields": False,
}


class FcpServiceSchema(ResourceSchema):
    """The fields of the FcpService object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the fcp_service.
 """
    enabled = fields.Boolean()
    r""" The administrative state of the FC Protocol service. The FC Protocol service can be disabled to block all FC Protocol connectivity to the SVM.<br/>
This is optional in POST and PATCH. The default setting is _true_ (enabled) in POST. """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the fcp_service.
 """
    target = fields.Nested("FcpServiceTargetSchema", unknown=EXCLUDE)
    r""" The target field of the fcp_service.
 """

    @property
    def resource(self):
        return FcpService

    @property
    def patchable_fields(self):
        return [
            "enabled",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "enabled",
            "svm",
            "target",
        ]

class FcpService(Resource):
    r""" A Fibre Channel (FC) Protocol service defines the properties of the FC Protocol target for an SVM. There can be at most one FC Protocol service for an SVM. An SVM's FC Protocol service must be created before FC Protocol initiators can login to the SVM.<br/>
A FC Protocol service is identified by the UUID of its SVM. """

    _schema = FcpServiceSchema
    _path = "/api/protocols/san/fcp/services"
    @property
    def _keys(self):
        return ["svm.uuid"]

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

    get_collection.__func__.__doc__ = r"""Retrieves FC Protocol services.
### Related ONTAP commands
* `vserver fcp show`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
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

    patch_collection.__func__.__doc__ = r"""Updates an FC Protocol service.
### Related ONTAP commands
* `vserver fcp modify`
* `vserver fcp start`
* `vserver fcp stop`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
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

    delete_collection.__func__.__doc__ = r"""Deletes an FC Protocol service. An FC Protocol service must be disabled before it can be deleted.
### Related ONTAP commands
* `vserver fcp delete`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves FC Protocol services.
### Related ONTAP commands
* `vserver fcp show`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves a Fibre Channel Protocol service.
### Related ONTAP commands
* `vserver fcp show`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
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

    post.__doc__ = r"""Creates an FC Protocol service.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the FC service.
### Related ONTAP commands
* `vserver fcp create`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
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

    patch.__doc__ = r"""Updates an FC Protocol service.
### Related ONTAP commands
* `vserver fcp modify`
* `vserver fcp start`
* `vserver fcp stop`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
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

    delete.__doc__ = r"""Deletes an FC Protocol service. An FC Protocol service must be disabled before it can be deleted.
### Related ONTAP commands
* `vserver fcp delete`
### Learn more
* [`DOC /protocols/san/fcp/services`](#docs-SAN-protocols_san_fcp_services)
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



