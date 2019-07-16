# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
This endpoint supports the following operations: GET (collection and instance), POST, and DELETE.
<br/>
---
## Retrieving network routes
The IP routes GET API retrieves and displays relevant information pertaining to the routes configured in the cluster. The API retrieves the list of all routes configured in the cluster, or a specific route. The fields that are returned in the response will differ with the configuration.
## Examples
### Retrieving all routes in the cluster
The following output shows the list of all routes configured in a cluster.
<br/>
---
```
# The API:
/api/network/ip/routes
# The call:
curl -X GET "https://<mgmt-ip>/api/network/ip/routes?fields=*" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "uuid": "5fdffb0b-62f8-11e8-853d-005056b4c971",
      "ipspace": {
        "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
        "name": "Default",
        "_links": {
          "self": {
            "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
          }
        }
      },
      "svm": {
        "uuid": "3243312c-62f8-11e8-853d-005056b4c971",
        "name": "vs1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/3243312c-62f8-11e8-853d-005056b4c971"
          }
        }
      },
      "scope": "svm",
      "destination": {
        "address": "10.4.3.14",
        "netmask": "18",
        "family": "ipv4"
      },
      "gateway": "10.4.3.1",
      "_links": {
        "self": {
          "href": "/api/network/ip/routes/5fdffb0b-62f8-11e8-853d-005056b4c971"
        }
      }
    },
    {
      "uuid": "84c128d2-62f9-11e8-853d-005056b4c971",
      "ipspace": {
        "uuid": "cc71aadc-62f7-11e8-853d-005056b4c971",
        "name": "ips1",
        "_links": {
          "self": {
            "href": "/api/network/ipspaces/cc71aadc-62f7-11e8-853d-005056b4c971"
          }
        }
      },
      "scope": "cluster",
      "destination": {
        "address": "::",
        "netmask": "0",
        "family": "ipv6"
      },
      "gateway": "fd20:8b1e:b255:814e::1",
      "_links": {
        "self": {
          "href": "/api/network/ip/routes/84c128d2-62f9-11e8-853d-005056b4c971"
        }
      }
    },
    {
      "uuid": "8cc72bcd-616c-11e8-a4df-005056b4c971",
      "ipspace": {
        "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
        "name": "Default",
        "_links": {
          "self": {
            "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
          }
        }
      },
      "scope": "cluster",
      "destination": {
        "address": "0.0.0.0",
        "netmask": "0",
        "family": "ipv4"
      },
      "gateway": "10.224.64.1",
      "_links": {
        "self": {
          "href": "/api/network/ip/routes/8cc72bcd-616c-11e8-a4df-005056b4c971"
        }
      }
    },
    {
      "uuid": "d63b6eee-62f9-11e8-853d-005056b4c971",
      "ipspace": {
        "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
        "name": "Default",
        "_links": {
          "self": {
            "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
          }
        }
      },
      "svm": {
        "uuid": "3243312c-62f8-11e8-853d-005056b4c971",
        "name": "vs1",
        "_links": {
          "self": {
            "href": "/api/svm/svms/3243312c-62f8-11e8-853d-005056b4c971"
          }
        }
      },
      "scope": "svm",
      "destination": {
        "address": "fd20:8b1e:b255:814e::",
        "netmask": "64",
        "family": "ipv6"
      },
      "gateway": "fd20:8b1e:b255:814e::1",
      "_links": {
        "self": {
          "href": "/api/network/ip/routes/d63b6eee-62f9-11e8-853d-005056b4c971"
        }
      }
    }
  ],
  "num_records": 4,
  "_links": {
    "self": {
      "href": "/api/network/ip/routes?fields=*"
    }
  }
}
```
---
### Retrieving a specific cluster-scoped route
The following output shows the returned response when a specific cluster-scoped route is requested. The system returns an error if there is no route with the requested UUID. SVM information is not returned for cluster-scoped routes.
<br/>
---
```
# The API:
/api/network/ip/routes/{uuid}
# The call:
curl -X GET "https://<mgmt-ip>/api/network/ip/routes/84c128d2-62f9-11e8-853d-005056b4c971?fields=*" -H "accept: application/hal+json"
# The response:
{
  "uuid": "84c128d2-62f9-11e8-853d-005056b4c971",
  "ipspace": {
    "uuid": "cc71aadc-62f7-11e8-853d-005056b4c971",
    "name": "ips1",
    "_links": {
      "self": {
        "href": "/api/network/ipspaces/cc71aadc-62f7-11e8-853d-005056b4c971"
      }
    }
  },
  "scope": "cluster",
  "destination": {
    "address": "::",
    "netmask": "0",
    "family": "ipv6"
  },
  "gateway": "fd20:8b1e:b255:814e::1",
  "_links": {
    "self": {
      "href": "/api/network/ip/routes/84c128d2-62f9-11e8-853d-005056b4c971"
    }
  }
}
```
---
### Retrieving a specific SVM-scoped route
The following output shows the returned response when a specific SVM-scoped route is requested. The system returns an error if there is no route with the requested UUID. The SVM object is only included for SVM-scoped routes.
<br/>
---
```
# The API:
/api/network/ip/routes
# The call:
curl -X GET "https://<mgmt-ip>/api/network/ip/routes/d63b6eee-62f9-11e8-853d-005056b4c971?fields=*" -H "accept: application/hal+json"
# The response:
{
  "uuid": "d63b6eee-62f9-11e8-853d-005056b4c971",
  "ipspace": {
    "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
    "name": "Default",
    "_links": {
      "self": {
        "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
      }
    }
  },
  "svm": {
    "uuid": "3243312c-62f8-11e8-853d-005056b4c971",
    "name": "vs1",
    "_links": {
      "self": {
        "href": "/api/svm/svms/3243312c-62f8-11e8-853d-005056b4c971"
      }
    }
  },
  "scope": "svm",
  "destination": {
    "address": "fd20:8b1e:b255:814e::",
    "netmask": "64",
    "family": "ipv6"
  },
  "gateway": "fd20:8b1e:b255:814e::1",
  "_links": {
    "self": {
      "href": "/api/network/ip/routes/d63b6eee-62f9-11e8-853d-005056b4c971"
    }
  }
}
```
---
## Creating network routes
The POST API is used to create an SVM-scoped route by specifying the associated SVM, or a cluster-scoped route by specifying the associated IPspace.
## Examples
### Creating a cluster-scoped route
IPspace is required to create a cluster-scoped route. If the IPspace is not specified, the route will be created in the Default IPspace. The default destination will be set to "0.0.0.0/0" for IPv4 gateway addresses or "::/0" for IPv6 gateway addresses.
<br/>
---
```
# The API:
/api/network/ip/routes
# The call:
curl -X POST "https://<mgmt-ip>/api/network/ip/routes?return_records=true" -H "accept: application/json" -d '{ "ipspace": { "name":"ips1" }, "gateway": "10.10.10.1"}'
# The response:
{
  "num_records": 1,
  "records": [
    {
      "uuid": "ae583c9e-9ac7-11e8-8bc9-005056bbd531",
      "ipspace": {
        "name": "ips1"
      },
      "gateway": "10.10.10.1"
    }
  ]
}
```
---
### Creating an SVM-scoped route
To create an SVM-scoped route, the associated SVM can be identified by either its UUID or name.
<br/>
---
```
# The API:
/api/network/ip/routes
# The call:
curl -X POST "https://<mgmt-ip>/api/network/ip/routes?return_records=true" -H "accept: application/json" -d '{ "svm": { "name":"vs0" }, "gateway": "10.10.10.1"}'
# The response:
{
  "num_records": 1,
  "records": [
    {
      "uuid": "38805a91-9ac9-11e8-8bc9-005056bbd531",
      "svm": {
        "name": "vs0"
      },
      "gateway": "10.10.10.1"
    }
  ]
}
```
---
## Deleting network routes
The DELETE API can remove a specific route identified by its UUID.
## Example
### Deleting a specific route
---
```
# The API:
/api/network/ip/routes
# The call:
curl -X DELETE "https://<mgmt-ip>/api/network/ip/routes/38805a91-9ac9-11e8-8bc9-005056bbd531"
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


__all__ = ["NetworkRoute", "NetworkRouteSchema"]
__pdoc__ = {
    "NetworkRouteSchema.resource": False,
    "NetworkRouteSchema.patchable_fields": False,
    "NetworkRouteSchema.postable_fields": False,
}


class NetworkRouteSchema(ResourceSchema):
    """The fields of the NetworkRoute object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the network_route.
 """
    destination = fields.Nested("IpInfoSchema", unknown=EXCLUDE)
    r""" The destination field of the network_route.
 """
    gateway = fields.Str()
    r""" The IP address of the gateway router leading to the destination.

Example: 10.1.1.1 """
    ipspace = fields.Nested("IpspaceSchema", unknown=EXCLUDE)
    r""" The ipspace field of the network_route.
 """
    scope = fields.Str()
    r""" The scope field of the network_route.
 """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the network_route.
 """
    uuid = fields.Str()
    r""" The UUID that uniquely identifies the route.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NetworkRoute

    @property
    def patchable_fields(self):
        return [
            "gateway",
            "scope",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "destination",
            "gateway",
            "ipspace",
            "scope",
            "svm",
        ]

class NetworkRoute(Resource):
    """Allows interaction with NetworkRoute objects on the host"""

    _schema = NetworkRouteSchema
    _path = "/api/network/ip/routes"
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

    get_collection.__func__.__doc__ = r"""Retrieves the collection of IP routes.
### Related ONTAP commands
* `network route show`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


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

    delete_collection.__func__.__doc__ = r"""Deletes a specific IP route.
### Related ONTAP commands
* `network route delete`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the collection of IP routes.
### Related ONTAP commands
* `network route show`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the details of a specific IP route.
### Related ONTAP commands
* `network route show`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
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

    post.__doc__ = r"""Creates a cluster-scoped or SVM-scoped static route.
### Required properties
* `gateway` - IP address to route packets to.
* SVM-scoped routes
  * `svm.name` or `svm.uuid` - SVM that route is applied to.
* cluster-scoped routes
  * There are no additional required fields for cluster-scoped routes.
### Default property values
If not specified in POST, the following default property values are assigned:
* `destination` - _0.0.0.0/0_ for IPv4 or _::/0_ for IPv6.
* `ipspace.name`
  * _Default_ for cluster-scoped routes.
  * Name of the SVM's IPspace for SVM-scoped routes.
### Related ONTAP commands
* `network route create`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


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

    delete.__doc__ = r"""Deletes a specific IP route.
### Related ONTAP commands
* `network route delete`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



