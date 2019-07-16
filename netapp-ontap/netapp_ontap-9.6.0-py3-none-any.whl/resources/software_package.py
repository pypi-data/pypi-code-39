# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.


"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SoftwarePackage", "SoftwarePackageSchema"]
__pdoc__ = {
    "SoftwarePackageSchema.resource": False,
    "SoftwarePackageSchema.patchable_fields": False,
    "SoftwarePackageSchema.postable_fields": False,
}


class SoftwarePackageSchema(ResourceSchema):
    """The fields of the SoftwarePackage object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the software_package.
 """
    create_time = fields.DateTime()
    r""" Indicates when this package was loaded

Example: 2019-02-04T19:00:00.000+0000 """
    version = fields.Str()
    r""" Version of this package

Example: ONTAP_X """

    @property
    def resource(self):
        return SoftwarePackage

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]

class SoftwarePackage(Resource):
    """Allows interaction with SoftwarePackage objects on the host"""

    _schema = SoftwarePackageSchema
    _path = "/api/cluster/software/packages"
    @property
    def _keys(self):
        return ["version"]

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

    get_collection.__func__.__doc__ = r"""Retrieves the software packages for a cluster.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
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

    delete_collection.__func__.__doc__ = r"""Deletes a software package from the cluster. The delete operation fails if the package is currently installed.
### Related ONTAP commands
* `cluster image package delete`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the software packages for a cluster.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the software package information.
### Related ONTAP commands
* `cluster image package show-repository`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)



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

    delete.__doc__ = r"""Deletes a software package from the cluster. The delete operation fails if the package is currently installed.
### Related ONTAP commands
* `cluster image package delete`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



