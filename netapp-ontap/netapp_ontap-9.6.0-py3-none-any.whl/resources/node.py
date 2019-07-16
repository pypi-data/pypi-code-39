# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

# Overview
This API is used to add nodes to a cluster, update node-specific configurations, and retrieve the current node configuration details.
## Adding a node to a cluster
A node can be added to a cluster by issuing a POST /cluster/nodes request to a node currently in the cluster. All nodes must be at the same version to use this API. Mixed version joins are not supported in this release. Properties can be provided as fields in the body of the POST request to configure node-specific settings. On a successful request, POST /cluster/nodes returns a status code of 202 and job information in the body. The /cluster/jobs APIs can be used to track the status of the node add job.
### Fields used for adding a node
Fields used for the /cluster/nodes APIs fall into the following categories
<br/>
### Required node fields
The following field is required for any POST /cluster/nodes request:

* cluster_interface.ip.address
### Optional fields
All of the following fields are used to setup additional cluster-wide configuration:

* name
* location
* records
### Network interface fields
Each node can have a node-specific configuration set in POST /cluster/nodes. If a field is provided in the body of a node, it must be provided for all nodes in the POST body.
The node management interface can be provided for each node if all node management interfaces in the cluster use the same netmask. If the node management interfaces use different netmasks, then configuration of the node management interfaces should be done using the /network/ip/interfaces API.
<br/>
### The records field
Multiple nodes can be added to the cluster in one request by providing an array named "records" with multiple node entries. Each node entry in records must follow the required and optional fields listed previously. When only adding a single node, no records field is needed. See 'Example usecases' for an example of how to use the records field.
## Modifying node configurations
The following fields can be used to modify a node configuration:

* name
* location
<br/>
## Examples
The following examples show how to shutdown/reboot a node and how to update a node configuration.
### Adding a single node with a minimal configuration
---
```
# Body
body =
{
  "cluster_interface": {
    "ip": {
      "address": "1.1.1.1"
    }
  }
}
# Request
curl -X POST "https://<mgmt-ip>/api/cluster/nodes" -d body
```
---
### Adding multiple nodes in the same request
---
```
# Body
body =
{
  "records": [
      {
          "name": "node1",
          "cluster_interface": {
            "ip": {
              "address": "1.1.1.1"
            }
          }
      },
      {
          "name": "node2",
          "cluster_interface": {
            "ip": {
              "address": "2.2.2.2"
            }
          }
      },
  ]
}
# Request
curl -X POST "https://<mgmt-ip>/api/cluster/nodes" -d body
```
---
### Modifying a cluster-wide configuration
---
```
# Body
body =
{
  "name": "renamedNode",
  "location": "newLocation"
}
# Request
curl -X PATCH "https://<mgmt-ip>/api/cluster/nodes" -d body
```
---
### Shutting down a node
---
```
curl -X PATCH "https://<mgmt-ip>/api/cluster/nodes/{uuid}?action=shutdown"
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


__all__ = ["Node", "NodeSchema"]
__pdoc__ = {
    "NodeSchema.resource": False,
    "NodeSchema.patchable_fields": False,
    "NodeSchema.postable_fields": False,
}


class NodeSchema(ResourceSchema):
    """The fields of the Node object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the node.
 """
    cluster_interface = fields.Nested("NodeClusterInterfaceSchema", unknown=EXCLUDE)
    r""" The cluster_interface field of the node.
 """
    cluster_interfaces = fields.List(fields.Nested("IpInterfaceSchema", unknown=EXCLUDE))
    r""" The cluster_interfaces field of the node.
 """
    controller = fields.Nested("NodeControllerSchema", unknown=EXCLUDE)
    r""" The controller field of the node.
 """
    date_ = fields.DateTime()
    r""" Specifies the ISO-8601 format date and time on the node.

Example: 2017-01-25T07:20:13.000+0000 """
    ha = fields.Nested("NodeHaSchema", unknown=EXCLUDE)
    r""" The ha field of the node.
 """
    location = fields.Str()
    r""" The location field of the node.

Example: rack 2 row 5 """
    management_interface = fields.Nested("NodeManagementInterfaceSchema", unknown=EXCLUDE)
    r""" The management_interface field of the node.
 """
    management_interfaces = fields.List(fields.Nested("IpInterfaceSchema", unknown=EXCLUDE))
    r""" The management_interfaces field of the node.
 """
    membership = fields.Str(validate=enum_validation(['available', 'joining', 'member']))
    r""" Possible values:

* <i>available</i> - If a node is available, this means it is detected on the internal cluster network and can be added to the cluster.  Nodes that have a membership of "available" are not returned when a GET request is called when the cluster exists. A query on the "membership" property for <i>available</i> must be provided to scan for nodes on the cluster network. Nodes that have a membership of "available" are returned automatically before a cluster is created.
* <i>joining</i> - Joining nodes are in the process of being added to the cluster. The node may be progressing through the steps to become a member or might have failed. The job to add the node or create the cluster provides details on the current progress of the node.
* <i>member</i> - Nodes that are members have successfully joined the cluster.


Valid choices:

* available
* joining
* member """
    model = fields.Str()
    r""" The model field of the node.

Example: FAS3070 """
    name = fields.Str()
    r""" The name field of the node.

Example: node-01 """
    serial_number = fields.Str()
    r""" The serial_number field of the node.

Example: 4048820-60-9 """
    service_processor = fields.Nested("ServiceProcessorSchema", unknown=EXCLUDE)
    r""" The service_processor field of the node.
 """
    uptime = fields.Integer()
    r""" The total time, in seconds, that the node has been up.

Example: 300536 """
    uuid = fields.Str()
    r""" The uuid field of the node.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """
    version = fields.Nested("VersionSchema", unknown=EXCLUDE)
    r""" The version field of the node.
 """

    @property
    def resource(self):
        return Node

    @property
    def patchable_fields(self):
        return [
            "location",
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "cluster_interface",
            "controller",
            "ha",
            "location",
            "management_interface",
            "name",
            "service_processor",
            "version",
        ]

class Node(Resource):
    r""" Complete node information
 """

    _schema = NodeSchema
    _path = "/api/cluster/nodes"
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

    get_collection.__func__.__doc__ = r"""Retrieves the nodes in the cluster.
### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
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

    patch_collection.__func__.__doc__ = r"""Updates the node information or performs shutdown/reboot actions on a node.
### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)


    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the nodes in the cluster.
### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves information for the node.
### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
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

    post.__doc__ = r"""Adds a node or nodes to the cluster
### Required properties
* `cluster_interface.ip.address`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
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

    patch.__doc__ = r"""Updates the node information or performs shutdown/reboot actions on a node.
### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)




