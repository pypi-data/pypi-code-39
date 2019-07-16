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


__all__ = ["PortLag", "PortLagSchema"]
__pdoc__ = {
    "PortLagSchema.resource": False,
    "PortLag": False,
}


class PortLagSchema(ResourceSchema):
    """The fields of the PortLag object"""

    active_ports = fields.Nested("PortSchema", unknown=EXCLUDE, many=True)
    r""" Active ports of a LAG (ifgrp). (Some member ports may be inactive.)
 """
    distribution_policy = fields.Str()
    r""" Policy for mapping flows to ports for outbound packets through a LAG (ifgrp).

Valid choices:

* port
* ip
* mac
* sequential """
    member_ports = fields.Nested("PortSchema", unknown=EXCLUDE, many=True)
    r""" The member_ports field of the port_lag.
 """
    mode = fields.Str()
    r""" Determines how the ports interact with the switch.

Valid choices:

* multimode_lacp
* multimode
* singlemode """

    @property
    def resource(self):
        return PortLag

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "distribution_policy",
            "member_ports",
            "mode",
        ]


class PortLag(Resource):  # pylint: disable=missing-docstring

    _schema = PortLagSchema
