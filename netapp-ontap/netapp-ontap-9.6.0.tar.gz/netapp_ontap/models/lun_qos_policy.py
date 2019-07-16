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


__all__ = ["LunQosPolicy", "LunQosPolicySchema"]
__pdoc__ = {
    "LunQosPolicySchema.resource": False,
    "LunQosPolicy": False,
}


class LunQosPolicySchema(ResourceSchema):
    """The fields of the LunQosPolicy object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the lun_qos_policy.
 """
    name = fields.Str()
    r""" The name of the QoS policy. To remove the QoS policy from a LUN, leaving it with no QoS policy, set this property to an empty string ("") in a PATCH request. Valid in POST and PATCH.


Example: qos1 """
    uuid = fields.Str()
    r""" The unique identifier of the QoS policy. Valid in POST and PATCH.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LunQosPolicy

    @property
    def patchable_fields(self):
        return [
            "name",
            "uuid",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name",
            "uuid",
        ]


class LunQosPolicy(Resource):  # pylint: disable=missing-docstring

    _schema = LunQosPolicySchema
