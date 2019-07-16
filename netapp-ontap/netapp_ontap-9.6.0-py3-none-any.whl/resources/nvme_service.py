# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
A Non-Volatile Memory Express (NVMe) service defines the properties of the NVMe controller target for an SVM. There can be at most one NVMe service for an SVM. An SVM's NVMe service must be created before NVMe host initiators can connect to the SVM.<br/>
The Non-Volatile Memory Express (NVMe) service REST API allows you to create, update, delete, and discover NVMe services for SVMs.
## Examples
### Creating an NVMe service for an SVM
The simpliest way to create an NVMe service is to specify only the SVM, either by name or UUID. By default, the new NVMe service is enabled.<br/>
In this example, the `return_records` query parameter is used to retrieve the new NVMe service object in the REST response.
<br/>
```
# The API:
POST /api/protocols/nvme/services
# The call:
curl -X POST 'https://<mgmt-ip>/api/protocols/nvme/services?return_records=true' -H 'accept: application/hal+json' -d '{ "svm": { "name": "svm1" } }'
# The response:
{
  "num_records": 1,
  "records": [
    {
      "svm": {
        "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
        "name": "svm1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"
          }
        }
      },
      "enabled": true,
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
        }
      }
    }
  ]
}
```
---
### Retrieving the NVMe services for all SVMs in the cluster
```
# The API:
GET /api/protocols/nvme/services
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/services' -H 'accept: application/hal+json'
# The response:
{
  "records": [
    {
      "svm": {
        "uuid": "ab60c350-dc68-11e8-9711-005056bbe408",
        "name": "svm0",
        "_links": {
          "self": {
            "href": "/api/svm/svms/ab60c350-dc68-11e8-9711-005056bbe408"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/services/ab60c350-dc68-11e8-9711-005056bbe408"
        }
      }
    },
    {
      "svm": {
        "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
        "name": "svm1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/services"
    }
  }
}
```
---
### Retrieving details for a specific NVMe service
The NVMe service is identified by the UUID of its SVM.
<br/>
```
# The API:
GET /api/protocols/nvme/services/{svm.uuid}
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341' -H 'accept: application/hal+json'
# The response:
{
  "svm": {
    "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
    "name": "svm1",
    "_links": {
      "self": {
        "href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"
      }
    }
  },
  "enabled": true,
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
    }
  }
}
```
---
### Disabling an NVMe service
Disabling an NVMe service shuts down all active NVMe connections for the SVM and prevents the creation of new NVMe connections.<br/>
The NVMe service to update is identified by the UUID of its SVM.
<br/>
```
# The API:
PATCH /api/protocols/nvme/services/{svm.uuid}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341' -H 'accept: application/hal+json' -d '{ "enabled": "false" }'
```
<br/>
You can retrieve the NVMe service to confirm the change.<br/>
<br/>
```
# The API:
GET /api/protocols/nvme/services/{svm.uuid}
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341' -H 'accept: application/hal+json'
# The response:
{
  "svm": {
    "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
    "name": "svm1",
    "_links": {
      "self": {
        "href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"
      }
    }
  },
  "enabled": false,
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
    }
  }
}
```
---
### Deleting an NVMe service
The NVMe service must be disabled before it can be deleted. In addition, all NVMe interfaces, subsystems, and subsystem maps associated with the SVM must first be deleted.<br/>
The NVMe service to delete is identified by the UUID of its SVM.
<br/>
```
# The API:
DELETE /api/protocols/nvme/services/{svm.uuid}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341' -H 'accept: application/hal+json'
```
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["NvmeService", "NvmeServiceSchema"]
__pdoc__ = {
    "NvmeServiceSchema.resource": False,
    "NvmeServiceSchema.patchable_fields": False,
    "NvmeServiceSchema.postable_fields": False,
}


class NvmeServiceSchema(ResourceSchema):
    """The fields of the NvmeService object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_service.
 """
    enabled = fields.Boolean()
    r""" The administrative state of the NVMe service. The NVMe service can be disabled to block all NVMe connectivity to the SVM.<br/>
This is optional in POST and PATCH. The default setting is _true_ (enabled) in POST. """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the nvme_service.
 """

    @property
    def resource(self):
        return NvmeService

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
        ]

class NvmeService(Resource):
    r""" A Non-Volatile Memory Express (NVMe) service defines the properties of the NVMe controller target for an SVM. There can be at most one NVMe service for an SVM. An SVM's NVMe service must be created before NVMe host initiators can connect to the SVM.<br/>
An NVMe service is identified by the UUID of its SVM. """

    _schema = NvmeServiceSchema
    _path = "/api/protocols/nvme/services"
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

    get_collection.__func__.__doc__ = r"""Retrieves NVMe services.
### Related ONTAP commands
* `vserver nvme show`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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

    patch_collection.__func__.__doc__ = r"""Updates an NVMe service.
### Related ONTAP commands
* `vserver nvme modify`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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

    delete_collection.__func__.__doc__ = r"""Deletes an NVMe service. An NVMe service must be disabled before it can be deleted. In addition, all NVMe interfaces, subsystems, and subsystem maps associated with the SVM must first be deleted.
### Related ONTAP commands
* `vserver nvme delete`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves NVMe services.
### Related ONTAP commands
* `vserver nvme show`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves an NVMe service.
### Related ONTAP commands
* `vserver nvme show`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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

    post.__doc__ = r"""Creates an NVMe service.
### Required properties
* `svm.uuid` or `svm.name` - The existing SVM in which to create the NVMe service.
### Related ONTAP commands
* `vserver nvme create`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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

    patch.__doc__ = r"""Updates an NVMe service.
### Related ONTAP commands
* `vserver nvme modify`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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

    delete.__doc__ = r"""Deletes an NVMe service. An NVMe service must be disabled before it can be deleted. In addition, all NVMe interfaces, subsystems, and subsystem maps associated with the SVM must first be deleted.
### Related ONTAP commands
* `vserver nvme delete`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



