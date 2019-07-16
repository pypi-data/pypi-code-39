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


__all__ = ["ApplicationComponentSnapshotRestore", "ApplicationComponentSnapshotRestoreSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotRestoreSchema.resource": False,
    "ApplicationComponentSnapshotRestore": False,
}


class ApplicationComponentSnapshotRestoreSchema(ResourceSchema):
    """The fields of the ApplicationComponentSnapshotRestore object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_component_snapshot_restore.
 """
    application = fields.Nested("ApplicationComponentSnapshotRestoreApplicationSchema", unknown=EXCLUDE)
    r""" The application field of the application_component_snapshot_restore.
 """
    component = fields.Nested("ApplicationComponentSnapshotRestoreComponentSchema", unknown=EXCLUDE)
    r""" The component field of the application_component_snapshot_restore.
 """
    uuid = fields.Str()
    r""" Snapshot UUID. Valid in URL or POST
 """

    @property
    def resource(self):
        return ApplicationComponentSnapshotRestore

    @property
    def patchable_fields(self):
        return [
            "uuid",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "application",
            "component",
            "uuid",
        ]


class ApplicationComponentSnapshotRestore(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationComponentSnapshotRestoreSchema
