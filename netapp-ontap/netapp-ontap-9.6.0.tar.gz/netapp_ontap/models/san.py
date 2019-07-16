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


__all__ = ["San", "SanSchema"]
__pdoc__ = {
    "SanSchema.resource": False,
    "San": False,
}


class SanSchema(ResourceSchema):
    """The fields of the San object"""

    application_components = fields.Nested("SanApplicationComponentsSchema", unknown=EXCLUDE, many=True)
    r""" The application_components field of the san.
 """
    new_igroups = fields.Nested("SanNewIgroupsSchema", unknown=EXCLUDE, many=True)
    r""" The list of initiator groups to create. Optional in the POST or PATCH body
 """
    os_type = fields.Str()
    r""" The name of the host OS running the application. Required in the POST body

Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* solaris_efi
* vmware
* windows
* windows_2008
* windows_gpt
* xen """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the san.
 """

    @property
    def resource(self):
        return San

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "application_components",
            "new_igroups",
            "os_type",
            "protection_type",
        ]


class San(Resource):  # pylint: disable=missing-docstring

    _schema = SanSchema
