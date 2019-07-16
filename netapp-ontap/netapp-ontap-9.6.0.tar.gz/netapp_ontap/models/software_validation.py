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


__all__ = ["SoftwareValidation", "SoftwareValidationSchema"]
__pdoc__ = {
    "SoftwareValidationSchema.resource": False,
    "SoftwareValidation": False,
}


class SoftwareValidationSchema(ResourceSchema):
    """The fields of the SoftwareValidation object"""

    action = fields.Str()
    r""" Corrective action to resolve errors or warnings for update checks.
 """
    message = fields.Str()
    r""" Details of the error or warning encountered by the update check.
 """
    status = fields.Str()
    r""" Status of this update check.

Valid choices:

* warning
* error """
    update_check = fields.Str()
    r""" Name of the update check to be validated.

Example: nfs_mounts """

    @property
    def resource(self):
        return SoftwareValidation

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class SoftwareValidation(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareValidationSchema
