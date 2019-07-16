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


__all__ = ["ApplicationStatisticsSpace1", "ApplicationStatisticsSpace1Schema"]
__pdoc__ = {
    "ApplicationStatisticsSpace1Schema.resource": False,
    "ApplicationStatisticsSpace1": False,
}


class ApplicationStatisticsSpace1Schema(ResourceSchema):
    """The fields of the ApplicationStatisticsSpace1 object"""

    available = fields.Integer()
    r""" The available amount of space left in the application. Note that this field has limited meaning for SAN applications. Space may be considered used from ONTAP's perspective while the host filesystem still considers it available
 """
    logical_used = fields.Integer()
    r""" The amount of space that would currently be used if no space saving features were enabled. For example, if compression were the only space saving feature enabled, this field would represent the uncompressed amount of space used
 """
    provisioned = fields.Integer()
    r""" The originally requested amount of space that was provisioned for the application
 """
    reserved_unused = fields.Integer()
    r""" The amount of space reserved for system features such as snapshots that has not yet been used
 """
    savings = fields.Integer()
    r""" The amount of space saved by all enabled space saving features
 """
    used = fields.Integer()
    r""" The amount of space that is currently being used by the application. Note that this includes any space reserved by the system for features such as snapshots
 """
    used_excluding_reserves = fields.Integer()
    r""" The amount of space that is currently being used, excluding any space that is reserved by the system for features such as snapshots
 """
    used_percent = fields.Integer()
    r""" The percentage of the originally provisioned space that is currently being used by the application
 """

    @property
    def resource(self):
        return ApplicationStatisticsSpace1

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class ApplicationStatisticsSpace1(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationStatisticsSpace1Schema
