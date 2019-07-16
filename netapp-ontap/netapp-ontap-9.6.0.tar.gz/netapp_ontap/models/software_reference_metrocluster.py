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


__all__ = ["SoftwareReferenceMetrocluster", "SoftwareReferenceMetroclusterSchema"]
__pdoc__ = {
    "SoftwareReferenceMetroclusterSchema.resource": False,
    "SoftwareReferenceMetrocluster": False,
}


class SoftwareReferenceMetroclusterSchema(ResourceSchema):
    """The fields of the SoftwareReferenceMetrocluster object"""

    clusters = fields.Nested("SoftwareMccSchema", unknown=EXCLUDE, many=True)
    r""" List of MetroCluster sites, statuses, and active versions.
 """
    progress_details = fields.Str()
    r""" MetroCluster update progress details.

Example: Switchover in progress. """
    progress_summary = fields.Str()
    r""" MetroCluster update progress summary.

Example: MetroCluster updated successfully. """

    @property
    def resource(self):
        return SoftwareReferenceMetrocluster

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class SoftwareReferenceMetrocluster(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareReferenceMetroclusterSchema
