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


__all__ = ["SvmNfs", "SvmNfsSchema"]
__pdoc__ = {
    "SvmNfsSchema.resource": False,
    "SvmNfs": False,
}


class SvmNfsSchema(ResourceSchema):
    """The fields of the SvmNfs object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the svm_nfs.
 """
    enabled = fields.Boolean()
    r""" Enable NFS? Setting to true creates a service if not already created.
 """

    @property
    def resource(self):
        return SvmNfs

    @property
    def patchable_fields(self):
        return [
            "enabled",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "enabled",
        ]


class SvmNfs(Resource):  # pylint: disable=missing-docstring

    _schema = SvmNfsSchema
