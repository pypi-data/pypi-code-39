# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Summary
This API is used to view and manipulate jobs. Jobs provide information about asynchronous operations. Some long-running jobs are paused or cancelled by calling PATCH. Individual operations will mention if they support PATCH on the job. Once a job transitions to a terminal state, it is deleted after a default time of 300 seconds. Attempts to GET or PATCH the job will return a 404 error code once the job has been deleted.
## Example
The following examples show how to retrieve and update a job state
### 1) Retrieve job information
---
```
# The API:
/api/cluster/jobs/{uuid}
# The call:
curl -X GET "https://<mgmt-ip>/api/cluster/jobs/b5145e1d-b53b-11e8-8252-005056bbd8f5" -H "accept: application/json"
# The response:
{
    "uuid": "b5145e1d-b53b-11e8-8252-005056bbd8f5",
    "code": 0,
    "description": "Cluster Backup Job",
    "state": "running",
    "message": "creating_node_backups",
    "_links": {
        "self": {
            "href": "/api/cluster/jobs/b5145e1d-b53b-11e8-8252-005056bbd8f5"
        }
    }
}
```
---
### 2) Update a job that supports the new state
---
```
# The API:
/api/cluster/jobs/{uuid}
# The call:
curl -X PATCH "https://<mgmt-ip>/api/cluster/jobs/b5145e1d-b53b-11e8-8252-005056bbd8f5?action=cancel" -H "accept: application/json"
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


__all__ = ["Job", "JobSchema"]
__pdoc__ = {
    "JobSchema.resource": False,
    "JobSchema.patchable_fields": False,
    "JobSchema.postable_fields": False,
}


class JobSchema(ResourceSchema):
    """The fields of the Job object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the job.
 """
    code = fields.Integer()
    r""" If the state indicates "failure", this is the final error code.

Example: 0 """
    description = fields.Str()
    r""" The description of the job to help identify it independent of the UUID.

Example: App Snapshot Job """
    end_time = fields.DateTime()
    r""" The time the job ended.
 """
    message = fields.Str()
    r""" A message corresponding to the state of the job providing additional details about the current state.

Example: Complete: Successful """
    start_time = fields.DateTime()
    r""" The time the job started.
 """
    state = fields.Str(validate=enum_validation(['queued', 'running', 'paused', 'success', 'failure']))
    r""" The state of the job.

Valid choices:

* queued
* running
* paused
* success
* failure """
    uuid = fields.Str()
    r""" The uuid field of the job.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return Job

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]

class Job(Resource):
    """Allows interaction with Job objects on the host"""

    _schema = JobSchema
    _path = "/api/cluster/jobs"
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

    get_collection.__func__.__doc__ = r"""Retrieves a list of recently running asynchronous jobs. Once a job transitions to a failure or success state, it is deleted after a default time of 300 seconds.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
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

    patch_collection.__func__.__doc__ = r"""Updates the state of a specific asynchronous job.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)


    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves a list of recently running asynchronous jobs. Once a job transitions to a failure or success state, it is deleted after a default time of 300 seconds.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the details of a specific asynchronous job. Once a job transitions to a failure or success state, it is deleted after a default time of 300 seconds.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


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

    patch.__doc__ = r"""Updates the state of a specific asynchronous job.
### Learn more
* [`DOC /cluster/jobs`](#docs-cluster-cluster_jobs)"""
    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)




