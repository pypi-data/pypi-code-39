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


__all__ = ["SoftwareUpdateDetails", "SoftwareUpdateDetailsSchema"]
__pdoc__ = {
    "SoftwareUpdateDetailsSchema.resource": False,
    "SoftwareUpdateDetails": False,
}


class SoftwareUpdateDetailsSchema(ResourceSchema):
    """The fields of the SoftwareUpdateDetails object"""

    elapsed_duration = fields.Integer()
    r""" Elapsed duration for each update phase

Example: 2100 """
    estimated_duration = fields.Integer()
    r""" Estimated duration for each update phase

Example: 4620 """
    node = fields.Nested("SoftwareUpdateDetailsReferenceNodeSchema", unknown=EXCLUDE)
    r""" The node field of the software_update_details.
 """
    phase = fields.Str()
    r""" Phase details

Example: Pre-update checks """
    state = fields.Str()
    r""" State of the update phase

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
        return SoftwareUpdateDetails

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "node",
        ]


class SoftwareUpdateDetails(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareUpdateDetailsSchema
