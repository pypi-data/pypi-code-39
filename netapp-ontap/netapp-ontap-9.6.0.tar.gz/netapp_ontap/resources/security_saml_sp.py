# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
You can use this API to retrieve and display relevant information pertaining to the SAML service provider configuration in the cluster. The POST operation creates a SAML service provider configuration if there is none present.  The DELETE operation removes the SAML service provider configuration.  The PATCH operation enables and disables SAML in the cluster.  Various responses are shown in the examples below.
<br />
---
## Examples
### Retrieving the SAML service provider configuration in the cluster.
The following output shows the SAML service provider configuration in the cluster.
<br />
---
```
# The API:
/api/security/authentication/cluster/saml-sp
# The call:
curl -X GET "https://<mgmt-ip>/api/security/authentication/cluster/saml-sp" -H "accept: application/hal+json"
# The response:
{
  "idp_uri": "https://examplelab.customer.com/idp/Metadata",
  "enabled": true,
  "host": "172.21.74.181",
  "certificate": {
    "ca": "cluster1",
    "serial_number": "156F10C3EB4C51C1",
    "common_name": "cluster1"
  },
  "_links": {
    "self": {
      "href": "/api/security/authentication/cluster/saml-sp"
    }
  }
}
```
---
### Creating the SAML service provider configuration
The following output shows how to create a SAML service provider configuration in the cluster.
<br />
---
```
# The API:
/api/security/authentication/cluster/saml-sp
# The call:
curl -X POST "https://<mgmt-ip>/api/security/authentication/cluster/saml-sp?return_records=true" -H "accept: application/hal+json" -d '{ "idp_uri": "https://examplelab.customer.com/idp/Metadata", "host": "172.21.74.181", "certificate": { "ca": "cluster1", "serial_number": "156F10C3EB4C51C1" }}'
```
---
### Updating the SAML service provider configuration
The following output shows how to enable a SAML service provider configuration in the cluster.
<br/>Disabling the configuration requires the client to be authenticated through SAML prior to performing the operation.
<br />
---
```
# The API:
/api/security/authentication/cluster/saml-sp
# The call:
curl -X PATCH "https://<mgmt-ip>/api/security/authentication/cluster/saml-sp/" -d '{ "enabled": true }'
```
---
### Deleting the SAML service provider configuration
---
```
# The API:
/api/security/authentication/cluster/saml-sp
# The call:
curl -X DELETE "https://<mgmt-ip>/api/security/authentication/cluster/saml-sp/"
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


__all__ = ["SecuritySamlSp", "SecuritySamlSpSchema"]
__pdoc__ = {
    "SecuritySamlSpSchema.resource": False,
    "SecuritySamlSpSchema.patchable_fields": False,
    "SecuritySamlSpSchema.postable_fields": False,
}


class SecuritySamlSpSchema(ResourceSchema):
    """The fields of the SecuritySamlSp object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the security_saml_sp.
 """
    certificate = fields.Nested("SecuritySamlSpCertificateSchema", unknown=EXCLUDE)
    r""" The certificate field of the security_saml_sp.
 """
    enabled = fields.Boolean()
    r""" The SAML service provider is enabled.  Valid for PATCH and GET operations only.
 """
    host = fields.Str()
    r""" The SAML service provider host.
 """
    idp_uri = fields.Str()
    r""" The identity provider (IdP) metadata location. Required for POST operations.

Example: https://idp.example.com/FederationMetadata/2007-06/FederationMetadata.xml """

    @property
    def resource(self):
        return SecuritySamlSp

    @property
    def patchable_fields(self):
        return [
            "enabled",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "certificate",
            "host",
            "idp_uri",
        ]

class SecuritySamlSp(Resource):
    """Allows interaction with SecuritySamlSp objects on the host"""

    _schema = SecuritySamlSpSchema
    _path = "/api/security/authentication/cluster/saml-sp"





    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves a SAML service provider configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
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

    post.__doc__ = r"""Creates a SAML service provider configuration. Note that "common_name" is mutually exclusive with "serial_number" and "ca" in the POST. SAML will initially be disabled, requiring a patch to set "enabled" to "true", so that the user has time to complete the setup of the IdP.
### Required properties
* `idp_uri`
### Optional properties
* `certificate`
* `enabled`
* `host`

### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
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

    patch.__doc__ = r"""Updates a SAML service provider configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
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

    delete.__doc__ = r"""Deletes a SAML service provider configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



