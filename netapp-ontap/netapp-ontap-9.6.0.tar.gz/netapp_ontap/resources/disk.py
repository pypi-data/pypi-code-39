# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Retrieving storage disk information
The storage disk GET API retrieves all of the disks in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of disks from the cluster
#### The following example shows the response with a list of disks in the cluster:
---
```
# The API:
/api/storage/disks
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/disks" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "name": "1.24.4",
      "_links": {
        "self": {
          "href": "/api/storage/disks/1.24.4"
        }
      }
    },
    {
      "name": "1.24.3",
      "_links": {
        "self": {
          "href": "/api/storage/disks/1.24.3"
        }
      }
    },
    {
      "name": "1.24.5",
      "_links": {
        "self": {
          "href": "/api/storage/disks/1.24.5"
        }
      }
    },
    {
      "name": "1.24.0",
      "_links": {
        "self": {
          "href": "/api/storage/disks/1.24.0"
        }
      }
    },
    {
      "name": "1.24.2",
      "_links": {
        "self": {
          "href": "/api/storage/disks/1.24.2"
        }
      }
    },
    {
      "name": "1.24.1",
      "_links": {
        "self": {
          "href": "/api/storage/disks/1.24.1"
        }
      }
    }
  ],
  "num_records": 6,
  "_links": {
    "self": {
      "href": "/api/storage/disks"
    }
  }
}
```
---
### 2) Retrieve a specific disk from the cluster
#### The following example shows the response of the requested disk. If there is no disk with the requested name, an error is returned.
---
```
# The API:
/api/storage/disks/{name}
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/disks/1.24.3" -H "accept: application/hal+json"
# The response:
{
  "name": "1.24.3",
  "uid": "50000394:0808AA88:00000000:00000000:00000000:00000000:00000000:00000000:00000000:00000000",
  "serial_number": "EC47PC5021SW",
  "model": "X421_FAL12450A10",
  "vendor": "NETAPP",
  "firmware_version": "NA02",
  "usable_size": 438304768000,
  "rpm": 10000,
  "type": "sas",
  "class": "performance",
  "container_type": "aggregate",
  "pool": "pool0",
  "state": "present",
  "node": {
    "uuid": "3a89ed49-8c6d-11e8-93bc-00a0985a64b6",
    "name": "node-2",
    "_links": {
      "self": {
        "href": "/api/cluster/nodes/3a89ed49-8c6d-11e8-93bc-00a0985a64b6"
      }
    }
  },
  "home_node": {
    "uuid": "3a89ed49-8c6d-11e8-93bc-00a0985a64b6",
    "name": "node-2",
    "_links": {
      "self": {
        "href": "/api/cluster/nodes/3a89ed49-8c6d-11e8-93bc-00a0985a64b6"
      }
    }
  },
  "aggregates": [
    {
      "uuid": "3fd9c345-ba91-4949-a7b1-6e2b898d74e3",
      "name": "node_2_SAS_1",
      "_links": {
        "self": {
          "href": "/api/storage/aggregates/3fd9c345-ba91-4949-a7b1-6e2b898d74e3"
        }
      }
    }
  ],
  "shelf": {
    "uid": "10318311901725526608",
    "_links": {
      "self": {
        "href": "/api/storage/shelves/10318311901725526608"
      }
    }
  },
  "bay": 3,
  "_links": {
    "self": {
      "href": "/api/storage/disks/1.24.3"
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


__all__ = ["Disk", "DiskSchema"]
__pdoc__ = {
    "DiskSchema.resource": False,
    "DiskSchema.patchable_fields": False,
    "DiskSchema.postable_fields": False,
}


class DiskSchema(ResourceSchema):
    """The fields of the Disk object"""

    aggregates = fields.List(fields.Nested("AggregateSchema", unknown=EXCLUDE))
    r""" List of aggregates sharing this disk
 """
    bay = fields.Str()
    r""" Disk shelf bay

Example: 1 """
    class_ = fields.Str(validate=enum_validation(['unknown', 'capacity', 'performance', 'archive', 'solid_state', 'array', 'virtual']))
    r""" Disk class

Valid choices:

* unknown
* capacity
* performance
* archive
* solid_state
* array
* virtual """
    container_type = fields.Str(validate=enum_validation(['aggregate', 'broken', 'foreign', 'labelmaint', 'maintenance', 'shared', 'spare', 'unassigned', 'unknown', 'unsupported', 'remote', 'mediator']))
    r""" Type of overlying disk container

Valid choices:

* aggregate
* broken
* foreign
* labelmaint
* maintenance
* shared
* spare
* unassigned
* unknown
* unsupported
* remote
* mediator """
    dr_node = fields.Nested("DrNodeSchema", unknown=EXCLUDE)
    r""" The dr_node field of the disk.
 """
    drawer = fields.Nested("DiskDrawerSchema", unknown=EXCLUDE)
    r""" The drawer field of the disk.
 """
    firmware_version = fields.Str()
    r""" The firmware_version field of the disk.

Example: NA51 """
    home_node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The home_node field of the disk.
 """
    model = fields.Str()
    r""" The model field of the disk.

Example: X421_HCOBE450A10 """
    name = fields.Str()
    r""" Cluster-wide disk name

Example: 1.0.1 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the disk.
 """
    pool = fields.Str(validate=enum_validation(['pool0', 'pool1', 'failed', 'none']))
    r""" Pool to which disk is assigned

Valid choices:

* pool0
* pool1
* failed
* none """
    rated_life_used_percent = fields.Integer()
    r""" Percentage of rated life used

Example: 10 """
    rpm = fields.Integer()
    r""" Revolutions per minute

Example: 15000 """
    serial_number = fields.Str()
    r""" The serial_number field of the disk.

Example: KHG2VX8R """
    shelf = fields.Nested("ShelfSchema", unknown=EXCLUDE)
    r""" The shelf field of the disk.
 """
    state = fields.Str(validate=enum_validation(['broken', 'copy', 'maintenance', 'partner', 'pending', 'present', 'reconstructing', 'removed', 'spare', 'unfail', 'zeroing']))
    r""" State

Valid choices:

* broken
* copy
* maintenance
* partner
* pending
* present
* reconstructing
* removed
* spare
* unfail
* zeroing """
    type = fields.Str(validate=enum_validation(['ata', 'bsas', 'fcal', 'fsas', 'lun', 'sas', 'msata', 'ssd', 'vmdisk', 'unknown', 'ssd_nvm']))
    r""" Disk interface type

Valid choices:

* ata
* bsas
* fcal
* fsas
* lun
* sas
* msata
* ssd
* vmdisk
* unknown
* ssd_nvm """
    uid = fields.Str()
    r""" The unique identifier for a disk

Example: 002538E5:71B00B2F:00000000:00000000:00000000:00000000:00000000:00000000:00000000:00000000 """
    usable_size = fields.Integer()
    r""" The usable_size field of the disk.

Example: 959934889984 """
    vendor = fields.Str()
    r""" The vendor field of the disk.

Example: NETAPP """

    @property
    def resource(self):
        return Disk

    @property
    def patchable_fields(self):
        return [
            "bay",
            "class_",
            "container_type",
            "firmware_version",
            "model",
            "name",
            "pool",
            "rated_life_used_percent",
            "rpm",
            "serial_number",
            "state",
            "type",
            "uid",
            "usable_size",
            "vendor",
        ]

    @property
    def postable_fields(self):
        return [
            "aggregates",
            "bay",
            "class_",
            "container_type",
            "dr_node",
            "drawer",
            "firmware_version",
            "home_node",
            "model",
            "name",
            "node",
            "pool",
            "rated_life_used_percent",
            "rpm",
            "serial_number",
            "shelf",
            "state",
            "type",
            "uid",
            "usable_size",
            "vendor",
        ]

class Disk(Resource):
    """Allows interaction with Disk objects on the host"""

    _schema = DiskSchema
    _path = "/api/storage/disks"
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

    get_collection.__func__.__doc__ = r"""Retrieves a collection of disks.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves a collection of disks.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves a specific disk.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)






