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


__all__ = ["ApplicationSnapshotRestore", "ApplicationSnapshotRestoreSchema"]
__pdoc__ = {
    "ApplicationSnapshotRestoreSchema.resource": False,
    "ApplicationSnapshotRestore": False,
}


class ApplicationSnapshotRestoreSchema(ResourceSchema):
    """The fields of the ApplicationSnapshotRestore object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_snapshot_restore.
 """
    application = fields.Nested("ApplicationSnapshotRestoreApplicationSchema", unknown=EXCLUDE)
    r""" The application field of the application_snapshot_restore.
 """
    uuid = fields.Str()
    r""" The Snapshot copy UUID. Valid in URL or POST.
 """

    @property
    def resource(self):
        return ApplicationSnapshotRestore

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
            "uuid",
        ]


class ApplicationSnapshotRestore(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationSnapshotRestoreSchema
