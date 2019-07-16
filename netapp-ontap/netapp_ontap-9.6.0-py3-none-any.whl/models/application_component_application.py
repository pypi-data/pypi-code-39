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


__all__ = ["ApplicationComponentApplication", "ApplicationComponentApplicationSchema"]
__pdoc__ = {
    "ApplicationComponentApplicationSchema.resource": False,
    "ApplicationComponentApplication": False,
}


class ApplicationComponentApplicationSchema(ResourceSchema):
    """The fields of the ApplicationComponentApplication object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_component_application.
 """
    name = fields.Str()
    r""" Application name
 """
    uuid = fields.Str()
    r""" The application UUID. Valid in URL.
 """

    @property
    def resource(self):
        return ApplicationComponentApplication

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class ApplicationComponentApplication(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationComponentApplicationSchema
