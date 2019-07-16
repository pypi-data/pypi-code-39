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


__all__ = ["ApplicationComponentSnapshotRestoreComponent", "ApplicationComponentSnapshotRestoreComponentSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotRestoreComponentSchema.resource": False,
    "ApplicationComponentSnapshotRestoreComponent": False,
}


class ApplicationComponentSnapshotRestoreComponentSchema(ResourceSchema):
    """The fields of the ApplicationComponentSnapshotRestoreComponent object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_component_snapshot_restore_component.
 """
    uuid = fields.Str()
    r""" Application Component UUID. Valid in URL or POST
 """

    @property
    def resource(self):
        return ApplicationComponentSnapshotRestoreComponent

    @property
    def patchable_fields(self):
        return [
            "uuid",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "uuid",
        ]


class ApplicationComponentSnapshotRestoreComponent(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationComponentSnapshotRestoreComponentSchema
