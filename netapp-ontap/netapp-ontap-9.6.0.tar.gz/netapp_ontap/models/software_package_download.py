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


__all__ = ["SoftwarePackageDownload", "SoftwarePackageDownloadSchema"]
__pdoc__ = {
    "SoftwarePackageDownloadSchema.resource": False,
    "SoftwarePackageDownload": False,
}


class SoftwarePackageDownloadSchema(ResourceSchema):
    """The fields of the SoftwarePackageDownload object"""

    password = fields.Str()
    r""" Password for download

Example: admin_password """
    url = fields.Str()
    r""" HTTP or FTP URL of the package via a server

Example: http://server/package """
    username = fields.Str()
    r""" Username for download

Example: admin """

    @property
    def resource(self):
        return SoftwarePackageDownload

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "password",
            "url",
            "username",
        ]


class SoftwarePackageDownload(Resource):  # pylint: disable=missing-docstring

    _schema = SoftwarePackageDownloadSchema
