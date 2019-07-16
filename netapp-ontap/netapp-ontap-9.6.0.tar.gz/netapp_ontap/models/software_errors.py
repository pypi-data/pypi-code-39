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


__all__ = ["SoftwareErrors", "SoftwareErrorsSchema"]
__pdoc__ = {
    "SoftwareErrorsSchema.resource": False,
    "SoftwareErrors": False,
}


class SoftwareErrorsSchema(ResourceSchema):
    """The fields of the SoftwareErrors object"""

    code = fields.Integer()
    r""" Error code of message

Example: 177 """
    message = fields.Str()
    r""" Error message

Example: Giveback of CFO aggregate is vetoed. Action: Use the "storage failover show-giveback" command to view detailed veto status information. Correct the vetoed update check. Use the "storage failover giveback -ofnode "node1" command to complete the giveback. """
    severity = fields.Str()
    r""" Severity of error

Valid choices:

* informational
* warning
* error """

    @property
    def resource(self):
        return SoftwareErrors

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class SoftwareErrors(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareErrorsSchema
