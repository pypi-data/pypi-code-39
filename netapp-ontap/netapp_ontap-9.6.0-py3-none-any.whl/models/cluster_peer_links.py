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


__all__ = ["ClusterPeerLinks", "ClusterPeerLinksSchema"]
__pdoc__ = {
    "ClusterPeerLinksSchema.resource": False,
    "ClusterPeerLinks": False,
}


class ClusterPeerLinksSchema(ResourceSchema):
    """The fields of the ClusterPeerLinks object"""

    interfaces = fields.Nested("HrefSchema", unknown=EXCLUDE)
    r""" The interfaces field of the cluster_peer_links.
 """
    self_ = fields.Nested("HrefSchema", unknown=EXCLUDE)
    r""" The self_ field of the cluster_peer_links.
 """

    @property
    def resource(self):
        return ClusterPeerLinks

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "interfaces",
            "self_",
        ]


class ClusterPeerLinks(Resource):  # pylint: disable=missing-docstring

    _schema = ClusterPeerLinksSchema
