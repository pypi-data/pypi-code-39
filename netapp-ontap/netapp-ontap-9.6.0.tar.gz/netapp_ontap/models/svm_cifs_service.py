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


__all__ = ["SvmCifsService", "SvmCifsServiceSchema"]
__pdoc__ = {
    "SvmCifsServiceSchema.resource": False,
    "SvmCifsService": False,
}


class SvmCifsServiceSchema(ResourceSchema):
    """The fields of the SvmCifsService object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the svm_cifs_service.
 """
    ad_domain = fields.Nested("AdDomainSvmSchema", unknown=EXCLUDE)
    r""" The ad_domain field of the svm_cifs_service.
 """
    enabled = fields.Boolean()
    r""" Specifies whether or not the CIFS service is administratively enabled.
 """
    name = fields.Str()
    r""" The NetBIOS name of the CIFS server.

Example: CIFS1 """

    @property
    def resource(self):
        return SvmCifsService

    @property
    def patchable_fields(self):
        return [
            "enabled",
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "ad_domain",
            "enabled",
            "name",
        ]


class SvmCifsService(Resource):  # pylint: disable=missing-docstring

    _schema = SvmCifsServiceSchema
