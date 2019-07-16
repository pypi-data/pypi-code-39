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


__all__ = ["NvmeSubsystemHost", "NvmeSubsystemHostSchema"]
__pdoc__ = {
    "NvmeSubsystemHostSchema.resource": False,
    "NvmeSubsystemHostSchema.patchable_fields": False,
    "NvmeSubsystemHostSchema.postable_fields": False,
}


class NvmeSubsystemHostSchema(ResourceSchema):
    """The fields of the NvmeSubsystemHost object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the nvme_subsystem_host.
 """
    io_queue = fields.Nested("NvmeSubsystemHostIoQueueSchema", unknown=EXCLUDE)
    r""" The io_queue field of the nvme_subsystem_host.
 """
    nqn = fields.Str()
    r""" The NVMe qualified name (NQN) used to identify the NVMe storage target. Not allowed in POST when the `records` property is used.


Example: nqn.1992-01.example.com:string """
    records = fields.List(fields.Nested("NvmeSubsystemHostNoRecordsSchema", unknown=EXCLUDE))
    r""" An array of NVMe hosts specified to add multiple NVMe hosts to an NVMe subsystem in a single API call. Valid in POST only.
 """
    subsystem = fields.Nested("NvmeSubsystemHostSubsystemSchema", unknown=EXCLUDE)
    r""" The subsystem field of the nvme_subsystem_host.
 """

    @property
    def resource(self):
        return NvmeSubsystemHost

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "io_queue",
            "nqn",
            "records",
            "subsystem",
        ]

class NvmeSubsystemHost(Resource):
    r""" The NVMe host provisioned to access NVMe namespaces mapped to a subsystem.
 """

    _schema = NvmeSubsystemHostSchema
    _path = "/api/protocols/nvme/subsystems/{subsystem[uuid]}/hosts"
    @property
    def _keys(self):
        return ["subsystem.uuid", "nqn"]

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

    get_collection.__func__.__doc__ = r"""Retrieves the NVMe subsystem hosts of an NVMe subsystem.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `subsystem_maps.*`
### Related ONTAP commands
* `vserver nvme subsystem map show`
* `vserver nvme subsystem show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    # pylint: disable=bad-continuation
    # pylint: disable=missing-docstring
    @classmethod
    def delete_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._delete_collection(*args, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ = r"""Deletes an NVMe subsystem host from an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host remove`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the NVMe subsystem hosts of an NVMe subsystem.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`DOC Requesting specific fields`](#docs-docs-Requesting-specific-fields) to learn more.
* `subsystem_maps.*`
### Related ONTAP commands
* `vserver nvme subsystem map show`
* `vserver nvme subsystem show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves an NVMe subsystem host of an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    # pylint: disable=missing-docstring
    # pylint: disable=bad-continuation
    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ = r"""Adds NVMe subsystem host(s) to an NVMe subsystem.
### Required properties
* `nqn` or `records.nqn` - NVMe host(s) NQN(s) to add to the NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host add`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    # pylint: disable=missing-docstring
    # pylint: disable=bad-continuation
    def delete(
        self,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._delete(
            poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ = r"""Deletes an NVMe subsystem host from an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host remove`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



