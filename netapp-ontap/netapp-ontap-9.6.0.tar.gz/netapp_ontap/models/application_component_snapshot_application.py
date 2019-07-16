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


__all__ = ["ApplicationComponentSnapshotApplication", "ApplicationComponentSnapshotApplicationSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotApplicationSchema.resource": False,
    "ApplicationComponentSnapshotApplication": False,
}


class ApplicationComponentSnapshotApplicationSchema(ResourceSchema):
    """The fields of the ApplicationComponentSnapshotApplication object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_component_snapshot_application.
 """
    name = fields.Str()
    r""" Application Name
 """
    uuid = fields.Str()
    r""" Application UUID. Valid in URL
 """

    @property
    def resource(self):
        return ApplicationComponentSnapshotApplication

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class ApplicationComponentSnapshotApplication(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationComponentSnapshotApplicationSchema
