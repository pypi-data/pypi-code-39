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


__all__ = ["SoftwareMcc", "SoftwareMccSchema"]
__pdoc__ = {
    "SoftwareMccSchema.resource": False,
    "SoftwareMcc": False,
}


class SoftwareMccSchema(ResourceSchema):
    """The fields of the SoftwareMcc object"""

    elapsed_duration = fields.Integer()
    r""" Elapsed duration of update time (in seconds) in MetroCluster.

Example: 2140 """
    estimated_duration = fields.Integer()
    r""" Estimated duration of update time (in seconds) in MetroCluster.

Example: 3480 """
    name = fields.Str()
    r""" Name of the site in MetroCluster.

Example: cluster_A """
    state = fields.Str()
    r""" Upgrade state of MetroCluster.

Valid choices:

* in_progress
* waiting
* paused_by_user
* paused_on_error
* completed
* canceled
* failed
* pause_pending
* cancel_pending """

    @property
    def resource(self):
        return SoftwareMcc

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class SoftwareMcc(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareMccSchema
