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


__all__ = ["NasApplicationComponents", "NasApplicationComponentsSchema"]
__pdoc__ = {
    "NasApplicationComponentsSchema.resource": False,
    "NasApplicationComponents": False,
}


class NasApplicationComponentsSchema(ResourceSchema):
    """The fields of the NasApplicationComponents object"""

    name = fields.Str()
    r""" The name of the application component. Optional in the POST or PATCH body
 """
    share_count = fields.Integer()
    r""" The number of shares in the application component. Optional in the POST body
 """
    storage_service = fields.Nested("NasStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the nas_application_components.
 """
    total_size = fields.Integer()
    r""" The total size of the application component, split across the member shares. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Optional in the POST or PATCH body
 """

    @property
    def resource(self):
        return NasApplicationComponents

    @property
    def patchable_fields(self):
        return [
            "name",
            "total_size",
        ]

    @property
    def postable_fields(self):
        return [
            "name",
            "share_count",
            "storage_service",
            "total_size",
        ]


class NasApplicationComponents(Resource):  # pylint: disable=missing-docstring

    _schema = NasApplicationComponentsSchema
