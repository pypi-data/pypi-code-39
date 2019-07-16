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


__all__ = ["FpolicyEventFilters", "FpolicyEventFiltersSchema"]
__pdoc__ = {
    "FpolicyEventFiltersSchema.resource": False,
    "FpolicyEventFilters": False,
}


class FpolicyEventFiltersSchema(ResourceSchema):
    """The fields of the FpolicyEventFilters object"""

    close_with_modification = fields.Boolean()
    r""" Filter the client request for close with modification.
 """
    close_with_read = fields.Boolean()
    r""" Filter the client request for close with read.
 """
    close_without_modification = fields.Boolean()
    r""" Filter the client request for close without modification.
 """
    exclude_directory = fields.Boolean()
    r""" Filter the client requests for directory operations. When this filter is specified directory operations are not monitored.
 """
    first_read = fields.Boolean()
    r""" Filter the client requests for the first-read.
 """
    first_write = fields.Boolean()
    r""" Filter the client requests for the first-write.
 """
    monitor_ads = fields.Boolean()
    r""" Filter the client request for alternate data stream.
 """
    offline_bit = fields.Boolean()
    r""" Filter the client request for offline bit set. FPolicy server receives notification only when offline files are accessed.
 """
    open_with_delete_intent = fields.Boolean()
    r""" Filter the client request for open with delete intent.
 """
    open_with_write_intent = fields.Boolean()
    r""" Filter the client request for open with write intent.
 """
    setattr_with_access_time_change = fields.Boolean()
    r""" Filter the client setattr requests for changing the access time of a file or directory.
 """
    setattr_with_allocation_size_change = fields.Boolean()
    r""" Filter the client setattr requests for changing the allocation size of a file.
 """
    setattr_with_creation_time_change = fields.Boolean()
    r""" Filter the client setattr requests for changing the creation time of a file or directory.
 """
    setattr_with_dacl_change = fields.Boolean()
    r""" Filter the client setattr requests for changing dacl on a file or directory.
 """
    setattr_with_group_change = fields.Boolean()
    r""" Filter the client setattr requests for changing group of a file or directory.
 """
    setattr_with_mode_change = fields.Boolean()
    r""" Filter the client setattr requests for changing the mode bits on a file or directory.
 """
    setattr_with_modify_time_change = fields.Boolean()
    r""" Filter the client setattr requests for changing the modification time of a file or directory.
 """
    setattr_with_owner_change = fields.Boolean()
    r""" Filter the client setattr requests for changing owner of a file or directory.
 """
    setattr_with_sacl_change = fields.Boolean()
    r""" Filter the client setattr requests for changing sacl on a file or directory.
 """
    setattr_with_size_change = fields.Boolean()
    r""" Filter the client setattr requests for changing the size of a file.
 """
    write_with_size_change = fields.Boolean()
    r""" Filter the client request for write with size change.
 """

    @property
    def resource(self):
        return FpolicyEventFilters

    @property
    def patchable_fields(self):
        return [
            "close_with_modification",
            "close_with_read",
            "close_without_modification",
            "exclude_directory",
            "first_read",
            "first_write",
            "monitor_ads",
            "offline_bit",
            "open_with_delete_intent",
            "open_with_write_intent",
            "setattr_with_access_time_change",
            "setattr_with_allocation_size_change",
            "setattr_with_creation_time_change",
            "setattr_with_dacl_change",
            "setattr_with_group_change",
            "setattr_with_mode_change",
            "setattr_with_modify_time_change",
            "setattr_with_owner_change",
            "setattr_with_sacl_change",
            "setattr_with_size_change",
            "write_with_size_change",
        ]

    @property
    def postable_fields(self):
        return [
            "close_with_modification",
            "close_with_read",
            "close_without_modification",
            "exclude_directory",
            "first_read",
            "first_write",
            "monitor_ads",
            "offline_bit",
            "open_with_delete_intent",
            "open_with_write_intent",
            "setattr_with_access_time_change",
            "setattr_with_allocation_size_change",
            "setattr_with_creation_time_change",
            "setattr_with_dacl_change",
            "setattr_with_group_change",
            "setattr_with_mode_change",
            "setattr_with_modify_time_change",
            "setattr_with_owner_change",
            "setattr_with_sacl_change",
            "setattr_with_size_change",
            "write_with_size_change",
        ]


class FpolicyEventFilters(Resource):  # pylint: disable=missing-docstring

    _schema = FpolicyEventFiltersSchema
