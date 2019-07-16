# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
A qtree is a logically defined file system that can exist as a special subdirectory of the root directory within a FlexVol or a FlexGroup volume.
## Qtree APIs
The following APIs are used to create, retrieve, modify, and delete qtrees.
&ndash; POST      /api/storage/qtrees
&ndash; GET       /api/storage/qtrees
&ndash; GET       /api/storage/qtrees/{volume-uuid}/{qtree-id}
&ndash; PATCH     /api/storage/qtrees/{volume-uuid}/{qtree-id}
&ndash; DELETE    /api/storage/qtrees/{volume-uuid}/{qtree-id}
## Examples
### Creating a qtree inside a volume for an SVM
This API is used to create a qtree inside a volume for an SVM.<br/>
The following example shows how to create a qtree in a FlexVol with a given security style, UNIX permissions, and an export policy.
<br/>
---
```
# The API:
POST /api/storage/qtrees
# The call:
curl -X POST 'https://<mgmt-ip>/api/storage/qtrees?return_records=true' -H 'accept: application/hal+json' -d @test_qtree_post.txt
test_qtree_post.txt(body):
{
  "svm": {
    "name": "svm1"
  },
  "volume": {
    "name": "fv"
  },
  "name": "qt1",
  "security_style": "unix",
  "unix_permissions": 744,
  "export_policy": {
      "name": "default"
  }
}
# The response:
{
    "num_records": 1,
    "records": [
      {
        "svm": {
          "name": "svm1"
        },
        "volume": {
          "name": "fv"
        },
        "name": "qt1",
        "security_style": "unix",
        "unix_permissions": 744,
        "export_policy": {
          "name": "default"
        },
        "_links": {
          "self": {
            "href": "/api/storage/qtrees/?volume.name=fv&name=qt1"
          }
        }
      }
    ],
    "job": {
      "uuid": "84edef3c-4f6d-11e9-9a71-005056a7f717",
      "_links": {
        "self": {
          "href": "/api/cluster/jobs/84edef3c-4f6d-11e9-9a71-005056a7f717"
        }
      }
    }
}
```
---
### Retrieving qtrees
This API is used to retrieve qtrees. <br/>
The following example shows how to retrieve qtrees belonging to SVM _svm1_ and volume _fv_. The `svm.name` and `volume.name` query parameters are used to find the required qtrees.
<br/>
---
```
# The API:
GET /api/storage/qtrees
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/qtrees/?svm.name=svm1&volume.name=fv" -H 'accept: application/hal+json'
# The response
{
    "records": [
      {
        "svm": {
          "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
          "name": "svm1",
          "_links": {
            "self": {
              "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
            }
          }
        },
        "volume": {
          "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
          "name": "fv",
          "_links": {
            "self": {
              "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
            }
          }
        },
        "id": 0,
        "name": "",
        "_links": {
          "self": {
            "href": "/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/0"
          }
        }
      },
      {
        "svm": {
          "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
          "name": "svm1",
          "_links": {
            "self": {
              "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
            }
          }
        },
        "volume": {
          "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
          "name": "fv",
          "_links": {
            "self": {
              "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
            }
          }
        },
        "id": 1,
        "name": "qt1",
        "_links": {
          "self": {
            "href": "/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/1"
          }
        }
      },
      {
        "svm": {
          "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
          "name": "svm1",
          "_links": {
            "self": {
              "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
            }
          }
        },
        "volume": {
          "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
          "name": "fv",
          "_links": {
            "self": {
              "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
            }
          }
        },
        "id": 2,
        "name": "qt2",
        "_links": {
          "self": {
            "href": "/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/2"
          }
        }
      }
    ],
    "num_records": 3,
    "_links": {
      "self": {
        "href": "/api/storage/qtrees/?svm.name=svm1&volume.name=fv"
      }
    }
}
```
---
### Retrieving properties of a specific qtree using a qtree identifier
This API is used to retrieve properties of a specific qtree using qtree.id. <br/>
The following example shows how to use the qtree identifier to retrieve all properties of the qtree using the `fields` query parameter.
<br/>
---
```
# The API:
GET /api/storage/qtrees/{volume.uuid}/{id}
# The call:
curl -X GET 'https://<mgmt-ip>/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/2?fields=*' -H 'accept: application/hal+json'
{
    "svm": {
      "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
      "name": "svm1",
      "_links": {
        "self": {
          "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
        }
      }
    },
    "volume": {
      "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
      "name": "fv",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
        }
      }
    },
    "id": 2,
    "name": "qt2",
    "security_style": "unix",
    "unix_permissions": 744,
    "export_policy": {
      "name": "default",
      "id": 12884901889,
      "_links": {
        "self": {
          "href": "/api/protocols/nfs/export-policies/12884901889"
        }
      }
    },
    "path": "/fv/qt2",
    "_links": {
      "self": {
        "href": "/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/2"
      }
    }
}
```
---
### Retrieving properties of a specific qtree using the qtree name
This API is used to retrieve properties of a specific qtree using qtree.name. <br/>
The following example shows how to retrieve all of the properties belonging to qtree qt2. The `svm.name` and `volume.name` query parameters are used here along with the qtree name.
<br/>
---
```
# The API:
GET /api/storage/qtrees/
# The call:
curl -X GET 'https://<mgmt-ip>/api/storage/qtrees/?svm.name=svm1&volume.name=fv&name=qt2&fields=*' -H 'accept: application/hal+json'
{
    "svm": {
      "uuid": "b68f961b-4cee-11e9-930a-005056a7f717",
      "name": "svm1",
      "_links": {
        "self": {
          "href": "/api/svm/svms/b68f961b-4cee-11e9-930a-005056a7f717"
        }
      }
    },
    "volume": {
      "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
      "name": "fv",
      "_links": {
        "self": {
          "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717"
        }
      }
    },
    "id": 2,
    "name": "qt2",
    "security_style": "unix",
    "unix_permissions": 744,
    "export_policy": {
      "name": "default",
      "id": 12884901889,
      "_links": {
        "self": {
          "href": "/api/protocols/nfs/export-policies/12884901889"
        }
      }
    },
    "_links": {
      "self": {
        "href": "/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/2"
      }
    }
}
```
---
### Updating a qtree
This API is used to update a qtree. <br/>
The following example shows how to update properties in a qtree.
<br/>
---
```
# The API:
PATCH /api/storage/qtrees/{volume.uuid}/{id}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/2' -H 'accept: application/hal+json' -d '@test_qtree_patch.txt'
test_qtree_patch.txt(body):
{
  "security_style": "mixed",
  "unix_permissions": 777,
  "export_policy": {
      "id": "9",
      "name": "exp1"
  }
}
```
---
### Renaming a qtree
This API is used to rename a qtree. <br/>
The following example below shows how to rename a qtree with a new name.
<br/>
---
```
# The API:
PATCH /api/storage/qtrees/{volume.uuid}/{id}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/1' -H 'accept: application/hal+json' -d '{ "name": "new_qt1" }'
```
---
### Deleting a qtree inside a volume of an SVM
This API is used to delete a qtree inside a volume of an SVM.</br>
The following example shows how to delete a qtree.
<br/>
---
```
# The API:
DELETE /api/storage/qtrees/{volume.uuid}/{id}
# The call:
curl -X DELETE "https://<mgmt-ip>/api/storage/qtrees/cb20da45-4f6b-11e9-9a71-005056a7f717/2" -H 'accept: application/hal+json'
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


__all__ = ["Qtree", "QtreeSchema"]
__pdoc__ = {
    "QtreeSchema.resource": False,
    "QtreeSchema.patchable_fields": False,
    "QtreeSchema.postable_fields": False,
}


class QtreeSchema(ResourceSchema):
    """The fields of the Qtree object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the qtree.
 """
    export_policy = fields.Nested("ExportPolicySchema", unknown=EXCLUDE)
    r""" The export_policy field of the qtree.
 """
    id = fields.Integer(validate=integer_validation(minimum=0, maximum=4994))
    r""" The identifier for the qtree, unique within the qtree's volume.


Example: 1 """
    name = fields.Str()
    r""" The name of the qtree. Required in POST; optional in PATCH.
 """
    path = fields.Str()
    r""" Client visible path to the qtree. This field is not available if the volume does not have a junction-path configured. Not valid in POST or PATCH.

Example: /volume3/qtree1 """
    security_style = fields.Str()
    r""" The security_style field of the qtree.
 """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the qtree.
 """
    unix_permissions = fields.Integer()
    r""" The UNIX permissions for the qtree. Valid in POST or PATCH.

Example: 493 """
    volume = fields.Nested("VolumeSchema", unknown=EXCLUDE)
    r""" The volume field of the qtree.
 """

    @property
    def resource(self):
        return Qtree

    @property
    def patchable_fields(self):
        return [
            "name",
            "security_style",
            "unix_permissions",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "export_policy",
            "name",
            "security_style",
            "svm",
            "unix_permissions",
            "volume",
        ]

class Qtree(Resource):
    r""" A qtree is a directory at the top level of a volume to which a custom export policy (for fine-grained access control) and a quota rule can be applied, if required.
 """

    _schema = QtreeSchema
    _path = "/api/storage/qtrees"
    @property
    def _keys(self):
        return ["volume.uuid", "id"]

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

    get_collection.__func__.__doc__ = r"""Retrieves qtrees configured for all FlexVols or FlexGroup volumes. <br/>
Use the `fields` query parameter to retrieve all properties of the qtree. If the `fields` query parameter is not used, then GET returns the qtree `name` and qtree `id` only.
### Related ONTAP commands
* `qtree show`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
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

    patch_collection.__func__.__doc__ = r"""Updates properties for a specific qtree.
### Related ONTAP commands
* `qtree modify`
* `qtree rename`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
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

    delete_collection.__func__.__doc__ = r"""Deletes a qtree.
### Related ONTAP commands
* `qtree delete`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves qtrees configured for all FlexVols or FlexGroup volumes. <br/>
Use the `fields` query parameter to retrieve all properties of the qtree. If the `fields` query parameter is not used, then GET returns the qtree `name` and qtree `id` only.
### Related ONTAP commands
* `qtree show`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves properties for a specific qtree identified by the `volume.uuid` and the `id` in the api path.
### Related ONTAP commands
* `qtree show`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
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

    post.__doc__ = r"""Creates a qtree in a FlexVol or a FlexGroup volume. <br/>
After a qtree is created, the new qtree is assigned an identifier. This identifier is obtained using a qtree GET request. This identifier is used in the API path for the qtree PATCH and DELETE operations.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the qtree.
* `volume.uuid` or `volume.name` - Existing volume in which to create the qtree.
* `name` - Name for the qtree.
### Recommended optional properties
If not specified in POST, the values are inherited from the volume.
* `security_style` - Security style for the qtree.
* `unix_permissions` - UNIX permissions for the qtree.
* `export_policy.name or export_policy.id` - Export policy of the SVM for the qtree.
### Related ONTAP commands
* `qtree create`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
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

    patch.__doc__ = r"""Updates properties for a specific qtree.
### Related ONTAP commands
* `qtree modify`
* `qtree rename`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
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

    delete.__doc__ = r"""Deletes a qtree.
### Related ONTAP commands
* `qtree delete`

### Learn more
* [`DOC /storage/qtrees`](#docs-storage-storage_qtrees)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



