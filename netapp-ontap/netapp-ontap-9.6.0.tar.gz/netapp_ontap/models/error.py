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


__all__ = ["Error", "ErrorSchema"]
__pdoc__ = {
    "ErrorSchema.resource": False,
    "Error": False,
}


class ErrorSchema(ResourceSchema):
    """The fields of the Error object"""

    arguments = fields.Nested("ErrorArgumentsSchema", unknown=EXCLUDE, many=True)
    r""" Message arguments
 """
    code = fields.Str()
    r""" Error code

Example: 4 """
    message = fields.Str()
    r""" Error message

Example: entry doesn't exist """
    target = fields.Str()
    r""" The target parameter that caused the error.

Example: uuid """

    @property
    def resource(self):
        return Error

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class Error(Resource):  # pylint: disable=missing-docstring

    _schema = ErrorSchema
