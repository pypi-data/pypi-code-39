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


__all__ = ["JobLink", "JobLinkSchema"]
__pdoc__ = {
    "JobLinkSchema.resource": False,
    "JobLink": False,
}


class JobLinkSchema(ResourceSchema):
    """The fields of the JobLink object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the job_link.
 """
    uuid = fields.Str()
    r""" The UUID of the asynchronous job that is triggered by a POST, PATCH, or DELETE operation.
 """

    @property
    def resource(self):
        return JobLink

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class JobLink(Resource):  # pylint: disable=missing-docstring

    _schema = JobLinkSchema
