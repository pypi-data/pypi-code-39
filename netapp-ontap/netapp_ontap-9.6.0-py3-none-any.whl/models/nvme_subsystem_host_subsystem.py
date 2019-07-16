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


__all__ = ["NvmeSubsystemHostSubsystem", "NvmeSubsystemHostSubsystemSchema"]
__pdoc__ = {
    "NvmeSubsystemHostSubsystemSchema.resource": False,
    "NvmeSubsystemHostSubsystem": False,
}


class NvmeSubsystemHostSubsystemSchema(ResourceSchema):
    """The fields of the NvmeSubsystemHostSubsystem object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_subsystem_host_subsystem.
 """
    uuid = fields.Str()
    r""" The unique identifier of the NVMe subsystem.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeSubsystemHostSubsystem

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class NvmeSubsystemHostSubsystem(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeSubsystemHostSubsystemSchema
