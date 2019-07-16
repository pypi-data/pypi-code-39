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


__all__ = ["ApplicationComponentSnapshotRestoreApplication", "ApplicationComponentSnapshotRestoreApplicationSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotRestoreApplicationSchema.resource": False,
    "ApplicationComponentSnapshotRestoreApplication": False,
}


class ApplicationComponentSnapshotRestoreApplicationSchema(ResourceSchema):
    """The fields of the ApplicationComponentSnapshotRestoreApplication object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_component_snapshot_restore_application.
 """
    uuid = fields.Str()
    r""" Application UUID. Valid in URL or POST
 """

    @property
    def resource(self):
        return ApplicationComponentSnapshotRestoreApplication

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


class ApplicationComponentSnapshotRestoreApplication(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationComponentSnapshotRestoreApplicationSchema
