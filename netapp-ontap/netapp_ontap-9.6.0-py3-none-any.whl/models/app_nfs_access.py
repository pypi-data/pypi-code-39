# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema


__all__ = ["AppNfsAccess", "AppNfsAccessSchema"]
__pdoc__ = {
    "AppNfsAccessSchema.resource": False,
    "AppNfsAccess": False,
}


class AppNfsAccessSchema(ResourceSchema):
    """The fields of the AppNfsAccess object"""

    access = fields.Str()
    r""" The NFS access granted. Optional in the POST body

Valid choices:

* none
* ro
* rw """
    host = fields.Str()
    r""" The name of the NFS entity granted access. Optional in the POST body
 """

    @property
    def resource(self):
        return AppNfsAccess

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "access",
            "host",
        ]


class AppNfsAccess(Resource):  # pylint: disable=missing-docstring

    _schema = AppNfsAccessSchema
