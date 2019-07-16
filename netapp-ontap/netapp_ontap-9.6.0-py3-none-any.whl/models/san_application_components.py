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


__all__ = ["SanApplicationComponents", "SanApplicationComponentsSchema"]
__pdoc__ = {
    "SanApplicationComponentsSchema.resource": False,
    "SanApplicationComponents": False,
}


class SanApplicationComponentsSchema(ResourceSchema):
    """The fields of the SanApplicationComponents object"""

    igroup_name = fields.Str()
    r""" The name of the initiator group through which the contents of this application will be accessed. Modification of this parameter is a disruptive operation. All LUNs in the application component will be unmapped from the current igroup and re-mapped to the new igroup. Optional in the POST or PATCH body
 """
    lun_count = fields.Integer()
    r""" The number of LUNs in the application component. Optional in the POST body
 """
    name = fields.Str()
    r""" The name of the application component. Optional in the POST or PATCH body
 """
    storage_service = fields.Nested("NasStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the san_application_components.
 """
    total_size = fields.Integer()
    r""" The total size of the application component, split across the member LUNs. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Optional in the POST or PATCH body
 """

    @property
    def resource(self):
        return SanApplicationComponents

    @property
    def patchable_fields(self):
        return [
            "igroup_name",
            "name",
            "total_size",
        ]

    @property
    def postable_fields(self):
        return [
            "igroup_name",
            "lun_count",
            "name",
            "storage_service",
            "total_size",
        ]


class SanApplicationComponents(Resource):  # pylint: disable=missing-docstring

    _schema = SanApplicationComponentsSchema
