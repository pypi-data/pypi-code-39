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


__all__ = ["SnapmirrorEndpoint", "SnapmirrorEndpointSchema"]
__pdoc__ = {
    "SnapmirrorEndpointSchema.resource": False,
    "SnapmirrorEndpoint": False,
}


class SnapmirrorEndpointSchema(ResourceSchema):
    """The fields of the SnapmirrorEndpoint object"""

    path = fields.Str()
    r""" ONTAP FlexVol/FlexGroup - svm1:volume1
ONTAP SVM               - svm1:


Example: svm1:volume1 """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the snapmirror_endpoint.
 """

    @property
    def resource(self):
        return SnapmirrorEndpoint

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "path",
            "svm",
        ]


class SnapmirrorEndpoint(Resource):  # pylint: disable=missing-docstring

    _schema = SnapmirrorEndpointSchema
