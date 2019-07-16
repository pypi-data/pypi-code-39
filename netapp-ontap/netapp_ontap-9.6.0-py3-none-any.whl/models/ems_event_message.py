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


__all__ = ["EmsEventMessage", "EmsEventMessageSchema"]
__pdoc__ = {
    "EmsEventMessageSchema.resource": False,
    "EmsEventMessage": False,
}


class EmsEventMessageSchema(ResourceSchema):
    """The fields of the EmsEventMessage object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the ems_event_message.
 """
    name = fields.Str()
    r""" Message name of the event. Returned by default.

Example: callhome.spares.low """
    severity = fields.Str()
    r""" Severity of the event. Returned by default.

Valid choices:

* emergency
* alert
* error
* notice
* informational
* debug """

    @property
    def resource(self):
        return EmsEventMessage

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class EmsEventMessage(Resource):  # pylint: disable=missing-docstring

    _schema = EmsEventMessageSchema
