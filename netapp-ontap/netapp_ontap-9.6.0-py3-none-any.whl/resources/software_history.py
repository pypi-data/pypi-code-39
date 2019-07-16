# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.


"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SoftwareHistory", "SoftwareHistorySchema"]
__pdoc__ = {
    "SoftwareHistorySchema.resource": False,
    "SoftwareHistorySchema.patchable_fields": False,
    "SoftwareHistorySchema.postable_fields": False,
}


class SoftwareHistorySchema(ResourceSchema):
    """The fields of the SoftwareHistory object"""

    links = fields.Nested("CollectionLinksSchema", unknown=EXCLUDE)
    r""" The links field of the software_history.
 """
    num_records = fields.Integer()
    r""" The num_records field of the software_history.
 """
    records = fields.List(fields.Nested("SoftwareHistorySchema", unknown=EXCLUDE))
    r""" The records field of the software_history.
 """

    @property
    def resource(self):
        return SoftwareHistory

    @property
    def patchable_fields(self):
        return [
            "num_records",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "num_records",
            "records",
        ]

class SoftwareHistory(Resource):
    """Allows interaction with SoftwareHistory objects on the host"""

    _schema = SoftwareHistorySchema
    _path = "/api/cluster/software/history"

    # pylint: disable=bad-continuation
    # pylint: disable=missing-docstring
    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ = r"""Retrieves the history details for software installation requests.
### Related ONTAP commands
* `cluster image show-update-history`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the history details for software installation requests.
### Related ONTAP commands
* `cluster image show-update-history`
### Learn more
* [`DOC /cluster/software`](#docs-cluster-cluster_software)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)







