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


__all__ = ["NvmeSubsystemNamespace", "NvmeSubsystemNamespaceSchema"]
__pdoc__ = {
    "NvmeSubsystemNamespaceSchema.resource": False,
    "NvmeSubsystemNamespace": False,
}


class NvmeSubsystemNamespaceSchema(ResourceSchema):
    """The fields of the NvmeSubsystemNamespace object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_subsystem_namespace.
 """
    name = fields.Str()
    r""" The name of the NVMe namespace.


Example: /vol/vol1/namespace1 """
    uuid = fields.Str()
    r""" The unique identifier of the NVMe namespace.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeSubsystemNamespace

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class NvmeSubsystemNamespace(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeSubsystemNamespaceSchema
