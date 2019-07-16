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


__all__ = ["VolumeClone", "VolumeCloneSchema"]
__pdoc__ = {
    "VolumeCloneSchema.resource": False,
    "VolumeClone": False,
}


class VolumeCloneSchema(ResourceSchema):
    """The fields of the VolumeClone object"""

    is_flexclone = fields.Boolean()
    r""" Specifies if this volume is a normal FlexVol or FlexClone. This field needs to be set when creating a FlexClone. Valid in POST.
 """
    parent_snapshot = fields.Nested("SnapshotSchema", unknown=EXCLUDE)
    r""" The parent_snapshot field of the volume_clone.
 """
    parent_svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The parent_svm field of the volume_clone.
 """
    parent_volume = fields.Nested("VolumeSchema", unknown=EXCLUDE)
    r""" The parent_volume field of the volume_clone.
 """
    split_complete_percent = fields.Integer()
    r""" Percentage of FlexClone blocks split from its parent volume.
 """
    split_estimate = fields.Integer()
    r""" Space required by the containing-aggregate to split the FlexClone volume.
 """
    split_initiated = fields.Boolean()
    r""" This field is set when split is executed on any FlexClone, that is when the FlexClone volume is split from its parent FlexVol. This field needs to be set for splitting a FlexClone form FlexVol. Valid in PATCH.
 """

    @property
    def resource(self):
        return VolumeClone

    @property
    def patchable_fields(self):
        return [
            "is_flexclone",
            "split_initiated",
        ]

    @property
    def postable_fields(self):
        return [
            "is_flexclone",
            "parent_snapshot",
            "parent_svm",
            "parent_volume",
            "split_initiated",
        ]


class VolumeClone(Resource):  # pylint: disable=missing-docstring

    _schema = VolumeCloneSchema
