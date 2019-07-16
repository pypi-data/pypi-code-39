# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

# Overview
This API is used to create a cluster, update cluster-wide configurations, and retrieve the current configuration details.
## Creating a cluster
You can create a new cluster by issuing a POST request to /cluster. Parameters are provided in the body of the POST request to configure cluster-wide settings and add nodes during the cluster setup.
### Fields used for creating a cluster
The fields used for the cluster APIs fall into the following categories:
### Required cluster-wide configuration
The following fields are always required for any POST /cluster request:

* name
* password
### Optional cluster-wide configuration
The following fields are used to setup additional cluster-wide configuration:

* location
* contact
* dns_domains
* name_servers
* ntp_servers
* license
* configuration_backup
* management_interface
* nodes
### Nodes field
The nodes field specifies the nodes to join to the cluster. All nodes must be at the same version to use this API. If no nodes are specified, the cluster is configured with one node added. The node added is the node to which the REST request is issued. If one node is specified, the "node.cluster_interface.ip.address" field must not be used. If multiple nodes are specified, the node to which the REST request is issued must be provided in addition to the remote nodes, and the "node.cluster_interface.ip.address" field is required for each node to identify them. All other node fields are optional in all cases. If a field is provided for one node, it must be provided for all nodes.
### Node networking fields
The cluster management interface and each node management interface use the cluster management interface netmask and gateway. For advanced configurations where the cluster and node management interfaces are on different subnets, the /network/ip/interface APIs must be used to configure network interfaces after setup is complete.
The management interfaces are used to communicate with the name servers and NTP servers. The address family of the name servers and NTP servers must match the management interfaces address family.
### Single node cluster field
When the "single_node_cluster" field is set to true, the cluster is created in single node cluster mode. A node field for this node can be provided for node-specific configuration and the "node.cluster_interface.ip.address" field must not be used. Storage failover is configured to non-HA mode, and ports used for cluster ports are moved to the default IPspace. This might cause the node to reboot during setup. While a node reboots, the RESTful interface might not be available. See 'Connection failures during cluster create' for more information.
## Performance monitoring
Performance of the cluster can be monitored by the `metric.*` and `statistics.*` fields. These show the performance of the cluster in terms of IOPS, latency and throughput. The `metric.*` fields denote an average whereas `statistics.*` fields denote a real-time monotonically increasing value aggregated across all nodes.
## Monitoring cluster create status
### Errors before the job starts
Configuration in the POST /cluster request is validated before the cluster create job starts. If an invalid configuration is found, an HTTP error code in the 4xx range is returned. No cluster create job is started.
### Polling on the job
After a successful POST /cluster has been issued, an HTTP error code of 202 is returned along with a job UUID and link in the body of the response. The cluster create job continues asynchronously and can be monitored with the job UUID using the /cluster/jobs API. The "message" field in the response of GET /cluster/jobs/{uuid} shows the current step in the job and the "state" field shows the overall state of the job.
### Errors during the job
If a failure occurs during the cluster create job, the job body provides details of the error along with error code fields. See the error table in the 'Responses' of the POST /cluster documentation for common error codes and descriptions.
### Re-running POST /cluster
The POST /cluster command can be re-run if errors occur. When re-running the request, the same body and query parameters must be used. The value of any field in the original body or query can be changed, but the fields that were provided cannot be changed. For example, an initial request might have a body section as follows:
<br />
---
```
body =
{
  "name": "clusCreateRerun",
  "password": "openSesame",
  "nodes": [
    {
      "cluster_interface": {
        "ip": {
          "address": "1.1.1.1"
        }
      }
    },
    {
      "cluster_interface": {
        "ip": {
          "address": "2.2.2.2"
        }
      }
    }
  ]
}
```
---
A re-run request updates the body details to:
<br />
---
```
body =
{
  "name": "clusCreateRerun",
  "password": "openSesame",
  "nodes": [
    {
      "cluster_interface": {
        "ip": {
          "address": "3.3.3.3"
        }
      }
    },
    {
      "cluster_interface": {
        "ip": {
          "address": "4.4.4.4"
        }
      }
    }
  ]
}
```
---
A re-run request with the following body details is invalid:
<br />
---
```
body =
{
  "name": "clusCreateRerun",
  "password": "openSesame",
  "nodes": [
    {
      "cluster_interface": {
        "ip": {
          "address": "3.3.3.3"
        }
      }
    }
  ]
}
```
---
Also, note that the password might already be configured. If a password is already configured and a new password is provided, this request overwrites the existing password. If a password is already configured either by another interface or by a previous POST to /cluster, any future REST requests must be authenticated with that password. If POST to /cluster with the default return_timeout of 0 returns an error, then the password was not changed.
### Connection failures during cluster create
There are two cases where a request to poll the job status might fail during the cluster create job. In these cases, programmatic use of the RESTful interface should be resilient to these connection failures.
1. When the "single_node_cluster" flag is set to true, the node might reboot. During this time, the RESTful interface might refuse connections, return errors on GET, or connection timeouts might occur. Any programmatic use of the RESTful interface during reboots must consider these effects while polling a cluster create job.
2. The "mgmt_auto" LIF is removed during the cluster create job. A POST /cluster request might be issued on the "mgmt_auto" LIF. However, requests to poll the job status might fail during cluster create when the "mgmt_auto" LIF is removed. The "mgmt_auto" LIF is only removed if a cluster management interface is provided as an argument to POST /cluster, and only after the cluster management interface is created. Programmatic use of the POST /cluster API on the "mgmt_auto" LIF should be configured to dynamically switch to polling the job on the cluster management LIF.
## Modifying cluster configurations
The following fields can be used to modify a cluster-wide configuration:

* name
* location
* contact
* dns_domains
* name_servers
## Examples
### A minimal configuration of a 2-node setup
---
```
# Body
body =
{
  "name": "clusCreateExample1",
  "password": "openSesame",
  "nodes": [
    {
      "cluster_interface": {
        "ip": {
          "address": "1.1.1.1"
        }
      }
    },
    {
      "cluster_interface": {
        "ip": {
          "address": "2.2.2.2"
        }
      }
    }
  ]
}
# Request
curl -X POST "https://<mgmt-ip>/api/cluster" -d body
```
---
### A single node setup with additional node configuration
---
```
# Body
body =
{
  "name": "clusCreateExample2",
  "password": "openSesame",
  "nodes": [
    {
      "name": "singleNode",
      "location": "Sunnyvale"
    }
  ]
}
# Request
curl -X POST "https://<mgmt-ip>/api/cluster?single_node_cluster=true" -d body
```
---
### Modifying a cluster-wide configuration
---
```
# Body
body =
{
  "contact": "it@company.com"
}
# Request
curl -X PATCH "https://<mgmt-ip>/api/cluster" -d body
```
---
## A detailed example of a cluster "create" operation
The following is an example of how a cluster can be created using the cluster APIs.  This example shows the creation of a two node cluster and uses information from the nodes themselves combined with user supplied information to configure the cluster.
### 1) Preparing for setup
Before the REST APIs can be issued to create the cluster, the cluster must be wired up and powered on. The network connections between the nodes for the cluster network, as well as the connections to the management network, must be completed.  Once the nodes are powered up, the nodes automatically configure interfaces on the platform's default cluster ports to allow the nodes to discover each other during setup and expansion workflows. You must configure a management interface on one node or use the mgmt_auto LIF, which is assigned an IP address using DHCP, to start using the REST APIs.  By making a console connection to a node, the cluster setup wizard guides you through the configuration of the initial node managment interface to which the REST calls can be sent.  Once this step is completed, exit the wizard by typing "exit". You can then issue REST API requests.
1.  Wire and power up the nodes.
2.  Make a console connection to one node to access the cluster setup wizard.
3.  Enter node management interface information to enable REST API requests to be sent to the node.
---
```
Welcome to the cluster setup wizard.
You can enter the following commands at any time:
  "help" or "?" - if you want to have a question clarified,
  "back" - if you want to change previously answered questions, and
  "exit" or "quit" - if you want to quit the cluster setup wizard.
  Any changes you made before quitting will be saved.
  You can return to cluster setup at any time by typing "cluster setup".
  To accept a default or omit a question, do not enter a value.
  This system will send event messages and periodic reports to NetApp Technical
  Support. To disable this feature, enter
  autosupport modify -support disable
  within 24 hours.
  Enabling AutoSupport can significantly speed problem determination and
  resolution should a problem occur on your system.
  For further information on AutoSupport, see:
    http://support.netapp.com/autosupport/
    Type yes to confirm and continue {yes}: yes
    Enter the node management interface port [e0c]:
      Enter the node management interface IP address: 10.224.82.249
      Enter the node management interface netmask: 255.255.192.0
      Enter the node management interface default gateway: 10.224.64.1
      A node management interface on port e0c with IP address 10.224.82.249 has been created.
      Use your web browser to complete cluster setup by accessing
      https://10.224.82.249
      Otherwise, press Enter to complete cluster setup using the command line
      interface: exit
      Exiting the cluster setup wizard. Any changes you made have been saved.
      The cluster administrator's account (username "admin") password is set to the system default.
      Warning: You have exited the cluster setup wizard before completing all
      of the tasks. The cluster is not configured. You can complete cluster setup by typing
      "cluster setup" in the command line interface.
```
---
### 2) Discovering the nodes
Issuing a GET /api/cluster/nodes request when the nodes are not in a cluster, the API returns a list of nodes that were discovered on the cluster network.  Information returned include the node's serial number, model, software version, UUID, and cluster interface address.  The number of nodes returned should be the same as the number of nodes expected to be in the cluster.  If too many nodes are discovered, remove those nodes that should not be part of the cluster.  If not enough nodes are discovered, ensure all the nodes are powered up, that the connections to the cluster network are complete, and retry the command.
<br />
---
```
# The API:
/api/cluster/nodes
# The call:
curl -X GET "https://<mgmt-ip>/api/cluster/nodes?fields=*" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "uuid": "60277d87-19e4-11e9-ba25-005056bb6eee",
      "name": "Computer.local",
      "serial_number": "4136233-26-3",
      "model": "FAS9000",
      "version": {
        "full": "NetApp Release 9.6.0: Wed Jan 16 18:20:57 UTC 2019",
        "generation": 9,
        "major": 6,
        "minor": 0
      },
      "membership": "available",
      "cluster_interfaces": [
        {
          "ip": {
            "address": "169.254.245.113"
          }
        }
      ],
      "_links": {
        "self": {
          "href": "/api/cluster/nodes/60277d87-19e4-11e9-ba25-005056bb6eee"
        }
      }
    },
    {
      "uuid": "8071ba1b-19e3-11e9-b003-005056bb096a",
      "name": "Computer-6.local",
      "serial_number": "4136233-26-2",
      "model": "FAS9000",
      "version": {
        "full": "NetApp Release 9.6.0: Wed Jan 16 18:20:57 UTC 2019",
        "generation": 9,
        "major": 6,
        "minor": 0
      },
      "membership": "available",
      "cluster_interfaces": [
        {
          "ip": {
            "address": "169.254.217.95"
          }
        }
      ],
      "_links": {
        "self": {
          "href": "/api/cluster/nodes/8071ba1b-19e3-11e9-b003-005056bb096a"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/cluster/nodes?fields=*"
    }
  }
}
```
---
### 3) Creating the cluster
Once the node information is available, including each node's cluster interface address, the information for creating the cluster can be assembled.  You must provide the cluster name and the password for the admin account.  The rest of the information is optional and can be configured later using other APIs.  Each node to be included in the cluster must have the cluster interface address provided so that it can be connected to while adding it to the cluster.  In addition to the cluster interface address, the optional node name, location, and management interface information can be supplied.  If node names are not provided, nodes are named based on the cluster name.  The nodes' managment interface netmask and gateway values are omitted and must be the same as the cluster management interface's netmask and gateway.
<br />
---
```
# The API:
/api/cluster
# The call:
curl -X POST "https://<mgmt-ip>/api/cluster" -H "accept: application/hal+json" -H "accept: application/hal+json" -d '{"name":"cluster1","location":"datacenter1","contact":"me","dns_domains":["example.com"],"name_servers":["10.224.223.130","10.224.223.131","10.224.223.132"],"ntp_servers":["time.nist.gov"],"management_interface":{"ip":{"address":"10.224.82.25","netmask":"255.255.192.0","gateway":"10.224.64.1"}},"password":"mypassword","license":{"keys":["AMEPOSOIKLKGEEEEDGNDEKSJDE"]},"nodes":[{"cluster_interface":{"ip":{"address":"169.254.245.113"}},"name":"node1","management_interface":{"ip":{"address":"10.224.82.29"}}},{"cluster_interface":{"ip":{"address":"169.254.217.95"}},"name":"node2","management_interface":{"ip":{"address":"10.224.82.31"}}}]}'
# The response:
{
  "job": {
    "uuid": "b5bc07e2-19e9-11e9-a751-005056bbd95f",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/b5bc07e2-19e9-11e9-a751-005056bbd95f"
      }
    }
  }
}
```
---
### 4) Monitoring the progress of cluster creation
To monitor the progress of the cluster create operation, the job link returned should be polled until the state value is no longer "runnning" or "queued".
<br />
---
```
# The API:
/api/cluster/jobs/b5bc07e2-19e9-11e9-a751-005056bbd95f
# The call:
curl -X GET "https://<mgmt-ip>/api/cluster/jobs/b5bc07e2-1e9-11e9-a751-005056bbd95f" -H "accept: application/hal+json"
# The response:
{
  "uuid": "b5bc07e2-19e9-11e9-a751-005056bbd95f",
  "description": "POST /api/cluster",
  "state": "success",
  "message": "success",
  "code": 0,
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/b5bc07e2-19e9-11e9-a751-005056bbd95f"
    }
  }
}
```
---
### 5) Verifying the cluster information
Once the cluster is created, the information applied can be verified using a number of APIs. Most of the information provided can be retrieved using the /api/cluster and /api/cluster/nodes APIs. In addition, the network interface and route information can be viewed using the /api/network APIs. The following example details how to retrieve the cluster information:
<br />
---
```
# The API:
/api/cluster
# The call:
curl -X GET "https://<mgmt-ip>/api/cluster" -H "accept: application/hal+json"
# The response:
{
  "name": "cluster1",
  "uuid": "93d05f83-7d80-482d-b59c-a6661d272a47",
  "location": "datacenter1",
  "contact": "me",
  "version": {
    "full": "NetApp Release 9.6.0: Wed Jan 16 18:20:57 UTC 2019",
    "generation": 9,
    "major": 6,
    "minor": 0
  },
  "dns_domains": [
    "example.com"
  ],
  "name_servers": [
    "10.224.223.130",
    "10.224.223.131",
    "10.224.223.132"
  ],
  "ntp_servers": [
    "time.nist.gov"
  ],
  "management_interfaces": [
    {
      "uuid": "c661725a-19e9-11e9-a751-005056bbd95f",
      "name": "cluster_mgmt",
      "ip": {
        "address": "10.224.82.25"
      }
      "_links": {
        "self": {
          "href": "/api/network/ip/interfaces/c661725a-19e9-11e9-a751-005056bbd95f"
        }
      }
    }
  ],
  "metric": {
    "timestamp": "2019-04-09T06:33:30Z",
    "duration": "PT15S",
    "status": "ok",
    "latency": {
       "other": 0,
       "total": 525,
       "read": 525,
       "write": 0
    },
    "iops": {
      "read": 200,
      "write": 0,
      "other": 0,
      "total": 200
    },
    "throughput": {
      "read": 820838,
      "write": 0,
      "other": 0,
      "total": 820838
    }
  },
  "statistics": {
    "timestamp": "2019-04-09T06:33:50Z",
    "status": "ok",
    "latency_raw": {
      "other": 38928,
      "total": 3331918704,
      "read": 3331879776,
      "write": 0
    },
    "iops_raw": {
      "read": 6188132,
      "write": 0,
      "other": 5,
      "total": 6188137
    },
    "throughput_raw": {
      "read": 25346587876,
      "write": 0,
      "other": 0,
      "total": 25346587876
    }
  },
  "_links": {
    "self": {
      "href": "/api/cluster"
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


__all__ = ["Cluster", "ClusterSchema"]
__pdoc__ = {
    "ClusterSchema.resource": False,
    "ClusterSchema.patchable_fields": False,
    "ClusterSchema.postable_fields": False,
}


class ClusterSchema(ResourceSchema):
    """The fields of the Cluster object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the cluster.
 """
    configuration_backup = fields.Nested("ConfigurationBackupSchema", unknown=EXCLUDE)
    r""" The configuration_backup field of the cluster.
 """
    contact = fields.Str()
    r""" The contact field of the cluster.

Example: support@company.com """
    dns_domains = fields.List(fields.Str)
    r""" A list of DNS domains.
Domain names have the following requirements:

* The name must contain only the following characters: A through Z, a through z, 0 through 9, ".", "-" or "_".
* The first character of each label, delimited by ".", must be one of the following characters: A through Z or a through z or 0 through 9.
* The last character of each label, delimited by ".", must be one of the following characters: A through Z, a through z, or 0 through 9.
* The top level domain must contain only the following characters: A through Z, a through z.
* The system reserves the following names:"all", "local", and "localhost".


Example: ["example.com","example2.example3.com"] """
    license = fields.Nested("LicenseKeysSchema", unknown=EXCLUDE)
    r""" The license field of the cluster.
 """
    location = fields.Str()
    r""" The location field of the cluster.

Example: building 1 """
    management_interface = fields.Nested("ClusterManagementInterfaceSchema", unknown=EXCLUDE)
    r""" The management_interface field of the cluster.
 """
    management_interfaces = fields.List(fields.Nested("IpInterfaceSchema", unknown=EXCLUDE))
    r""" The management_interfaces field of the cluster.
 """
    metric = fields.Nested("PerformanceMetricSchema", unknown=EXCLUDE)
    r""" The metric field of the cluster.
 """
    name = fields.Str()
    r""" The name field of the cluster.

Example: cluster1 """
    name_servers = fields.List(fields.Str)
    r""" The list of IP addresses of the DNS servers. Addresses can be either
IPv4 or IPv6 addresses.


Example: ["10.224.65.20","2001:db08:a0b:12f0::1"] """
    nodes = fields.List(fields.Nested("NodeSchema", unknown=EXCLUDE))
    r""" The nodes field of the cluster.
 """
    ntp_servers = fields.List(fields.Str)
    r""" Host name, IPv4 address, or IPv6 address for the external NTP time servers.

Example: ["time.nist.gov","10.98.19.20","2610:20:6F15:15::27"] """
    password = fields.Str()
    r""" Initial admin password used to create the cluster.

Example: mypassword """
    statistics = fields.Nested("PerformanceMetricRawSchema", unknown=EXCLUDE)
    r""" The statistics field of the cluster.
 """
    uuid = fields.Str()
    r""" The uuid field of the cluster.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """
    version = fields.Nested("VersionSchema", unknown=EXCLUDE)
    r""" The version field of the cluster.
 """

    @property
    def resource(self):
        return Cluster

    @property
    def patchable_fields(self):
        return [
            "contact",
            "dns_domains",
            "location",
            "name",
            "name_servers",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "configuration_backup",
            "contact",
            "dns_domains",
            "license",
            "location",
            "management_interface",
            "metric",
            "name",
            "name_servers",
            "nodes",
            "ntp_servers",
            "password",
            "statistics",
            "version",
        ]

class Cluster(Resource):
    r""" Complete cluster information
 """

    _schema = ClusterSchema
    _path = "/api/cluster"





    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the cluster configuration.
### Learn more
* [`DOC /cluster`](#docs-cluster-cluster)"""
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

    post.__doc__ = r"""Sets up a cluster.
### Required properties
* `name`
* `password`
### Recommended optional properties
* `location`
* `contact`
* `dns_domains`
* `name_servers`
* `ntp_servers`
* `license`
* `configuration_backup`
* `management_interface`
* `nodes`
### Learn more
* [`DOC /cluster`](#docs-cluster-cluster)
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

    patch.__doc__ = r"""Updates the cluster configuration once the cluster has been created.
### Learn more
* [`DOC /cluster`](#docs-cluster-cluster)"""
    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)




