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


__all__ = ["ApplicationComponentSnapshot", "ApplicationComponentSnapshotSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotSchema.resource": False,
    "ApplicationComponentSnapshotSchema.patchable_fields": False,
    "ApplicationComponentSnapshotSchema.postable_fields": False,
}


class ApplicationComponentSnapshotSchema(ResourceSchema):
    """The fields of the ApplicationComponentSnapshot object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the application_component_snapshot.
 """
    application = fields.Nested("ApplicationComponentSnapshotApplicationSchema", unknown=EXCLUDE)
    r""" The application field of the application_component_snapshot.
 """
    comment = fields.Str(validate=len_validation(minimum=0, maximum=255))
    r""" Comment. Valid in POST
 """
    component = fields.Nested("ApplicationComponentSnapshotComponentSchema", unknown=EXCLUDE)
    r""" The component field of the application_component_snapshot.
 """
    consistency_type = fields.Str(validate=enum_validation(['crash', 'application']))
    r""" Consistency Type. This is for categorization only. A snapshot should not be set to application consistent unless the host application is quiesced for the snapshot. Valid in POST

Valid choices:

* crash
* application """
    create_time = fields.Str()
    r""" Creation Time
 """
    is_partial = fields.Boolean()
    r""" A partial snapshot means that not all volumes in an application component were included in the snapshot.
 """
    name = fields.Str()
    r""" Snapshot Name. Valid in POST
 """
    svm = fields.Nested("ApplicationComponentSnapshotSvmSchema", unknown=EXCLUDE)
    r""" The svm field of the application_component_snapshot.
 """
    uuid = fields.Str()
    r""" Snapshot UUID. Valid in URL
 """

    @property
    def resource(self):
        return ApplicationComponentSnapshot

    @property
    def patchable_fields(self):
        return [
            "comment",
            "consistency_type",
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "application",
            "comment",
            "component",
            "consistency_type",
            "name",
            "svm",
        ]

class ApplicationComponentSnapshot(Resource):
    """Allows interaction with ApplicationComponentSnapshot objects on the host"""

    _schema = ApplicationComponentSnapshotSchema
    _path = "/api/application/applications/{application[uuid]}/components/{component[uuid]}/snapshots"
    @property
    def _keys(self):
        return ["application.uuid", "component.uuid", "uuid"]

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

    get_collection.__func__.__doc__ = r"""Retrieves Snapshot copies of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component Snapshot copies are essentially more granular application Snapshot copies. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_collection_get)
* [`DOC /application`](#docs-application-overview)
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

    delete_collection.__func__.__doc__ = r"""Delete a Snapshot copy of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component Snapshot copies are essentially more granular application Snapshot copies. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`DELETE /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_delete)
* [`DOC /application`](#docs-application-overview)
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves Snapshot copies of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component Snapshot copies are essentially more granular application Snapshot copies. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_collection_get)
* [`DOC /application`](#docs-application-overview)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieve a Snapshot copy of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component Snapshot copies are essentially more granular application Snapshot copies. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_get)
* [`DOC /application`](#docs-application-overview)
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

    post.__doc__ = r"""Creates a Snapshot copy of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
### Required properties
* `name`
### Recommended optional properties
* `consistency_type` - Track whether this snapshot is _application_ or _crash_ consistent.
Component Snapshot copies are essentially more granular application Snapshot copies. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_create)
* [`DOC /application`](#docs-application-overview)
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

    delete.__doc__ = r"""Delete a Snapshot copy of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component Snapshot copies are essentially more granular application Snapshot copies. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`DELETE /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_delete)
* [`DOC /application`](#docs-application-overview)
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    # pylint: disable=missing-docstring
    # pylint: disable=bad-continuation
    def restore(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ = r"""Restore a Snapshot copy of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component Snapshot copies are essentially more granular application Snapshot copies. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`POST /application/applications/{application.uuid}/snapshots/{uuid}/restore`](#operations-application-application_snapshot_restore)
* [`DOC /application`](#docs-application-overview)
* [`DOC Asynchronous operations`](#docs-docs-Synchronous-and-asynchronous-operations)
"""
    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)


