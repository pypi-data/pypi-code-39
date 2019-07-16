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


__all__ = ["Performance", "PerformanceSchema"]
__pdoc__ = {
    "PerformanceSchema.resource": False,
    "Performance": False,
}


class PerformanceSchema(ResourceSchema):
    """The fields of the Performance object"""

    links = fields.Nested("CollectionLinksSchema", unknown=EXCLUDE)
    r""" The links field of the performance.
 """
    num_records = fields.Integer()
    r""" Number of records
 """
    records = fields.Nested("PerformanceMetricSchema", unknown=EXCLUDE, many=True)
    r""" The records field of the performance.
 """

    @property
    def resource(self):
        return Performance

    @property
    def patchable_fields(self):
        return [
            "num_records",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "num_records",
            "records",
        ]


class Performance(Resource):  # pylint: disable=missing-docstring

    _schema = PerformanceSchema
