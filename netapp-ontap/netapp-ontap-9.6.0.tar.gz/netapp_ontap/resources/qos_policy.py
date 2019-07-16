# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Quality of Service Configuration
A QoS policy defines measurable service level objectives (SLOs) that apply to the storage objects with which the policy is associated. There are two types of policies that can be configured, fixed which define a fixed SLO, or adaptive which defines a variable SLO for a storage object. Adaptive policies vary the SLO depending on the space usage of the storage object. A policy can be either a fixed policy or an adaptive one not both.
<br />
Service level objectives include minimum and maximum limits on throughput in terms of IOPS. Only maximum limits can be set in terms of both IOPS and/or throughput (MB/s). A QoS policy can be used to enforce SLOs for multiple storage objects by specifying "capacity_shared" to true. For e.g. if a QoS policy with "capacity_shared" is set to true and it has maximum_throughput_iops set to 1000, and this policy is assigned to four volumes, then the combined throughput of all four volumes would be limited to 1000 IOPS. If "capacity_shared" is set to false then, each storage object will have it's SLOs enforced individually. For e.g. In the previous case if the same policy were applied to four volumes but with "capacity_shared" set to false, then each of the volumes would be limited to 1000 IOPS individually. Once "capacity_shared" is set it cannot be modified.
<br />
Adaptive parameters can specify the variable SLOs in terms of IOPS/TB, the actual IOPS enforced on the storage object can be calculated using the allocated space on the storage object. The policies are enforced individually amongst storage objects.
## Examples
### 1) Create a fixed QoS policy
The following example shows how to create a fixed QoS policy to limit throughput for a storage object between 5000 IOPS and 10000 IOPS which has capacity_shared set to false. This QoS policy can be used as a template to apply on multiple storage objects to provide individual SLOs to each object.
<br />
---
```
curl -X POST "https://172.21.69.245/api/storage/qos/policies?return_timeout=0" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"fixed\": { \"capacity_shared\": false, \"max_throughput_iops\": 10000, \"min_throughput_iops\": 5000 }, \"name\": \"qos_policy_5000_to_10000_iops\", \"svm\": { \"name\": \"vs0\" }}"
```
---
### 2) Create an adaptive QoS policy
The following example shows how to create an adaptive QoS policy which would provide 5000 IOPS per GB of allocated space for a storage object with a peak of 6000 IOPS. Minimum IOPS regardless of allocated space would be 1000 IOPS.
<br />
---
```
curl -X POST "https://172.21.69.245/api/storage/qos/policies?return_timeout=0" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"adaptive\": { \"absolute_min_iops\": 1000, \"expected_iops\": 5000, \"peak_iops\": 6000 }, \"name\": \"adaptive_pg_5k_to_6k\", \"svm\": { \"name\": \"vs0\" }}"
```
----
### 3) Update an existing QoS policy
The following example shows how to update SLOs of an exisiting QoS policy and also rename it.
<br />
---
```
curl -X PATCH "https://172.21.69.245/api/storage/qos/policies/d38bafc0-5a51-11e9-bd5b-005056ac6f1f?return_timeout=0" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"fixed\": { \"max_throughput_iops\": 15000, \"min_throughput_iops\": 10000 }, \"name\": \"qos_policy_10k_to_15k_iops\"}"
```
---
### 4) Delete an existing QoS policy
When a QoS policy is deleted any associations of the policy with a storage objects are also removed.
<br />
---
```
curl -X DELETE "https://172.21.69.245/api/storage/qos/policies/d38bafc0-5a51-11e9-bd5b-005056ac6f1f?return_timeout=0" -H "accept: application/json"
```
---
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["QosPolicy", "QosPolicySchema"]
__pdoc__ = {
    "QosPolicySchema.resource": False,
    "QosPolicySchema.patchable_fields": False,
    "QosPolicySchema.postable_fields": False,
}


class QosPolicySchema(ResourceSchema):
    """The fields of the QosPolicy object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the qos_policy.
 """
    adaptive = fields.Nested("QosPolicyAdaptiveSchema", unknown=EXCLUDE)
    r""" The adaptive field of the qos_policy.
 """
    fixed = fields.Nested("QosPolicyFixedSchema", unknown=EXCLUDE)
    r""" The fixed field of the qos_policy.
 """
    name = fields.Str()
    r""" Name of the QoS policy.

Example: extreme """
    object_count = fields.Integer()
    r""" Number of objects attached to this policy.
 """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the qos_policy.
 """
    uuid = fields.Str()
    r""" The uuid field of the qos_policy.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return QosPolicy

    @property
    def patchable_fields(self):
        return [
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "adaptive",
            "fixed",
            "name",
            "svm",
        ]

class QosPolicy(Resource):
    """Allows interaction with QosPolicy objects on the host"""

    _schema = QosPolicySchema
    _path = "/api/storage/qos/policies"
    @property
    def _keys(self):
        return ["policy.uuid"]

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

    get_collection.__func__.__doc__ = r"""Retrieves a collection of QoS policies.
### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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

    patch_collection.__func__.__doc__ = r"""Update a specific QoS policy.
### Related ONTAP commands
* `qos policy-group modify`
* `qos adaptive-policy-group modify`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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

    delete_collection.__func__.__doc__ = r"""Deletes a QoS policy. All QoS workloads associated with the policy are removed.
### Related ONTAP commands
* `qos policy-group delete`
* `qos adaptive-policy-group delete`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves a collection of QoS policies.
### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves a specific QoS policy.
### Related ONTAP commands
* `qos policy-group show`
* `qos adaptive-policy-group show`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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

    post.__doc__ = r"""Creates a QoS policy.
### Required properties
* `svm.uuid` or `svm.name` - The existing SVM owning the QoS policy.
* `name` - The name of the QoS policy.
* `fixed.*` or `adaptive.*` - Either of the fixed or adaptive parameters.
### Default property values
* If `fixed.*` parameters are specified, then capacity.shared is set to false by default.
### Related ONTAP commands
* `qos policy-group create`
* `qos adaptive-policy-group create`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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

    patch.__doc__ = r"""Update a specific QoS policy.
### Related ONTAP commands
* `qos policy-group modify`
* `qos adaptive-policy-group modify`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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

    delete.__doc__ = r"""Deletes a QoS policy. All QoS workloads associated with the policy are removed.
### Related ONTAP commands
* `qos policy-group delete`
* `qos adaptive-policy-group delete`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



