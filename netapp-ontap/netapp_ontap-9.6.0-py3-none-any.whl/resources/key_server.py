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


__all__ = ["KeyServer", "KeyServerSchema"]
__pdoc__ = {
    "KeyServerSchema.resource": False,
    "KeyServerSchema.patchable_fields": False,
    "KeyServerSchema.postable_fields": False,
}


class KeyServerSchema(ResourceSchema):
    """The fields of the KeyServer object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the key_server.
 """
    password = fields.Str()
    r""" Password credentials for connecting with the key server. This is not audited.

Example: password """
    records = fields.List(fields.Nested("KeyServerNoRecordsSchema", unknown=EXCLUDE))
    r""" An array of key servers specified to add multiple key servers to a key manager in a single API call. Valid in POST only and not valid if `server` is provided.
 """
    server = fields.Str()
    r""" External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.

Example: keyserver1.com:5698 """
    timeout = fields.Integer(validate=integer_validation(minimum=1, maximum=60))
    r""" I/O timeout in seconds for communicating with the key server.

Example: 60 """
    username = fields.Str()
    r""" KMIP username credentials for connecting with the key server.

Example: username """

    @property
    def resource(self):
        return KeyServer

    @property
    def patchable_fields(self):
        return [
            "password",
            "timeout",
            "username",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "password",
            "records",
            "server",
        ]

class KeyServer(Resource):
    """Allows interaction with KeyServer objects on the host"""

    _schema = KeyServerSchema
    _path = "/api/security/key-managers/{security_key_manager[uuid]}/key-servers"
    @property
    def _keys(self):
        return ["security_key_manager.uuid", "server"]

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

    get_collection.__func__.__doc__ = r"""Retrieves key servers.
### Related ONTAP commands
* `security key-manager external show`
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

    patch_collection.__func__.__doc__ = r"""Updates a key server.
### Related ONTAP commands
* `security key-manager external modify-server`
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

    delete_collection.__func__.__doc__ = r"""Deletes a key server.
### Related ONTAP commands
* `security key-manager external remove-servers`
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves key servers.
### Related ONTAP commands
* `security key-manager external show`
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves key servers configured in an external key manager.
### Related ONTAP commands
* `security key-manager external show`
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

    post.__doc__ = r"""Adds key servers to a configured external key manager.
### Required properties
* `uuid` - UUID of the external key manager.
* `server` - Key server name.
### Related ONTAP commands
* `security key-manager external add-servers`
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

    patch.__doc__ = r"""Updates a key server.
### Related ONTAP commands
* `security key-manager external modify-server`
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

    delete.__doc__ = r"""Deletes a key server.
### Related ONTAP commands
* `security key-manager external remove-servers`
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



