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


__all__ = ["SoftwareStatusDetails", "SoftwareStatusDetailsSchema"]
__pdoc__ = {
    "SoftwareStatusDetailsSchema.resource": False,
    "SoftwareStatusDetails": False,
}


class SoftwareStatusDetailsSchema(ResourceSchema):
    """The fields of the SoftwareStatusDetails object"""

    action = fields.Str()
    r""" Corrective action to be taken to resolve the status error.
 """
    end_time = fields.DateTime()
    r""" End time for each status phase.

Example: 2019-02-02T19:00:00.000+0000 """
    message = fields.Str()
    r""" Detailed message of the phase details.

Example: Post-update checks successful """
    name = fields.Str()
    r""" Name of the phase to be retrieved for status details.

Example: initialize """
    node = fields.Nested("SoftwareStatusDetailsReferenceNodeSchema", unknown=EXCLUDE)
    r""" The node field of the software_status_details.
 """
    start_time = fields.DateTime()
    r""" Start time for each status phase.

Example: 2019-02-02T19:00:00.000+0000 """
    state = fields.Str()
    r""" Status of the phase

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
        return SoftwareStatusDetails

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "node",
        ]


class SoftwareStatusDetails(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareStatusDetailsSchema
