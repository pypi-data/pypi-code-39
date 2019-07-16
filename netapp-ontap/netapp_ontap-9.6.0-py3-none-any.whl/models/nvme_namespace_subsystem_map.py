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


__all__ = ["NvmeNamespaceSubsystemMap", "NvmeNamespaceSubsystemMapSchema"]
__pdoc__ = {
    "NvmeNamespaceSubsystemMapSchema.resource": False,
    "NvmeNamespaceSubsystemMap": False,
}


class NvmeNamespaceSubsystemMapSchema(ResourceSchema):
    """The fields of the NvmeNamespaceSubsystemMap object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_namespace_subsystem_map.
 """
    anagrpid = fields.Str()
    r""" The Asymmetric Namespace Access Group ID (ANAGRPID) of the NVMe namespace.<br/>
The format for an ANAGRPID is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00103050h """
    nsid = fields.Str()
    r""" The NVMe namespace identifier. This is an identifier used by an NVMe controller to provide access to the NVMe namespace.<br/>
The format for an NVMe namespace identifier is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00000001h """
    subsystem = fields.Nested("NvmeSubsystemSchema", unknown=EXCLUDE)
    r""" The subsystem field of the nvme_namespace_subsystem_map.
 """

    @property
    def resource(self):
        return NvmeNamespaceSubsystemMap

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "subsystem",
        ]


class NvmeNamespaceSubsystemMap(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeNamespaceSubsystemMapSchema
