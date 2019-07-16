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


__all__ = ["ApplicationRpoLocal", "ApplicationRpoLocalSchema"]
__pdoc__ = {
    "ApplicationRpoLocalSchema.resource": False,
    "ApplicationRpoLocal": False,
}


class ApplicationRpoLocalSchema(ResourceSchema):
    """The fields of the ApplicationRpoLocal object"""

    description = fields.Str()
    r""" A detailed description of the local RPO. This will include details about the snapshot schedule
 """
    name = fields.Str()
    r""" The local RPO of the application. This indicates how often application snapshots are automatically created

Valid choices:

* 6_hourly
* 15_minutely
* hourly
* none """

    @property
    def resource(self):
        return ApplicationRpoLocal

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class ApplicationRpoLocal(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationRpoLocalSchema
