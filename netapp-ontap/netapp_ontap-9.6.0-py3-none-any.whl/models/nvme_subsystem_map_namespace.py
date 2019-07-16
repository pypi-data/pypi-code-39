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


__all__ = ["NvmeSubsystemMapNamespace", "NvmeSubsystemMapNamespaceSchema"]
__pdoc__ = {
    "NvmeSubsystemMapNamespaceSchema.resource": False,
    "NvmeSubsystemMapNamespace": False,
}


class NvmeSubsystemMapNamespaceSchema(ResourceSchema):
    """The fields of the NvmeSubsystemMapNamespace object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_subsystem_map_namespace.
 """
    name = fields.Str()
    r""" The fully qualified path name of the NVMe namespace composed from the volume name, qtree name, and file name of the NVMe namespace. Valid in POST.


Example: /vol/vol1/namespace1 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the nvme_subsystem_map_namespace.
 """
    uuid = fields.Str()
    r""" The unique identifier of the NVMe namespace. Valid in POST.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeSubsystemMapNamespace

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name",
            "node",
            "uuid",
        ]


class NvmeSubsystemMapNamespace(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeSubsystemMapNamespaceSchema
