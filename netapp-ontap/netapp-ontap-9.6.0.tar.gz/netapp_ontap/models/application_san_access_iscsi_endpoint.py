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


__all__ = ["ApplicationSanAccessIscsiEndpoint", "ApplicationSanAccessIscsiEndpointSchema"]
__pdoc__ = {
    "ApplicationSanAccessIscsiEndpointSchema.resource": False,
    "ApplicationSanAccessIscsiEndpoint": False,
}


class ApplicationSanAccessIscsiEndpointSchema(ResourceSchema):
    """The fields of the ApplicationSanAccessIscsiEndpoint object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_san_access_iscsi_endpoint.
 """
    interface = fields.Nested("IpInterfaceSchema", unknown=EXCLUDE)
    r""" The interface field of the application_san_access_iscsi_endpoint.
 """
    port = fields.Integer()
    r""" The TCP port number of the iSCSI access endpoint.

Example: 3260 """

    @property
    def resource(self):
        return ApplicationSanAccessIscsiEndpoint

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "interface",
        ]


class ApplicationSanAccessIscsiEndpoint(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationSanAccessIscsiEndpointSchema
