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


__all__ = ["ErrorResponses", "ErrorResponsesSchema"]
__pdoc__ = {
    "ErrorResponsesSchema.resource": False,
    "ErrorResponses": False,
}


class ErrorResponsesSchema(ResourceSchema):
    """The fields of the ErrorResponses object"""

    errors = fields.Nested("ErrorSchema", unknown=EXCLUDE, many=True)
    r""" The errors field of the error_responses.
 """

    @property
    def resource(self):
        return ErrorResponses

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "errors",
        ]


class ErrorResponses(Resource):  # pylint: disable=missing-docstring

    _schema = ErrorResponsesSchema
