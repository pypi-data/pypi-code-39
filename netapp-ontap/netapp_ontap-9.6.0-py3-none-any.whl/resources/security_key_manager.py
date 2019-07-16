# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Overview
A key manager is a key management solution (software or dedicated hardware) that enables other ONTAP client modules to securely and persistently store keys for various uses. For example, WAFL uses the key management framework to store and retrieve the volume encryption keys that it uses to encrypt/decrypt data on NVE volumes. A key manager can be configured at both cluster scope and SVM, with one key manager allowed per SVM. The key management framework in ONTAP supports two mutually exclusive modes for persisting keys, external and onboard.<p/>
When an SVM is configured with external key management, the keys are stored on up to four key servers that are external to the system.<p/>
Once external key management is enabled for an SVM, key servers can be added or removed using the <i>/api/security/key-managers/{uuid}/key-servers</i> endpoint. See [`POST /security/key-managers/{uuid}/key-servers`] and [`DELETE /security/key-managers/{uuid}/key-servers/{server}`] for more details.<p/>
Setting up external key management dictates that the required certificates for securely communicating with the key server are installed prior to configuring the key manager. To install the required client and server_ca certificates, use the <i>/api/security/certificates/</i> endpoint. <p/>
See [`POST /security/certificates`], [`GET /security/certificates/uuid`] and [`DELETE /security/certificates/{uuid}`] for more details.<p/>
When an SVM is configured with onboard key management, the keys are stored in ONTAP in wrapped format using a key hierarchy created using the salted hash of the passphrase entered when configuring onboard key management. This model fits well for customers who use ONTAP to store their own data. <p/>
## Examples
### Creating an external key manager with 1 key server for a cluster
The example key manager is configured at the cluster-scope with one key server. Note that the UUIDs of the certificates are those that are already installed at the cluster-scope. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration<br/>
```
# The API:
POST /api/security/key-managers
# The call:
curl -X POST 'https://<mgmt-ip>/api/security/key-managers?return_records=true' -H 'accept: application/hal+json' -d "{ \"external\": { \"client_certificate\": { \"uuid\": \"5fb1701a-d922-11e8-bfe8-005056bb017d\" }, \"server_ca_certificates\": [ { \"uuid\": \"827d7d31-d6c8-11e8-b5bf-005056bb017d\" }],\"servers\": [ { \"server\": \"10.225.89.33:5696\" } ] } }"
# The response:
{
  "num_records": 1,
  "records": [
    {
      "uuid": "815e9462-dc57-11e8-9b2c-005056bb017d",
      "external": {
        "client_certificate": {
          "uuid": "5fb1701a-d922-11e8-bfe8-005056bb017d"
        },
        "server_ca_certificates": [
          {
            "uuid": "827d7d31-d6c8-11e8-b5bf-005056bb017d"
          }
        ],
        "servers": [
          {
            "server": "10.225.89.33:5696"
          }
        ]
      },
      "_links": {
        "self": {
          "href": "/api/security/key-managers/815e9462-dc57-11e8-9b2c-005056bb017d"
        }
      }
    }
  ]
}
```
---
### Creating an external key manager with 1 key server for an SVM
The example key manager is configured at the SVM-scope with one key server. Note that the UUIDs of the certificates are those that are already installed in that SVM. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration<br/>
```
# The API:
POST /api/security/key-managers
# The call:
curl -X POST 'https://<mgmt-ip>/api/security/key-managers?return_records=true' -H 'accept: application/hal+json' -d "{ \"svm\": { \"uuid\": \"216e6c26-d6c6-11e8-b5bf-005056bb017d\" }, \"external\": { \"client_certificate\": { \"uuid\": \"91dcaf7c-dbbd-11e8-9b2c-005056bb017d\" }, \"server_ca_certificates\": [ { \"uuid\": \"a4d4b8ba-dbbd-11e8-9b2c-005056bb017d\" }],\"servers\": [ { \"server\": \"10.225.89.34:5696\" } ] } }"
# The response:
{
  "num_records": 1,
  "records": [
    {
      "uuid": "80af63f2-dbbf-11e8-9b2c-005056bb017d",
      "svm": {
        "uuid": "216e6c26-d6c6-11e8-b5bf-005056bb017d"
      },
      "external": {
        "client_certificate": {
        "uuid": "91dcaf7c-dbbd-11e8-9b2c-005056bb017d"
        },
        "server_ca_certificates": [
          {
            "uuid": "a4d4b8ba-dbbd-11e8-9b2c-005056bb017d"
          }
        ],
        "servers": [
          {
            "server": "10.225.89.34:5696"
          }
        ]
      },
      "_links": {
        "self": {
          "href": "/api/security/key-managers/80af63f2-dbbf-11e8-9b2c-005056bb017d"
        }
      }
    }
  ]
}
```
---
### Creating an onboard key manager for a cluster
The following example shows how to create an onboard key manager for a cluster with the onboard key manager configured at the cluster-scope.<br/>
```
# The API:
POST /api/security/key-managers
# The call:
curl -X POST 'https://<mgmt-ip>/api/security/key-managers' -H 'accept: application/hal+json' -d '{ "onboard": { "passphrase": "passphrase" } }'
```
---
### Retrieving the key manager configurations for all clusters and SVMs
The following example shows how to retrieve all configured key managers along with their configurations.
```
# The API:
GET /api/security/key-managers
# The call:
curl -X GET 'https://<mgmt-ip>/api/security/key-managers?fields=*' -H 'accept: application/hal+json'
# The response:
{
  "records": [
    {
      "uuid": "2345f09c-d6c9-11e8-b5bf-005056bb017d",
      "scope": "svm",
      "svm": {
        "uuid": "0f22f8f3-d6c6-11e8-b5bf-005056bb017d",
        "name": "vs0"
      },
      "external": {
        "client_certificate": {
          "uuid": "4cb15482-d6c8-11e8-b5bf-005056bb017d",
          "_links": {
            "self": {
              "href": "/api/security/certificates/4cb15482-d6c8-11e8-b5bf-005056bb017d/"
            }
          }
        },
        "server_ca_certificates": [
          {
            "uuid": "8a17c858-d6c8-11e8-b5bf-005056bb017d",
            "_links": {
              "self": {
                "href": "/api/security/certificates/8a17c858-d6c8-11e8-b5bf-005056bb017d/"
              }
            }
          }
        ],
        "servers": [
          {
            "server": "10.2.30.4:5696",
            "timeout": 25,
            "username": "",
            "_links": {
              "self": {
                "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/10.2.30.4:5696/"
              }
            }
          },
          {
            "server": "vs0.local1:3678",
            "timeout": 25,
            "username": "",
            "_links": {
              "self": {
                "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/vs0.local1:3678/"
              }
            }
          }
        ]
      },
      "_links": {
        "self": {
          "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d"
        }
      }
    },
    {
      "uuid": "815e9462-dc57-11e8-9b2c-005056bb017d",
      "scope": "cluster",
      "external": {
        "client_certificate": {
          "uuid": "5fb1701a-d922-11e8-bfe8-005056bb017d",
          "_links": {
            "self": {
              "href": "/api/security/certificates/5fb1701a-d922-11e8-bfe8-005056bb017d/"
            }
          }
        },
        "server_ca_certificates": [
          {
            "uuid": "827d7d31-d6c8-11e8-b5bf-005056bb017d",
            "_links": {
              "self": {
                "href": "/api/security/certificates/827d7d31-d6c8-11e8-b5bf-005056bb017d/"
              }
            }
          }
        ],
        "servers": [
          {
            "server": "10.225.89.33:5696",
            "timeout": 25,
            "username": "",
            "_links": {
              "self": {
                "href": "/api/security/key-managers/815e9462-dc57-11e8-9b2c-005056bb017d/key-servers/10.225.89.33:5696/"
              }
            }
          }
        ]
      },
      "_links": {
        "self": {
          "href": "/api/security/key-managers/815e9462-dc57-11e8-9b2c-005056bb017d"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/security/key-managers?fields=*"
    }
  }
}
```
---
### Retrieving a specific key manager configuration
The following example shows how to retrieve a specific key manager configuration.
```
# The API:
GET /api/security/key-managers/{uuid}
# The call:
curl -X GET 'https://<mgmt-ip>/api/security/key-managers/<uuid>?fields=*' -H 'accept: application/hal+json'
# The response:
{
  "uuid": "2345f09c-d6c9-11e8-b5bf-005056bb017d",
  "scope": "svm",
  "svm": {
    "uuid": "0f22f8f3-d6c6-11e8-b5bf-005056bb017d",
    "name": "vs0"
  },
  "external": {
    "client_certificate": {
      "uuid": "4cb15482-d6c8-11e8-b5bf-005056bb017d",
      "_links": {
        "self": {
          "href": "/api/security/certificates/4cb15482-d6c8-11e8-b5bf-005056bb017d/"
        }
      }
    },
    "server_ca_certificates": [
      {
        "uuid": "8a17c858-d6c8-11e8-b5bf-005056bb017d",
        "_links": {
          "self": {
            "href": "/api/security/certificates/8a17c858-d6c8-11e8-b5bf-005056bb017d/"
          }
        }
      }
    ],
    "servers": [
      {
        "server": "10.2.30.4:5696",
        "timeout": 25,
        "username": "",
        "_links": {
          "self": {
            "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/10.2.30.4:5696/"
          }
        }
      },
      {
        "server": "vs0.local1:3678",
        "timeout": 25,
        "username": "",
        "_links": {
          "self": {
            "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/vs0.local1:3678/"
          }
        }
      }
    ]
  },
  "_links": {
    "self": {
      "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d"
    }
  }
}
```
---
### Updating the configuration of an external key manager
The following example shows how to update the server-ca configuration of an external key manager.
```
# The API:
PATCH /api/security/key-managers/{uuid}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/security/key-managers/<uuid>?' -H 'accept: application/hal+json' -d "{ \"external\": { \"server_ca_certificates\": [ { \"uuid\": \"23b05c58-d790-11e8-b5bf-005056bb017d\" }] } }"
```
---
### Updating the passphrase of an onboard key manager
The following example shows how to update the passphrase of a given key manager.
```
# The API:
PATCH /api/security/key-managers/{uuid}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/security/key-managers/<uuid>?' -H 'accept: application/hal+json' -d "{ \"onboard\": { \"existing_passphrase\": \"existing_passphrase\", \"passphrase\": \"new_passphrase\" } }"
```
---
### Deleting a configured key manager
The following example shows how to delete a key manager given its UUID.
```
# The API:
DELETE /api/security/key-managers/{uuid}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/security/key-managers/<uuid>?' -H 'accept: application/hal+json'
```
---
### Adding a key server to an external key manager
The following example shows how to add a key server to an external key manager.
```
# The API:
POST /api/security/key-managers/{uuid}/key-servers
# The call:
curl -X POST 'https://<mgmt-ip>/api/security/key-managers/<uuid>/key-servers?return_records=true' -H 'accept: application/hal+json' -d "{ \"server\": \"10.225.89.34:5696\" }"
# The response:
{
  "num_records": 1,
  "records": [
    {
      "server": "10.225.89.34:5696",
      "_links": {
        "self": {
          "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.34%3A5696"
        }
      }
    }
  ]
}
```
---
### Adding 2 key servers to an external key manager
The following example shows how to add 2 key servers to an external key manager. Note that the <i>records</i> property is used to add multiple key servers to the key manager in a single API call.
```
# The API:
POST /api/security/key-managers/{uuid}/key-servers
# The call:
curl -X POST 'https://<mgmt-ip>/api/security/key-managers/<uuid>/key-servers?return_records=true' -H 'accept: application/hal+json' -d "{ \"records\": [ { \"server\": \"10.225.89.34:5696\" }, { \"server\": \"10.225.89.33:5696\" } ] }"
# The response:
{
  "num_records": 1,
  "records": [
    {
      "_links": {
        "self": {
          "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/"
        }
      }
    }
  ]
}
```
---
### Retrieving all the key servers configured in an external key manager
The following example shows how to retrieve all key servers configured in an external key manager.
```
# The API:
GET /api/security/key-managers/{uuid}/key-servers
# The call:
curl -X GET 'https://<mgmt-ip>/api/security/key-managers/<uuid>/key-servers?fields=*' -H 'accept: application/hal+json'
# The response:
{
  "records": [
    {
      "uuid": "43e0c191-dc5c-11e8-9b2c-005056bb017d",
      "server": "10.225.89.33:5696",
      "timeout": 25,
      "username": "",
      "_links": {
        "self": {
          "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.33%3A5696"
        }
      }
    },
    {
      "uuid": "43e0c191-dc5c-11e8-9b2c-005056bb017d",
      "server": "10.225.89.34:5696",
      "timeout": 25,
      "username": "",
      "_links": {
        "self": {
          "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.34%3A5696"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers?fields=*"
    }
  }
}
```
---
### Retrieving a specific key server configured in an external key manager
The following example shows how to retrieve a specific key server configured in an external key manager.
```
# The API:
GET /api/security/key-managers/{uuid}/key-servers/{server}
# The call:
curl -X GET 'https://<mgmt-ip>/api/security/key-managers/<uuid>/key-servers/{server}?fields=*' -H 'accept: application/hal+json'
# The response:
{
  "uuid": "43e0c191-dc5c-11e8-9b2c-005056bb017d",
  "server": "10.225.89.34:5696",
  "timeout": 25,
  "username": "",
  "_links": {
    "self": {
      "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.34:5696"
    }
  }
}
```
---
### Updating a specific key server configuration configured in an external key manager
The following example shows how to update a specific key server configured in an external key manager.
```
# The API:
PATCH /api/security/key-managers/{uuid}/key-servers/{server}
# The call:
curl -X PATCH 'https://<mgmt-ip>/api/security/key-managers/<uuid>/key-servers/{server}' -H 'accept: application/hal+json' -d "{ \"timeout\": 45 }"
```
---
### Deleting a key server from an external key manager
The following example shows how to delete a key server from an external key manager.
```
# The API:
DELETE /api/security/key-managers/{uuid}/key-servers/{server}
# The call:
curl -X DELETE 'https://<mgmt-ip>/api/security/key-managers/<uuid>/key-servers/{server}' -H 'accept: application/hal+json'
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


__all__ = ["SecurityKeyManager", "SecurityKeyManagerSchema"]
__pdoc__ = {
    "SecurityKeyManagerSchema.resource": False,
    "SecurityKeyManagerSchema.patchable_fields": False,
    "SecurityKeyManagerSchema.postable_fields": False,
}


class SecurityKeyManagerSchema(ResourceSchema):
    """The fields of the SecurityKeyManager object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the security_key_manager.
 """
    external = fields.Nested("SecurityKeyManagerExternalSchema", unknown=EXCLUDE)
    r""" The external field of the security_key_manager.
 """
    onboard = fields.Nested("SecurityKeyManagerOnboardSchema", unknown=EXCLUDE)
    r""" The onboard field of the security_key_manager.
 """
    scope = fields.Str()
    r""" The scope field of the security_key_manager.
 """
    svm = fields.Nested("SvmSchema", unknown=EXCLUDE)
    r""" The svm field of the security_key_manager.
 """
    uuid = fields.Str()
    r""" The uuid field of the security_key_manager.
 """

    @property
    def resource(self):
        return SecurityKeyManager

    @property
    def patchable_fields(self):
        return [
            "scope",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "external",
            "onboard",
            "scope",
            "svm",
        ]

class SecurityKeyManager(Resource):
    """Allows interaction with SecurityKeyManager objects on the host"""

    _schema = SecurityKeyManagerSchema
    _path = "/api/security/key-managers"
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

    get_collection.__func__.__doc__ = r"""Retrieves key managers.
### Related ONTAP commands
* `security key-manager show-keystore`
* `security key-manager external show`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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

    patch_collection.__func__.__doc__ = r"""Updates a key manager.
### Related ONTAP commands
* `security key-manager external modify`
* `security key-manager onboard update-passphrase`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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

    delete_collection.__func__.__doc__ = r"""Deletes a key manager.
### Related ONTAP commands
* `security key-manager external disable`
* `security key-manager onboard disable`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves key managers.
### Related ONTAP commands
* `security key-manager show-keystore`
* `security key-manager external show`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves key managers.
### Related ONTAP commands
* `security key-manager show-keystore`
* `security key-manager external show`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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

    post.__doc__ = r"""Creates a key manager.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create a key manager.
* `external.client_certificate` - Client certificate. Required only when creating an external key manager.
* `external.server_ca_certificates` - Server CA certificates. Required only when creating an external key manager.
* `external.servers.server` - Key servers. Required only when creating an external key manager.
* `onboard.passphrase` - Cluster-wide passphrase. Required only when creating an onboard key manager.
### Related ONTAP commands
* `security key-manager external enable`
* `security key-manager onboard enable`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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

    patch.__doc__ = r"""Updates a key manager.
### Related ONTAP commands
* `security key-manager external modify`
* `security key-manager onboard update-passphrase`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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

    delete.__doc__ = r"""Deletes a key manager.
### Related ONTAP commands
* `security key-manager external disable`
* `security key-manager onboard disable`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



