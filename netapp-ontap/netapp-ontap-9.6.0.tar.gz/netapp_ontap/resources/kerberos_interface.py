# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

##  Examples
### Retrieving the Kerberos interface configuration details
```
# The API:
GET /api/protocols/nfs/kerberos/interfaces
# The call:
curl -X GET "https://<mgmt-ip>/api/protocols/nfs/kerberos/interfaces"
```
### Updating the Kerberos interface configuration
```
# The API:
PATCH /api/protocols/nfs/kerberos/interfaces/{uuid}
# The call:
curl -d "@test_patch_kerb_interface.txt" -X PATCH "https://<mgmt-ip>/api/protocols/nfs/kerberos/interfaces/e62936de-7342-11e8-9eb4-0050568be2b7"
test_patch_kerb_interface.txt(body):
{
 "enabled" : "true",
 "spn": "nfs/datalif1-vsim3-d1.sim.netapp.com@NFS-NSR-W01.RTP.NETAPP.COM",
 "user" :"administrator",
 "password" :"Hello123!"
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


__all__ = ["KerberosInterface", "KerberosInterfaceSchema"]
__pdoc__ = {
    "KerberosInterfaceSchema.resource": False,
    "KerberosInterfaceSchema.patchable_fields": False,
    "KerberosInterfaceSchema.postable_fields": False,
}


class KerberosInterfaceSchema(ResourceSchema):
    """The fields of the KerberosInterface object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the kerberos_interface.
 """
    enabled = fields.Boolean()
    r""" Specifies if Kerberos is enabled.
 """
    encryption_types = fields.List(fields.Str)
    r""" The encryption_types field of the kerberos_interface.
 """
    interface = fields.Nested("IpInterfaceSchema", unknown=EXCLUDE)
    r""" The interface field of the kerberos_interface.
 """
    keytab_uri = fields.Str()
    r""" Load keytab from URI
 """
    organizational_unit = fields.Str()
    r""" Organizational unit
 """
    password = fields.Str()
    r""" Account creation password
 """
    spn = fields.Str()
    r""" Service principal name. Valid in PATCH.
 """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the kerberos_interface.
 """
    user = fields.Str()
    r""" Account creation user name
 """

    @property
    def resource(self):
        return KerberosInterface

    @property
    def patchable_fields(self):
        return [
            "enabled",
            "keytab_uri",
            "organizational_unit",
            "password",
            "spn",
            "user",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "enabled",
            "interface",
            "keytab_uri",
            "organizational_unit",
            "password",
            "spn",
            "svm",
            "user",
        ]

class KerberosInterface(Resource):
    """Allows interaction with KerberosInterface objects on the host"""

    _schema = KerberosInterfaceSchema
    _path = "/api/protocols/nfs/kerberos/interfaces"
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

    get_collection.__func__.__doc__ = r"""Retrieves Kerberos interfaces.
### Related ONTAP commands
* `vserver nfs kerberos interface show`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
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

    patch_collection.__func__.__doc__ = r"""Updates the properties of a Kerberos interface.
### Related ONTAP commands
* `vserver nfs kerberos interface modify`
* `vserver nfs kerberos interface enable`
* `vserver nfs kerberos interface disable`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
"""
    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)


    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves Kerberos interfaces.
### Related ONTAP commands
* `vserver nfs kerberos interface show`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves a Kerberos interface.
### Related ONTAP commands
* `vserver nfs kerberos interface show`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
"""
    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


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

    patch.__doc__ = r"""Updates the properties of a Kerberos interface.
### Related ONTAP commands
* `vserver nfs kerberos interface modify`
* `vserver nfs kerberos interface enable`
* `vserver nfs kerberos interface disable`
### Learn more
* [`DOC /protocols/nfs/kerberos/interfaces`](#docs-NAS-protocols_nfs_kerberos_interfaces)
"""
    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)




