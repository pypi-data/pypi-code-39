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


__all__ = ["ApplicationRpo", "ApplicationRpoSchema"]
__pdoc__ = {
    "ApplicationRpoSchema.resource": False,
    "ApplicationRpo": False,
}


class ApplicationRpoSchema(ResourceSchema):
    """The fields of the ApplicationRpo object"""

    components = fields.Nested("ApplicationRpoComponentsSchema", unknown=EXCLUDE, many=True)
    r""" The components field of the application_rpo.
 """
    is_supported = fields.Boolean()
    r""" Is RPO supported for this application? Generation 1 applications did not support snapshots or MetroCluster
 """
    local = fields.Nested("ApplicationRpoLocalSchema", unknown=EXCLUDE)
    r""" The local field of the application_rpo.
 """
    remote = fields.Nested("ApplicationRpoRemoteSchema", unknown=EXCLUDE)
    r""" The remote field of the application_rpo.
 """

    @property
    def resource(self):
        return ApplicationRpo

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "local",
            "remote",
        ]


class ApplicationRpo(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationRpoSchema
