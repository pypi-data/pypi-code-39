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


__all__ = ["Rotation", "RotationSchema"]
__pdoc__ = {
    "RotationSchema.resource": False,
    "Rotation": False,
}


class RotationSchema(ResourceSchema):
    """The fields of the Rotation object"""

    now = fields.Boolean()
    r""" Manually rotates the audit logs. Optional in PATCH only. Not available in POST.
 """
    schedule = fields.Nested("AuditScheduleSchema", unknown=EXCLUDE)
    r""" The schedule field of the rotation.
 """
    size = fields.Integer()
    r""" Rotates logs based on log size in bytes. This is mutually exclusive with schedule.
 """

    @property
    def resource(self):
        return Rotation

    @property
    def patchable_fields(self):
        return [
            "now",
            "size",
        ]

    @property
    def postable_fields(self):
        return [
            "now",
            "schedule",
            "size",
        ]


class Rotation(Resource):  # pylint: disable=missing-docstring

    _schema = RotationSchema
