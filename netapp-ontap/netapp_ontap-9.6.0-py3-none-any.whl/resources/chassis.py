# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Retrieving chassis information
The chassis GET API retrieves all of the chassis information in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of chassis from the cluster
#### The following example shows the response with a list of chassis in the cluster:
---
```
# The API:
/api/cluster/chassis
# The call:
curl -X GET "https://<mgmt-ip>/api/cluster/chassis" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "id": "021352005981",
      "_links": {
        "self": {
          "href": "/api/cluster/chassis/021352005981"
        }
      }
    },
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/cluster/chassis"
    }
  }
}
```
---
### 2) Retrieve a specific chassis from the cluster
#### The following example shows the response of the requested chassis. If there is no chassis with the requested id, an error is returned.
---
```
# The API:
/api/cluster/chassis/{id}
# The call:
curl -X GET "https://<mgmt-ip>/api/cluster/chassis/021352005981" -H "accept: application/hal+json"
# The response:
{
  "id": "021352005981",
  "state": "ok",
  "nodes": [
    {
      "name": "node-1",
      "uuid": "6ede364b-c3d0-11e8-a86a-00a098567f31",
      "_links": {
        "self": {
          "href": "/api/cluster/nodes/6ede364b-c3d0-11e8-a86a-00a098567f31"
        }
      }
    }
  ],
  "frus": [
    {
      "id": "PSU2",
      "type": "psu",
      "state": "ok"
    },
    {
      "id": "PSU1",
      "type": "psu",
      "state": "ok"
    },
    {
      "id": "Fan2",
      "type": "fan",
      "state": "ok"
    },
    {
      "id": "Fan3",
      "type": "fan",
      "state": "ok"
    },
    {
      "id": "Fan1",
      "type": "fan",
      "state": "ok"
    }
  ],
  "_links": {
    "self": {
      "href": "/api/cluster/chassis/021352005981"
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


__all__ = ["Chassis", "ChassisSchema"]
__pdoc__ = {
    "ChassisSchema.resource": False,
    "ChassisSchema.patchable_fields": False,
    "ChassisSchema.postable_fields": False,
}


class ChassisSchema(ResourceSchema):
    """The fields of the Chassis object"""

    frus = fields.List(fields.Nested("ChassisFrusSchema", unknown=EXCLUDE))
    r""" List of frus in chassis
 """
    id = fields.Str()
    r""" The id field of the chassis.

Example: 2.1352005981E10 """
    nodes = fields.List(fields.Nested("NodeSchema", unknown=EXCLUDE))
    r""" List of nodes in chassis
 """
    shelves = fields.List(fields.Nested("ShelfSchema", unknown=EXCLUDE))
    r""" List of shelves in chassis
 """
    state = fields.Str(validate=enum_validation(['ok', 'error']))
    r""" The state field of the chassis.

Valid choices:

* ok
* error """

    @property
    def resource(self):
        return Chassis

    @property
    def patchable_fields(self):
        return [
            "id",
            "state",
        ]

    @property
    def postable_fields(self):
        return [
            "frus",
            "id",
            "nodes",
            "shelves",
            "state",
        ]

class Chassis(Resource):
    """Allows interaction with Chassis objects on the host"""

    _schema = ChassisSchema
    _path = "/api/cluster/chassis"
    @property
    def _keys(self):
        return ["id"]

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

    get_collection.__func__.__doc__ = r"""Retrieves a collection of chassis.
### Related ONTAP commands
* `system chassis show`
* `system chassis fru show`
### Learn more
* [`DOC /cluster/chassis`](#docs-cluster-cluster_chassis)
"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves a collection of chassis.
### Related ONTAP commands
* `system chassis show`
* `system chassis fru show`
### Learn more
* [`DOC /cluster/chassis`](#docs-cluster-cluster_chassis)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves a specific chassis.
### Related ONTAP commands
* `system chassis show`
* `system chassis fru show`
### Learn more
* [`DOC /cluster/chassis`](#docs-cluster-cluster_chassis)
"""
    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)






