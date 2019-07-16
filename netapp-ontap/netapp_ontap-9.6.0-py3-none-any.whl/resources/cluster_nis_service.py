# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
NIS servers are used to authenticate user and client computers. NIS domain name and NIS server information is required to configure NIS. This API retrieves and manages NIS server configurations.
## Examples
### Retrieving cluster NIS information
The cluster NIS GET operation retrieves the NIS configuration of the cluster.<br>
The following example shows how a GET operation is used to retrieve the cluster NIS configuration:
```
# The API:
/security/authentication/cluster/nis
# The call:
curl -X GET "https://<mgmt-ip>/api/security/authentication/cluster/nis" -H "accept: application/hal+json"
# The response:
{
  "domain": "domainA.example.com",
  "servers": [
    "10.10.10.10",
    "example.com"
  ]
  "bound_servers": [
    "10.10.10.10"
  ]
}
```
### Creating the cluster NIS configuration
The cluster NIS POST operation creates a NIS configuration for the cluster.<br>
The following example shows how a POST operation is used to create a cluster NIS configuration:
```
# The API:
/security/authentication/cluster/nis
# The call:
curl -X POST "https://<mgmt-ip>/api/security/authentication/cluster/nis" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"domain\": \"domainA.example.com\", \"servers\": [ \"10.10.10.10\",\"example.com\" ]}"
```
### Updating the cluster NIS configuration
The cluster NIS PATCH operation updates the NIS configuration of the cluster.<br>
The following example shows how to update the domain:
```
# The API:
/security/authentication/cluster/nis
# The call:
curl -X PATCH "https://<mgmt-ip>/api/security/authentication/cluster/nis" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"domain\": \"domainC.example.com\", \"servers\": [ \"13.13.13.13\" ]}"
```
The following example shows how to update the server:
```
# The API:
/security/authentication/cluster/nis
# The call:
curl -X PATCH "https://<mgmt-ip>/api/security/authentication/cluster/nis" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"servers\": [ \"14.14.14.14\" ]}"
```
## Deleting the cluster NIS configuration
The cluster NIS DELETE operation deletes the NIS configuration of the cluster.<br>
The following example shows how a DELETE operation is used to delete the cluster NIS configuration:
```
# The API:
/security/authentication/cluster/nis
# The call:
curl -X DELETE "https://<mgmt-ip>/api/security/authentication/cluster/nis" -H "accept: application/hal+json"
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


__all__ = ["ClusterNisService", "ClusterNisServiceSchema"]
__pdoc__ = {
    "ClusterNisServiceSchema.resource": False,
    "ClusterNisServiceSchema.patchable_fields": False,
    "ClusterNisServiceSchema.postable_fields": False,
}


class ClusterNisServiceSchema(ResourceSchema):
    """The fields of the ClusterNisService object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the cluster_nis_service.
 """
    bound_servers = fields.List(fields.Str)
    r""" The bound_servers field of the cluster_nis_service.
 """
    domain = fields.Str(validate=len_validation(minimum=1, maximum=64))
    r""" The NIS domain to which this configuration belongs.
 """
    servers = fields.List(fields.Str)
    r""" A list of hostnames or IP addresses of NIS servers used
by the NIS domain configuration. """

    @property
    def resource(self):
        return ClusterNisService

    @property
    def patchable_fields(self):
        return [
            "domain",
            "servers",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "domain",
            "servers",
        ]

class ClusterNisService(Resource):
    """Allows interaction with ClusterNisService objects on the host"""

    _schema = ClusterNisServiceSchema
    _path = "/api/security/authentication/cluster/nis"





    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the NIS configuration of the cluster. Both NIS domain and servers are displayed by default.
The 'bound servers' field indicates the successfully bound NIS servers.

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
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

    post.__doc__ = r"""The cluster can have one NIS server configuration. Specify the NIS domain and NIS servers as input. Domain name and servers fields cannot be empty.
Both FQDNs and IP addresses are supported for the 'servers' field. IPv6 must be enabled if IPv6 family addresses are specified in the 'servers' field.
A maximum of ten NIS servers are supported.

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
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

    patch.__doc__ = r"""Both NIS domain and servers can be modified. Domains and servers cannot be empty. Both FQDNs and IP addresses are supported for the 'servers' field. If the domain is modified, NIS servers must also be specified. IPv6 must be enabled if IPv6 family addresses are specified for the 'servers' field.<br/>

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
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

    delete.__doc__ = r"""The DELETE operation removes the NIS configuration of the cluster. NIS can be removed as a source from ns-switch if NIS is not used for lookups.

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



