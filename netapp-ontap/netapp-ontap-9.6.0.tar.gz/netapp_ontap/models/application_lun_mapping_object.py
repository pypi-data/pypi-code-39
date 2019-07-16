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


__all__ = ["ApplicationLunMappingObject", "ApplicationLunMappingObjectSchema"]
__pdoc__ = {
    "ApplicationLunMappingObjectSchema.resource": False,
    "ApplicationLunMappingObject": False,
}


class ApplicationLunMappingObjectSchema(ResourceSchema):
    """The fields of the ApplicationLunMappingObject object"""

    fcp = fields.Nested("ApplicationSanAccessFcpEndpointSchema", unknown=EXCLUDE, many=True)
    r""" All possible Fibre Channel Protocol (FCP) access endpoints for the LUN.
 """
    igroup = fields.Nested("ApplicationLunMappingObjectIgroupSchema", unknown=EXCLUDE)
    r""" The igroup field of the application_lun_mapping_object.
 """
    iscsi = fields.Nested("ApplicationSanAccessIscsiEndpointSchema", unknown=EXCLUDE, many=True)
    r""" All possible iSCSI access endpoints for the LUN.
 """
    lun_id = fields.Integer()
    r""" LUN ID
 """

    @property
    def resource(self):
        return ApplicationLunMappingObject

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "igroup",
        ]


class ApplicationLunMappingObject(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationLunMappingObjectSchema
