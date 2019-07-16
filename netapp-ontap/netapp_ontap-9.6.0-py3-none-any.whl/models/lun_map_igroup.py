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


__all__ = ["LunMapIgroup", "LunMapIgroupSchema"]
__pdoc__ = {
    "LunMapIgroupSchema.resource": False,
    "LunMapIgroup": False,
}


class LunMapIgroupSchema(ResourceSchema):
    """The fields of the LunMapIgroup object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the lun_map_igroup.
 """
    initiators = fields.List(fields.Str)
    r""" The initiators that are members of the initiator group.
 """
    name = fields.Str()
    r""" The name of the initiator group. Valid in POST.


Example: igroup1 """
    os_type = fields.Str()
    r""" The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system.


Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* vmware
* windows
* xen """
    protocol = fields.Str()
    r""" The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group.


Valid choices:

* fcp
* iscsi
* mixed """
    uuid = fields.Str()
    r""" The unique identifier of the initiator group. Valid in POST.


Example: 1ad8544d-8cd1-91e0-9e1c-723478563412 """

    @property
    def resource(self):
        return LunMapIgroup

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name",
            "uuid",
        ]


class LunMapIgroup(Resource):  # pylint: disable=missing-docstring

    _schema = LunMapIgroupSchema
