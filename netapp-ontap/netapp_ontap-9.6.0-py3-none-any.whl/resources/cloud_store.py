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


__all__ = ["CloudStore", "CloudStoreSchema"]
__pdoc__ = {
    "CloudStoreSchema.resource": False,
    "CloudStoreSchema.patchable_fields": False,
    "CloudStoreSchema.postable_fields": False,
}


class CloudStoreSchema(ResourceSchema):
    """The fields of the CloudStore object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the cloud_store.
 """
    availability = fields.Str(validate=enum_validation(['available', 'unavailable']))
    r""" Availability of the object store.

Valid choices:

* available
* unavailable """
    mirror_degraded = fields.Boolean()
    r""" This field identifies if the mirror cloud store is in sync with the primary cloud store of a FabricPool.
 """
    primary = fields.Boolean()
    r""" This field indicates whether the cloud store is the primary cloud store of a cloud mirrored composite aggregate.
 """
    target = fields.Nested("CloudTargetSchema", unknown=EXCLUDE)
    r""" The target field of the cloud_store.
 """
    unreclaimed_space_threshold = fields.Integer()
    r""" Usage threshold for reclaiming unused space in the cloud store. Valid values are 0 to 99. The default value depends on the provider type. This can be specified in PATCH but not POST.

Example: 20 """
    used = fields.Integer()
    r""" The amount of object space used. Calculated every 5 minutes and cached.
 """

    @property
    def resource(self):
        return CloudStore

    @property
    def patchable_fields(self):
        return [
            "primary",
            "unreclaimed_space_threshold",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "primary",
            "target",
            "unreclaimed_space_threshold",
        ]

class CloudStore(Resource):
    """Allows interaction with CloudStore objects on the host"""

    _schema = CloudStoreSchema
    _path = "/api/storage/aggregates/{aggregate[uuid]}/cloud-stores"
    @property
    def _keys(self):
        return ["aggregate.uuid", "target.uuid"]

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

    get_collection.__func__.__doc__ = r"""Retrieves the collection of cloud stores used by an aggregate.
### Related ONTAP commands
* `storage aggregate object-store show`
"""
    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    # pylint: disable=bad-continuation
    # pylint: disable=missing-docstring
    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._patch_collection(body, *args, connection=connection, **kwargs)

    patch_collection.__func__.__doc__ = r"""Updates the cloud store specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store modify`
"""
    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

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

    delete_collection.__func__.__doc__ = r"""Removes the specified cloud target from the aggregate. Only removal of a mirror is allowed. The primary cannot be removed. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store unmirror`
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the collection of cloud stores used by an aggregate.
### Related ONTAP commands
* `storage aggregate object-store show`
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the cloud store for the aggregate using the specified cloud target UUID.
### Related ONTAP commands
* `storage aggregate object-store show`
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

    post.__doc__ = r"""Attaches an object store to an aggregate, or adds a second object store as a mirror.
### Required properties
* `target.uuid` or `target.name` - UUID or name of the cloud target.
### Recommended optional properties
* `primary` - _true_ if the object store is primary or _false_ if it is a mirror.
* `allow_flexgroups` - Allow attaching object store to an aggregate containing FlexGroup constituents.
* `check_only` - Validate only and do not add the cloud store.
### Default property values
* `primary` - _true_
* `allow_flexgroups` - _false_
* `check_only` - _false_
### Related ONTAP commands
* `storage aggregate object-store attach`
* `storage aggregate object-store mirror`
"""
    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    # pylint: disable=missing-docstring
    # pylint: disable=bad-continuation
    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ = r"""Updates the cloud store specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store modify`
"""
    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

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

    delete.__doc__ = r"""Removes the specified cloud target from the aggregate. Only removal of a mirror is allowed. The primary cannot be removed. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store unmirror`
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



