# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
An NVMe subsystem maintains configuration state and namespace access control for a set of NVMe-connected hosts.<br/>
The NVMe subsystem REST API allows you to create, update, delete, and discover NVMe subsystems as well as add and remove NVMe hosts that can access the subsystem and associated namespaces.
## Examples
### Creating an NVMe subsystem
```
# The API:
POST /api/protocols/nvme/subsystems
# The call:
curl -X POST 'https://<mgmt-ip>/api/protocols/nvme/subsystems' -H 'accept: application/hal+json' -d '{ "svm": { "name": "svm1" }, "name": "subsystem1", "os_type": "linux" }'
```
---
### Retrieving all NVMe subsystems
```
# The API:
GET /api/protocols/nvme/subsystems
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/subsystems' -H 'accept: application/hal+json'
# The response:
{
  "records": [
    {
      "svm": {
        "uuid": "a009a9e7-4081-b576-7575-ada21efcaf16",
        "name": "svm1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/a009a9e7-4081-b576-7575-ada21efcaf16"
          }
        }
      },
      "uuid": "acde901a-a379-4a91-9ea6-1b728ed6696f",
      "name": "subsystem1",
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/subsystems"
    }
  }
}
```
---
### Retrieving all NVMe subsystems with OS type _linux_
Note that the `os_type` query parameter is used to perform the query.
<br/>
```
# The API:
GET /api/protocols/nvme/subsystems
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/subsystems?os_type=linux' -H 'accept: application/hal+json'
# The response:
{
  "records": [
    {
      "svm": {
        "uuid": "a009a9e7-4081-b576-7575-ada21efcaf16",
        "name": "svm1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/a009a9e7-4081-b576-7575-ada21efcaf16"
          }
        }
      },
      "uuid": "acde901a-a379-4a91-9ea6-1b728ed6696f",
      "name": "subsystem1",
      "os_type": "linux",
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/subsystems?os_type=linux"
    }
  }
}
```
---
### Retrieving a specific NVMe subsystem
```
# The API:
GET /api/protocols/nvme/subsystems/{uuid}
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f' -H 'accept: application/hal+json'
# The response:
{
  "svm": {
    "uuid": "a009a9e7-4081-b576-7575-ada21efcaf16",
    "name": "svm1",
    "_links": {
      "self": {
        "href": "/api/svm/svms/a009a9e7-4081-b576-7575-ada21efcaf16"
      }
    }
  },
  "uuid": "acde901a-a379-4a91-9ea6-1b728ed6696f",
  "name": "subsystem1",
  "os_type": "linux",
  "target_nqn": "nqn.1992-08.com.netapp:sn.d04594ef915b4c73b642169e72e4c0b1:subsystem.subsystem1",
  "serial_number": "wtJNKNKD-uPLAAAAAAAD",
  "io_queue": {
    "default": {
      "count": 4,
      "depth": 32
    }
  }
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f"
    }
  }
}
```
---
### Retrieving the NVMe namespaces mapped to a specific NVMe subsystem
Note that the `fields` query parameter is used to specify the desired properties.
<br/>
```
# The API:
GET /api/protocols/nvme/subsystems/{uuid}
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f?fields=subsystem_maps' -H 'accept: application/hal+json'
# The response:
{
  "svm": {
    "uuid": "a009a9e7-4081-b576-7575-ada21efcaf16",
    "name": "svm1",
    "_links": {
      "self": {
        "href": "/api/svm/svms/a009a9e7-4081-b576-7575-ada21efcaf16"
      }
    }
  },
  "uuid": "acde901a-a379-4a91-9ea6-1b728ed6696f",
  "name": "subsystem1",
  "subsystem_maps": [
    {
      "anagrpid": "00000001h",
      "namespace": {
        "uuid": "eeaaca23-128d-4a7d-be4a-dc9106705799",
        "name": "/vol/vol1/namespace1"
        "_links": {
          "self": {
            "href": "/api/storage/namespaces/eeaaca23-128d-4a7d-be4a-dc9106705799"
          }
        }
      },
      "nsid": "00000001h"
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/subsystem_maps/acde901a-a379-4a91-9ea6-1b728ed6696f/eeaaca23-128d-4a7d-be4a-dc9106705799"
        }
      }
    },
    {
      "anagrpid": "00000002h",
      "namespace": {
        "uuid": "feaaca23-83a0-4a7d-beda-dc9106705799",
        "name": "/vol/vol1/namespace2"
        "_links": {
          "self": {
            "href": "/api/storage/namespaces/feaaca23-83a0-4a7d-beda-dc9106705799"
          }
        }
      },
      "nsid": "00000002h"
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/subsystem_maps/acde901a-a379-4a91-9ea6-1b728ed6696f/feaaca23-83a0-4a7d-beda-dc9106705799"
        }
      }
    }
  ]
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f"
    }
  }
}
```
---
### Adding a comment about an NVMe subsystem
```
# The API:
PATCH /api/protocols/nvme/subsystems/{uuid}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f' -H 'accept: application/hal+json' -d '{ "comment": "A brief comment about the subsystem" }'
```
---
### Deleting an NVMe subsystem
```
# The API:
DELETE /api/protocols/nvme/subsystems/{uuid}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f' -H 'accept: application/hal+json'
```
### Deleting an NVMe subsystem with mapped NVMe namespaces
Normally, deleting an NVMe subsystem that has mapped NVMe namespaces is not allowed. The deletion can be forced using the `allow_delete_while_mapped` query parameter.
<br/>
```
# The API:
DELETE /api/protocols/nvme/subsystems/{uuid}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f?allow_delete_while_mapped=true' -H 'accept: application/hal+json'
```
### Delete an NVMe subsystem with NVMe subsystem hosts
Normally, deleting an NVMe subsystem with NVMe subsystem hosts is disallowed. The deletion can be forced using the `allow_delete_with_hosts` query parameter.
<br/>
```
# The API:
DELETE /api/protocols/nvme/subsystems/{uuid}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f?allow_delete_with_hosts=true' -H 'accept: application/hal+json'
```
---
## An NVMe Subsystem Host
An NVMe subsystem host is a network host provisioned to an NVMe subsystem to access namespaces mapped to that subsystem.
## Examples
### Adding an NVMe subsystem host to an NVMe subsystem
```
# The API:
POST /protocols/nvme/subsystems/{subsystem.uuid}/hosts
# The call:
curl -X POST 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts' -H 'accept: application/hal+json' -d '{ "nqn": "nqn.1992-01.com.example:subsys1.host1" }'
```
---
### Adding multiple NVMe subsystem hosts to an NVMe subsystem
```
# The API:
POST /protocols/nvme/subsystems/{subsystem.uuid}/hosts
# The call:
curl -X POST 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts' -H 'accept: application/hal+json' -d '{ "records": [ { "nqn": "nqn.1992-01.com.example:subsys1.host2" }, { "nqn": "nqn.1992-01.com.example:subsys1.host3" } ] }'
```
---
### Retrieving all NVMe subsystem hosts for an NVMe subsystem
```
# The API:
GET /protocols/nvme/subsystems/{subsystem.uuid}/hosts
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts' -H 'accept: application/hal+json'
# The response:
{
  "records": [
    {
      "nqn": "nqn.1992-01.com.example:subsys1.host1",
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts/nqn.1992-01.com.example%3Asubsys1.host1"
        }
      }
    },
    {
      "nqn": "nqn.1992-01.com.example:subsys1.host2",
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts/nqn.1992-01.com.example%3Asubsys1.host2"
        }
      }
    },
    {
      "nqn": "nqn.1992-01.com.example:subsys1.host3",
      "_links": {
        "self": {
          "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts/nqn.1992-01.com.example%3Asubsys1.host3"
        }
      }
    }
  ],
  "num_records": 3,
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts"
    }
  }
}
```
---
### Retrieving a specific NVMe subsystem host for an NVMe subsystem
```
# The API:
GET /protocols/nvme/subsystems/{subsystem.uuid}/hosts/{nqn}
# The call:
curl -X GET 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts/nqn.1992-01.com.example:subsys1.host1' -H 'accept: application/hal+json'
# The response:
{
  "subsystem": {
    "uuid": "acde901a-a379-4a91-9ea6-1b728ed6696f",
    "_links": {
      "self": {
        "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f"
      }
    }
  },
  "nqn": "nqn.1992-01.com.example:subsys1.host1",
  "io_queue": {
    "count": 4,
    "depth": 32
  },
  "_links": {
    "self": {
      "href": "/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts/nqn.1992-01.com.example%3Asubsys1.host1"
    }
  }
}
```
---
### Deleting an NVMe subsystem host from an NVMe subsystem
```
# The API:
DELETE /protocols/nvme/subsystems/{subsystem.uuid}/hosts/{nqn}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/protocols/nvme/subsystems/acde901a-a379-4a91-9ea6-1b728ed6696f/hosts/nqn.1992-01.com.example:subsys1.host1' -H 'accept: application/hal+json'
```
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["NvmeSubsystem", "NvmeSubsystemSchema"]
__pdoc__ = {
    "NvmeSubsystemSchema.resource": False,
    "NvmeSubsystemSchema.patchable_fields": False,
    "NvmeSubsystemSchema.postable_fields": False,
}


class NvmeSubsystemSchema(ResourceSchema):
    """The fields of the NvmeSubsystem object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_subsystem.
 """
    comment = fields.Str(validate=len_validation(minimum=0, maximum=255))
    r""" A configurable comment for the NVMe subsystem. Optional in POST and PATCH.
 """
    hosts = fields.List(fields.Nested("NvmeSubsystemHostSchema", unknown=EXCLUDE))
    r""" The hosts field of the nvme_subsystem.
 """
    io_queue = fields.Nested("NvmeSubsystemIoQueueSchema", unknown=EXCLUDE)
    r""" The io_queue field of the nvme_subsystem.
 """
    name = fields.Str(validate=len_validation(minimum=1, maximum=96))
    r""" The name of the NVMe subsystem. Once created, an NVMe subsystem cannot be renamed. Required in POST.


Example: subsystem1 """
    os_type = fields.Str(validate=enum_validation(['hyper_v', 'linux', 'vmware', 'windows', 'xen']))
    r""" The host operating system of the NVMe subsystem's hosts. Required in POST.


Valid choices:

* hyper_v
* linux
* vmware
* windows
* xen """
    serial_number = fields.Str(validate=len_validation(minimum=20, maximum=20))
    r""" The serial number of the NVMe subsystem.


Example: wCVsgFMiuMhVAAAAAAAB """
    subsystem_maps = fields.List(fields.Nested("NvmeSubsystemSubsystemMapsSchema", unknown=EXCLUDE))
    r""" The NVMe namespaces mapped to the NVMe subsystem.<br/>
There is an added cost to retrieving property values for `subsystem_maps`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more. """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the nvme_subsystem.
 """
    target_nqn = fields.Str(validate=len_validation(minimum=1, maximum=223))
    r""" The NVMe qualified name (NQN) used to identify the NVMe storage target.


Example: nqn.1992-01.example.com:string """
    uuid = fields.Str()
    r""" The unique identifier of the NVMe subsystem.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeSubsystem

    @property
    def patchable_fields(self):
        return [
            "comment",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "comment",
            "io_queue",
            "name",
            "os_type",
            "svm",
        ]

class NvmeSubsystem(Resource):
    r""" An NVMe subsystem maintains configuration state and namespace access control for a set of NVMe-connected hosts.
 """

    _schema = NvmeSubsystemSchema
    _path = "/api/protocols/nvme/subsystems"
    @property
    def _keys(self):
        return ["uuid"]

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

    get_collection.__func__.__doc__ = r"""Retrieves NVMe subsystems.
### Related ONTAP commands
* `vserver nvme subsystem host show`
* `vserver nvme subsystem map show`
* `vserver nvme subsystem show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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

    patch_collection.__func__.__doc__ = r"""Updates an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem modify`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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

    delete_collection.__func__.__doc__ = r"""Removes an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem delete`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves NVMe subsystems.
### Related ONTAP commands
* `vserver nvme subsystem host show`
* `vserver nvme subsystem map show`
* `vserver nvme subsystem show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves an NVMe subsystem.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `subsystem_maps.*`
### Related ONTAP commands
* `vserver nvme subsystem host show`
* `vserver nvme subsystem map show`
* `vserver nvme subsystem show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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

    post.__doc__ = r"""Creates an NVMe subsystem.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the NVMe subsystem.
* `name` - Name for NVMe subsystem. Once created, an NVMe subsytem cannot be renamed.
* `os_type` - Operating system of the NVMe subsystem's hosts.
### Related ONTAP commands
* `vserver nvme subsystem create`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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

    patch.__doc__ = r"""Updates an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem modify`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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

    delete.__doc__ = r"""Removes an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem delete`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



