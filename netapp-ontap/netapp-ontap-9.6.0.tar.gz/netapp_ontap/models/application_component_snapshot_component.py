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


__all__ = ["ApplicationComponentSnapshotComponent", "ApplicationComponentSnapshotComponentSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotComponentSchema.resource": False,
    "ApplicationComponentSnapshotComponent": False,
}


class ApplicationComponentSnapshotComponentSchema(ResourceSchema):
    """The fields of the ApplicationComponentSnapshotComponent object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_component_snapshot_component.
 """
    name = fields.Str()
    r""" Component Name
 """
    uuid = fields.Str()
    r""" Component UUID
 """

    @property
    def resource(self):
        return ApplicationComponentSnapshotComponent

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class ApplicationComponentSnapshotComponent(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationComponentSnapshotComponentSchema
