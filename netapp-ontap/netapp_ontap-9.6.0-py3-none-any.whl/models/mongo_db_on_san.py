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


__all__ = ["MongoDbOnSan", "MongoDbOnSanSchema"]
__pdoc__ = {
    "MongoDbOnSanSchema.resource": False,
    "MongoDbOnSan": False,
}


class MongoDbOnSanSchema(ResourceSchema):
    """The fields of the MongoDbOnSan object"""

    dataset = fields.Nested("MongoDbOnSanDatasetSchema", unknown=EXCLUDE)
    r""" The dataset field of the mongo_db_on_san.
 """
    new_igroups = fields.Nested("MongoDbOnSanNewIgroupsSchema", unknown=EXCLUDE, many=True)
    r""" The list of initiator groups to create. Optional in the POST or PATCH body
 """
    os_type = fields.Str()
    r""" The name of the host OS running the application. Optional in the POST body

Valid choices:

* hyper_v
* linux
* solaris
* solaris_efi
* vmware
* windows
* windows_2008
* windows_gpt
* xen """
    primary_igroup_name = fields.Str()
    r""" The initiator group for the primary. Required in the POST body and optional in the PATCH body
 """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the mongo_db_on_san.
 """
    secondary_igroups = fields.Nested("MongoDbOnSanSecondaryIgroupsSchema", unknown=EXCLUDE, many=True)
    r""" The secondary_igroups field of the mongo_db_on_san.
 """

    @property
    def resource(self):
        return MongoDbOnSan

    @property
    def patchable_fields(self):
        return [
            "primary_igroup_name",
        ]

    @property
    def postable_fields(self):
        return [
            "dataset",
            "new_igroups",
            "os_type",
            "primary_igroup_name",
            "protection_type",
            "secondary_igroups",
        ]


class MongoDbOnSan(Resource):  # pylint: disable=missing-docstring

    _schema = MongoDbOnSanSchema
