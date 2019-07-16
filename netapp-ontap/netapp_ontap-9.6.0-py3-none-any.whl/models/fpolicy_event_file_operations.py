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


__all__ = ["FpolicyEventFileOperations", "FpolicyEventFileOperationsSchema"]
__pdoc__ = {
    "FpolicyEventFileOperationsSchema.resource": False,
    "FpolicyEventFileOperations": False,
}


class FpolicyEventFileOperationsSchema(ResourceSchema):
    """The fields of the FpolicyEventFileOperations object"""

    close = fields.Boolean()
    r""" File close operations
 """
    create = fields.Boolean()
    r""" File create operations
 """
    create_dir = fields.Boolean()
    r""" Directory create operations
 """
    delete = fields.Boolean()
    r""" File delete operations
 """
    delete_dir = fields.Boolean()
    r""" Directory delete operations
 """
    getattr = fields.Boolean()
    r""" Get attribute operations
 """
    link = fields.Boolean()
    r""" Link operations
 """
    lookup = fields.Boolean()
    r""" Lookup operations
 """
    open = fields.Boolean()
    r""" File open operations
 """
    read = fields.Boolean()
    r""" File read operations
 """
    rename = fields.Boolean()
    r""" File rename operations
 """
    rename_dir = fields.Boolean()
    r""" Directory rename operations
 """
    setattr = fields.Boolean()
    r""" Set attribute operations
 """
    symlink = fields.Boolean()
    r""" Symbolic link operations
 """
    write = fields.Boolean()
    r""" File write operations
 """

    @property
    def resource(self):
        return FpolicyEventFileOperations

    @property
    def patchable_fields(self):
        return [
            "close",
            "create",
            "create_dir",
            "delete",
            "delete_dir",
            "getattr",
            "link",
            "lookup",
            "open",
            "read",
            "rename",
            "rename_dir",
            "setattr",
            "symlink",
            "write",
        ]

    @property
    def postable_fields(self):
        return [
            "close",
            "create",
            "create_dir",
            "delete",
            "delete_dir",
            "getattr",
            "link",
            "lookup",
            "open",
            "read",
            "rename",
            "rename_dir",
            "setattr",
            "symlink",
            "write",
        ]


class FpolicyEventFileOperations(Resource):  # pylint: disable=missing-docstring

    _schema = FpolicyEventFileOperationsSchema
