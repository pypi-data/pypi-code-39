# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Retrieving a collection of cloud targets
The cloud targets GET API retrieves all cloud targets defined in the cluster.
## Creating cloud targets
The cluster administrator tells ONTAP how to connect to a cloud target. The following pre-requisites must be met before creating an object store configuration in ONTAP.
A valid data bucket or container must be created with the object store provider. This assumes that the user has valid account credentials with the object store provider to access the data bucket.
The ONTAP node must be able to connect to the object store. </br>
This includes:
  - Fast, reliable connectivity to the object store.
  - An inter-cluster LIF (logical interface) must be configured on the cluster. ONTAP verifies connectivity prior to saving this configuration information.
  - If SSL/TLS authentication is required, then valid certificates must be installed.
  - FabricPool license (required for all object stores except SGWS).
## Deleting cloud targets
If a cloud target is used by an aggregate, then the aggregate must be deleted before the cloud target can be deleted.
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["CloudTarget", "CloudTargetSchema"]
__pdoc__ = {
    "CloudTargetSchema.resource": False,
    "CloudTargetSchema.patchable_fields": False,
    "CloudTargetSchema.postable_fields": False,
}


class CloudTargetSchema(ResourceSchema):
    """The fields of the CloudTarget object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the cloud_target.
 """
    access_key = fields.Str()
    r""" Access key ID for AWS_S3 and other S3 compatible provider types.
 """
    authentication_type = fields.Str(validate=enum_validation(['key', 'cap', 'ec2_iam']))
    r""" Authentication used to access the target. Snapmirror does not yet support CAP. Required in POST.

Valid choices:

* key
* cap
* ec2_iam """
    azure_account = fields.Str()
    r""" Azure account
 """
    azure_private_key = fields.Str()
    r""" Azure access key
 """
    cap_url = fields.Str()
    r""" This parameter is available only when auth-type is CAP. It specifies a full URL of the request to a CAP server for retrieving temporary credentials (access-key, secret-pasword, and session token) for accessing the object store.

Example: https://123.45.67.89:1234/CAP/api/v1/credentials?agency=myagency&mission=mymission&role=myrole """
    certificate_validation_enabled = fields.Boolean()
    r""" Is SSL/TLS certificate validation enabled? The default value is true. This can only be modified for SGWS and IBM_COS provider types.
 """
    container = fields.Str()
    r""" Data bucket/container name

Example: bucket1 """
    ipspace = fields.Nested("IpspaceSchema", unknown=EXCLUDE)
    r""" The ipspace field of the cloud_target.
 """
    name = fields.Str()
    r""" Cloud target name
 """
    owner = fields.Str(validate=enum_validation(['fabricpool', 'snapmirror']))
    r""" Owner of the target. Allowed values are FabricPool or SnapMirror. A target can be used by only one feature.

Valid choices:

* fabricpool
* snapmirror """
    port = fields.Integer()
    r""" Port number of the object store that ONTAP uses when establishing a connection. Required in POST.
 """
    provider_type = fields.Str()
    r""" Type of cloud provider. Allowed values depend on owner type. For FabricPool, AliCloud, AWS_S3, Azure_Cloud, GoggleCloud, IBM_COS, and SGWS are allowed. For SnapMirror, the valid values are AWS_S3 or SGWS.
 """
    secret_password = fields.Str()
    r""" Secret access key for AWS_S3 and other S3 compatible provider types.
 """
    server = fields.Str()
    r""" Fully qualified domain name of the object store server. Required on POST.  For Amazon S3, server name must be an AWS regional endpoint in the format s3.amazonaws.com or s3-<region>.amazonaws.com, for example, s3-us-west-2.amazonaws.com. The region of the server and the bucket must match. For Azure, if the server is a "blob.core.windows.net" or a "blob.core.usgovcloudapi.net", then a value of azure-account followed by a period is added in front of the server.
 """
    snapmirror_use = fields.Str(validate=enum_validation(['data', 'metadata']))
    r""" Use of the cloud target by SnapMirror.

Valid choices:

* data
* metadata """
    ssl_enabled = fields.Boolean()
    r""" SSL/HTTPS enabled or not
 """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the cloud_target.
 """
    used = fields.Integer()
    r""" The amount of cloud space used by all the aggregates attached to the target, in bytes. This field is only populated for FabricPool targets. The value is recalculated once every 5 minutes.
 """
    uuid = fields.Str()
    r""" Cloud target UUID
 """

    @property
    def resource(self):
        return CloudTarget

    @property
    def patchable_fields(self):
        return [
            "access_key",
            "authentication_type",
            "azure_account",
            "azure_private_key",
            "cap_url",
            "certificate_validation_enabled",
            "name",
            "port",
            "secret_password",
            "server",
            "snapmirror_use",
            "ssl_enabled",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "access_key",
            "authentication_type",
            "azure_account",
            "azure_private_key",
            "cap_url",
            "certificate_validation_enabled",
            "container",
            "ipspace",
            "name",
            "owner",
            "port",
            "provider_type",
            "secret_password",
            "server",
            "snapmirror_use",
            "ssl_enabled",
            "svm",
        ]

class CloudTarget(Resource):
    """Allows interaction with CloudTarget objects on the host"""

    _schema = CloudTargetSchema
    _path = "/api/cloud/targets"
    @property
    def _keys(self):
        return ["uuid"]

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

    get_collection.__func__.__doc__ = r"""Retrieves the collection of cloud targets in the cluster.
### Related ONTAP commands
* `storage aggregate object-store config show`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
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

    patch_collection.__func__.__doc__ = r"""Updates the cloud target specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config modify`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
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

    delete_collection.__func__.__doc__ = r"""Deletes the cloud target specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config delete`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves the collection of cloud targets in the cluster.
### Related ONTAP commands
* `storage aggregate object-store config show`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the cloud target specified by the UUID.
### Related ONTAP commands
* `storage aggregate object-store config show`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
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

    post.__doc__ = r"""Creates a cloud target.
### Required properties
* `name` - Name for the cloud target.
* `owner` - Owner of the target: _fabricpool_, _snapmirror_.
* `provider_type` - Type of cloud provider: _AWS_S3_, _Azure_Cloud_, _SGWS_, _IBM_COS_, _AliCloud_, _GoogleCloud_.
* `server` - Fully qualified domain name of the object store server. Required when `provider_type` is one of the following: _SGWS_, _IBM_COS_, _AliCloud_.
* `container` - Data bucket/container name.
* `access_key` - Access key ID if `provider_type` is not _Azure_Cloud_ and `authentication_type` is _key_.
* `secret_password` - Secret access key if `provider_type` is not _Azure_Cloud_ and `authentication_type` is _key_.
* `azure_account` - Azure account if `provider_type` is _Azure_Cloud_.
* `azure_private_key` - Azure access key if `provider_type` is _Azure_Cloud_.
* `cap_url` - Full URL of the request to a CAP server for retrieving temporary credentials if `authentication_type` is _cap_.
* `svm.name` or `svm.uuid` - Name or UUID of SVM if `owner` is _snapmirror_.
* `snapmirror_use` - Use of the cloud target if `owner` is _snapmirror_: data, metadata.
### Recommended optional properties
* `authentication_type` - Authentication used to access the target: _key_, _cap_, _ec2_iam_.
* `ssl_enabled` - SSL/HTTPS enabled or disabled.
* `port` - Port number of the object store that ONTAP uses when establishing a connection.
* `ipspace` - IPspace to use in order to reach the cloud target.
### Default property values
* `authentication_type`
  - _ec2_iam_ - if running in Cloud Volumes ONTAP in AWS
  - _key_  - in all other cases.
* `server`
  - _s3.amazonaws.com_ - if `provider_type` is _AWS_S3_
  - _blob.core.windows.net_ - if `provider_type` is _Azure_Cloud_
  - _storage.googleapis.com_ - if `provider_type` is _GoogleCloud_
* `ssl_enabled` - _true_
* `port`
  - _443_ if `ssl_enabled` is _true_ and `provider_type` is not _SGWS_
  - _8082_ if `ssl_enabled` is _true_ and `provider_type` is _SGWS_
  - _80_ if `ssl_enabled` is _false_ and `provider_type` is not _SGWS_
  - _8084_ if `ssl_enabled` is _false_ and `provider_type` is _SGWS_
* `ipspace` - _Default_
* `certificate_validation_enabled` - _true_
* `ignore_warnings` - _false_
* `check_only` - _false_
### Related ONTAP commands
* `storage aggregate object-store config create`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
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

    patch.__doc__ = r"""Updates the cloud target specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config modify`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
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

    delete.__doc__ = r"""Deletes the cloud target specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config delete`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



