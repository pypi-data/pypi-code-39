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


__all__ = ["SoftwareMessageCatalog", "SoftwareMessageCatalogSchema"]
__pdoc__ = {
    "SoftwareMessageCatalogSchema.resource": False,
    "SoftwareMessageCatalog": False,
}


class SoftwareMessageCatalogSchema(ResourceSchema):
    """The fields of the SoftwareMessageCatalog object"""

    arguments = fields.List(fields.Str)
    r""" The arguments field of the software_message_catalog.
 """
    code = fields.Integer()
    r""" Message catalog code of message

Example: 177 """
    message = fields.Str()
    r""" message details

Example: Installing Data ONTAP software image on cluster 'clusA' """

    @property
    def resource(self):
        return SoftwareMessageCatalog

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class SoftwareMessageCatalog(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwareMessageCatalogSchema
