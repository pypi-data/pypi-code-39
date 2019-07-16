# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Retrieving storage aggregate information
The Storage Aggregate GET API retrieves all data aggregates in the cluster. System owned root aggregates are not included in the output.
This API also supports specific queries, in addition to queries on aggregate body properties, which affect the output of the API. The parameters
for these queries are "recommend" and "show_spares". Using the "recommend" query returns the list of aggregates that are
recommended for creation in the cluster. The "show_spares" query returns a response outside of the records body, which includes the groups
of usable spares in the cluster.</br>
The collection GET returns the aggregate identifiers, UUID and name, and the node on which the aggregate resides. The instance GET, by default, returns all of the properties defined in the aggregates object, except advanced properties.
The properties "space.footprint" and "space.block_storage.inactive_user_data" are considered advanced properties and only returned when requested
using the "fields" query parameter.
## Creating storage aggregates
When the POST command is issued with no properties, the system evaluates the cluster attached storage, determines the optimal aggregate layout and configures the aggregates. This layout is completely controlled by the system.
To view the recommended optimal layout rather than creating it, use the GET endpoint, setting the "recommend" query to 'true'.
Alternatively, POST can be used with specific properties to create an aggregate as requested. At a minimum, the
aggregate name, disk count, and the node where it should reside are required if any properties are provided.</br>
When using POST with input properties, three properties are required. These are:
- name
- node.name or node.uuid
- block_storage.primary.disk_count
### Remaining properties are optional
The following properties can be specified in POST:

* name - Name of the aggregate.
* node.name and node.uuid - Node on which the aggregate will be created.
* block_storage.primary.disk_count - Number of disks to be used to create the aggregate.
* block_storage.mirror.enabled - Specifies whether or not the aggregate should be created using SyncMirror.
* block_storage.primary.checksum_style - Checksum style of the disks to be use for the aggregate.
* block_storage.primary.disk_class - Class of disks to be use to for the aggregate.
* block_storage.primary.raid_size - Desired RAID size of the aggregate.
* block_storage.primary.raid_type - Desired RAID type of the aggregate.
* snaplock_type - SnapLock type to use on the aggregate.
## Updating storage aggregates
The PATCH operation is used to modify properties of the aggregate. There are several properties that can be modified on an aggregate. Only one property can be modified for each PATCH request. </br>
The list of patchable properties with a brief description for each is as follows:

* name - This property can be changed to rename the aggregate.
* node.name and node.uuid - Either property can be updated in order to relocate the aggregate to a different node in the cluster.
* block_storage.mirror.enabled - This property can be changed from 'false' to 'true' in order to mirror the aggregate, if the system is capable of doing so.
* block_storage.primary.disk_count - This property can be updated to increase the number of disks in an aggregate.
* block_storage.primary.raid_size - This property can be updated to set the desired RAID size.
* block_storage.primary.raid_type - This property can be updated to set the desired RAID type.
* cloud_storage.tiering_fullness_threshold - This property can be updated to set the desired tiering fullness threshold if using FabricPool.
## Deleting storage aggregates
If volumes exist on an aggregate, they must be deleted or moved before the aggregate can be deleted.
See the /storage/volumes API for details on moving or deleting volumes.
---
## Examples
### Retrieving a list of aggregates from the cluster
The following example shows the response with a list of data aggregates in the cluster:
```
# The API:
/api/storage/aggregates
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/aggregates" -H "accept: application/json"
# The response:
{
  "records": [
    {
      "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
      "name": "test1",
      "node": {
        "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
        "name": "node-1",
      },
    },
    {
      "uuid": "4a7e4139-ca7a-420b-9a11-3f040d2189fd",
      "name": "test4",
      "node": {
        "uuid": "4046dda8-f802-11e8-8f6d-005056bb2030",
        "name": "node-2",
      },
    }
  ],
  "num_records": 2,
}
```
### Retrieving a specific aggregate from the cluster
The following example shows the response of the requested aggregate. If there is no aggregate with the requested UUID, an error is returned.
```
# The API:
/api/storage/aggregates/{uuid}
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/aggregates/870dd9f2-bdfa-4167-b692-57d1cec874d4" -H "accept: application/json"
# The response:
{
  "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
  "name": "test1",
  "node": {
    "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
    "name": "node-1",
  },
  "home_node": {
    "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
    "name": "node-1",
  },
  "space": {
    "block_storage": {
      "size": 235003904,
      "available": 191942656,
      "used": 43061248,
      "full_threshold_percent": 98
    },
    "cloud_storage": {
      "used": 0
    },
    "efficiency": {
      "savings": 1408029,
      "ratio": 6.908119720880661,
      "logical_used": 1646350
    },
    "efficiency_without_snapshots": {
      "savings": 0,
      "ratio": 1,
      "logical_used": 737280
    }
  },
  "state": "online",
  "snaplock_type": "non_snaplock",
  "create_time": "2018-12-04T15:40:38-05:00",
  "data_encryption": {
    "software_encryption_enabled": false,
    "drive_protection_enabled": false
  },
  "block_storage": {
    "primary": {
      "disk_count": 6,
      "disk_class": "solid_state",
      "raid_type": "raid_dp",
      "raid_size": 24,
      "checksum_style": "block"
    },
    "hybrid_cache": {
      "enabled": false
    },
    "mirror": {
      "enabled": false,
      "state": "unmirrored"
    }
  },
  "plexes": [
    {
      "name": "plex0",
    }
  ],
  "cloud_storage": {
    "attach_eligible": false
  },
}
```
### Retrieving a list of aggregates recommended for creation from the cluster
The following example shows the response with a list of recommended data aggregates in the cluster. Note: Each aggregate UUID provided in this response is not guaranteed to be the same UUID for the aggregate if it is created.
```
# The API:
/api/storage/aggregates
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/aggregates?recommend=true&fields=*" -H "accept: application/json"
# The response:
{
  "records": [
    {
      "uuid": "795bf7c2-fa4b-11e8-ba65-005056bbe5c1",
      "name": "node_2_SSD_1",
      "node": {
        "uuid": "4046dda8-f802-11e8-8f6d-005056bb2030",
        "name": "node-2",
      },
      "space": {
        "block_storage": {
          "size": 1116180480
        }
      },
      "block_storage": {
        "primary": {
          "disk_count": 23,
          "disk_class": "solid_state",
          "raid_type": "raid_dp"
        },
        "hybrid_cache": {
          "enabled": false
        },
        "mirror": {
          "enabled": false
        }
      },
    },
    {
      "uuid": "795c0a15-fa4b-11e8-ba65-005056bbe5c1",
      "name": "node_1_SSD_1",
      "node": {
        "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1",
        "name": "node-1",
      },
      "space": {
        "block_storage": {
          "size": 176238592
        }
      },
      "block_storage": {
        "primary": {
          "disk_count": 5,
          "disk_class": "solid_state",
          "raid_type": "raid_dp"
        },
        "hybrid_cache": {
          "enabled": false
        },
        "mirror": {
          "enabled": false
        }
      },
    }
  ],
  "num_records": 2,
}
```
### Updating an aggregate in the cluster
The following example shows the workflow of adding disks to the aggregate.<br>
Step 1: Check the current disk count on the aggregate.
```
# The API:
/api/storage/aggregates
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/aggregates/19425837-f2fa-4a9f-8f01-712f626c983c?fields=block_storage.primary.disk_count" -H "accept: application/json"
# The response:
{
  "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
  "name": "test1",
  "block_storage": {
    "primary": {
      "disk_count": 6
    }
  },
}
```
Step 2: Update the aggregate with the new disk count in 'block_storage.primary.disk_count'. The response to PATCH is a job unless the request is invalid.
```
# The API:
/api/storage/aggregates
# The call:
curl -X PATCH "https://<mgmt-ip>/api/storage/aggregates/19425837-f2fa-4a9f-8f01-712f626c983c" -H "accept: application/hal+json" -d "{\"block_storage\": {\"primary\": {\"disk_count\": 8}}}"
# The response:
{
  "job": {
    "uuid": "c103d15e-730b-11e8-a57f-005056b465d6",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/c103d15e-730b-11e8-a57f-005056b465d6"
      }
    }
  }
}
```
Step 3: Wait for the job to finish, then call GET to see the reflected change.
```
# The API:
/api/storage/aggregates
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/aggregates/19425837-f2fa-4a9f-8f01-712f626c983c?fields=block_storage.primary.disk_count" -H "accept: application/json"
# The response:
{
  "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
  "name": "test1",
  "block_storage": {
    "primary": {
      "disk_count": 8
    }
  },
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


__all__ = ["Aggregate", "AggregateSchema"]
__pdoc__ = {
    "AggregateSchema.resource": False,
    "AggregateSchema.patchable_fields": False,
    "AggregateSchema.postable_fields": False,
}


class AggregateSchema(ResourceSchema):
    """The fields of the Aggregate object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the aggregate.
 """
    block_storage = fields.Nested("AggregateBlockStorageSchema", unknown=EXCLUDE)
    r""" The block_storage field of the aggregate.
 """
    cloud_storage = fields.Nested("AggregateCloudStorageSchema", unknown=EXCLUDE)
    r""" The cloud_storage field of the aggregate.
 """
    create_time = fields.Str()
    r""" Timestamp of aggregate creation

Example: 2018-01-01T16:00:00.000+0000 """
    data_encryption = fields.Nested("AggregateDataEncryptionSchema", unknown=EXCLUDE)
    r""" The data_encryption field of the aggregate.
 """
    dr_home_node = fields.Nested("DrNodeSchema", unknown=EXCLUDE)
    r""" The dr_home_node field of the aggregate.
 """
    home_node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The home_node field of the aggregate.
 """
    name = fields.Str()
    r""" Aggregate name

Example: node1_aggr_1 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the aggregate.
 """
    snaplock_type = fields.Str(validate=enum_validation(['non_snaplock', 'compliance', 'enterprise']))
    r""" SnapLock type

Valid choices:

* non_snaplock
* compliance
* enterprise """
    space = fields.Nested("AggregateSpaceSchema", unknown=EXCLUDE)
    r""" The space field of the aggregate.
 """
    state = fields.Str(validate=enum_validation(['online', 'onlining', 'offline', 'offlining', 'relocating', 'unmounted', 'restricted', 'inconsistent', 'failed', 'unknown']))
    r""" Operational state of the aggregate

Valid choices:

* online
* onlining
* offline
* offlining
* relocating
* unmounted
* restricted
* inconsistent
* failed
* unknown """
    uuid = fields.Str()
    r""" Aggregate UUID
 """

    @property
    def resource(self):
        return Aggregate

    @property
    def patchable_fields(self):
        return [
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "block_storage",
            "cloud_storage",
            "data_encryption",
            "dr_home_node",
            "home_node",
            "name",
            "node",
            "snaplock_type",
            "space",
        ]

class Aggregate(Resource):
    """Allows interaction with Aggregate objects on the host"""

    _schema = AggregateSchema
    _path = "/api/storage/aggregates"
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

    get_collection.__func__.__doc__ = r"""Retrieves the collection of aggregates for the entire cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `space.block_storage.inactive_user_data`
* `space.footprint`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
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

    patch_collection.__func__.__doc__ = r"""Updates the aggregate specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate add-disks`
* `storage aggregate mirror`
* `storage aggregate modify`
* `storage aggregate relocation start`
* `storage aggregate rename`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
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

    delete_collection.__func__.__doc__ = r"""Deletes the aggregate specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate delete`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the collection of aggregates for the entire cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `space.block_storage.inactive_user_data`
* `space.footprint`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the aggregate specified by the UUID. The recommend query cannot be used for this operation.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `space.block_storage.inactive_user_data`
* `space.footprint`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
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

    post.__doc__ = r"""Automatically creates aggregates based on an optimal layout recommended by the system. Alternatively, properties can be provided to create an aggregate according to the requested specification. This request starts a job and returns a link to that job.
### Required properties
Properties are not required for this API. The following properties are only required if you want to specify properties for aggregate creation:
* `name` - Name of the aggregate.
* `node.name` or `node.uuid` - Node on which the aggregate will be created.
* `block_storage.primary.disk_count` - Number of disks to be used to create the aggregate.
### Default values
If not specified in POST, the following default values are assigned. The remaining unspecified properties will receive system dependent default values.
* `block_storage.mirror.enabled` - _false_
* `snaplock_type` - _non_snaplock_
### Related ONTAP commands
* `storage aggregate auto-provision`
* `storage aggregate create`
### Example:
```
POST /api/storage/aggregates {"node": {"name": "node1"}, "name": "test", "block_storage": {"primary": {"disk_count": "10"}}}
```

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
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

    patch.__doc__ = r"""Updates the aggregate specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate add-disks`
* `storage aggregate mirror`
* `storage aggregate modify`
* `storage aggregate relocation start`
* `storage aggregate rename`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
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

    delete.__doc__ = r"""Deletes the aggregate specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate delete`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



