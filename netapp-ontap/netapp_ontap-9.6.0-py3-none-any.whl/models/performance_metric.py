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


__all__ = ["PerformanceMetric", "PerformanceMetricSchema"]
__pdoc__ = {
    "PerformanceMetricSchema.resource": False,
    "PerformanceMetric": False,
}


class PerformanceMetricSchema(ResourceSchema):
    """The fields of the PerformanceMetric object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the performance_metric.
 """
    duration = fields.Str()
    r""" The duration over which this sample is calculated. Samples can be calculated over the following durations:


Valid choices:

* PT15S
* PT4M
* PT30M
* PT2H
* PT1D """
    iops = fields.Nested("PerformanceMetricIoTypeSchema", unknown=EXCLUDE)
    r""" The iops field of the performance_metric.
 """
    latency = fields.Nested("PerformanceMetricIoTypeSchema", unknown=EXCLUDE)
    r""" The latency field of the performance_metric.
 """
    status = fields.Str()
    r""" Any errors associated with the sample. For example, if the aggregation of data over multiple nodes fails then any of the partial errors might be returned, "ok" on success, or "error" on any internal uncategorized failure. Whenever a sample collection is missed but done at a later time, it is back filled to the previous 15 second timestamp and tagged with "backfilled_data". "Inconsistent_ delta_time" is encountered when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. "Negative_delta" is returned when an expected monotonically increasing value has decreased in value. "Inconsistent_old_data" is returned when one or more nodes does not have the latest data.

Valid choices:

* ok
* error
* partial_no_data
* partial_no_response
* partial_other_error
* negative_delta
* backfilled_data
* inconsistent_delta_time
* inconsistent_old_data """
    throughput = fields.Nested("PerformanceMetricIoTypeSchema", unknown=EXCLUDE)
    r""" The throughput field of the performance_metric.
 """
    timestamp = fields.DateTime()
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000 """

    @property
    def resource(self):
        return PerformanceMetric

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "iops",
            "latency",
            "throughput",
        ]


class PerformanceMetric(Resource):  # pylint: disable=missing-docstring

    _schema = PerformanceMetricSchema
