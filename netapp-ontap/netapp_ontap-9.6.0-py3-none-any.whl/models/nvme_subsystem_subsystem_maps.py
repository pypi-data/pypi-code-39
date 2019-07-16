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


__all__ = ["NvmeSubsystemSubsystemMaps", "NvmeSubsystemSubsystemMapsSchema"]
__pdoc__ = {
    "NvmeSubsystemSubsystemMapsSchema.resource": False,
    "NvmeSubsystemSubsystemMaps": False,
}


class NvmeSubsystemSubsystemMapsSchema(ResourceSchema):
    """The fields of the NvmeSubsystemSubsystemMaps object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_subsystem_subsystem_maps.
 """
    anagrpid = fields.Str()
    r""" The Asymmetric Namespace Access Group ID (ANAGRPID) of the NVMe namespace.<br/>
The format for an ANAGRPIP is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00103050h """
    namespace = fields.Nested("NvmeSubsystemNamespaceSchema", unknown=EXCLUDE)
    r""" The namespace field of the nvme_subsystem_subsystem_maps.
 """
    nsid = fields.Str()
    r""" The NVMe namespace identifier. This is an identifier used by an NVMe controller to provide access to the NVMe namespace.<br/>
The format for an NVMe namespace identifier is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00000001h """

    @property
    def resource(self):
        return NvmeSubsystemSubsystemMaps

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "namespace",
        ]


class NvmeSubsystemSubsystemMaps(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeSubsystemSubsystemMapsSchema
