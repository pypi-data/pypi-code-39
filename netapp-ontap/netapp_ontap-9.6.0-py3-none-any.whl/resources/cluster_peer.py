# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

##  Cluster peer operations
Cluster peering allows administrators of ONTAP systems to establish relationships between two or more independent clusters. Once a relationship exists between two clusters, they may then exchange user data, configuration information and coordinate operations. The /cluster/peers endpoint supports operations such as create, get, modify and delete using GET, PATCH and POST HTTP requests.
### Creating a cluster peer
A new cluster peer relationship can be set up by issuing a POST request to /cluster/peers. Parameters in the POST body define the settings of the peering relationship. A successful POST request that succeeds in creating a peer returns a HTTP status code, code 201, along with the details of the created peer such as peer UUID, name, authentication information. A failed POST request returns an HTTP error code along with a message indicating the reason for the error. This can include malformed request and invalid operations.
#### Sample request
```
curl -X POST 'https://<mgmt-ip>/api/cluster/peers/' -d '{"authentication":{"expiry_time":"12/25/2018 12:34:56","generate_passphrase":true}}'
```
##### Examples
```
# Create - no params
body = {}
# Create with a peer address and a passphrase
body =
{
    "remote":
      {
          "ip_addresses":["1.2.3.4"]
      }
}
# Create with a peer name and a generated passphrase that is true
body =
{
    "name":"cp_xyz123",
    "authentication":
      {
          "generate_passphrase":true
      }
}
# Create with a name, a peer address, and a passphrase
body =
{
    "name":"cp_xyz123",
    "remote":
      {
          "ip_addresses": ["1.2.3.4"]
      },
    "authentication":
      {
          "passphrase":"xyz12345"
      }
 }
# Create with a proposed encryption protocol
body =
{
    "encryption":
      {
          "proposed":"tls-psk"
      }
}
```
## Creating local intercluster LIFs
The local cluster must have an intercluster LIF on each node for the correct operation of cluster peering.
If no local intercluster LIFs exist, you can optionally specify LIFs to be created for each node in the local cluster.
These local interfaces, if specified, are created on each node before proceeding with the creation of the cluster peering relationship. Cluster peering relationship would be established if there is an error preventing the LIFs from being created.
Local interfaces, once created, should not be specified for subsequent cluster peering relationships.
### Local LIF creation fields

* local_network.ip_addresses - list of IP addresses to assign, one per node in the local cluster
* local_network.netmask - IPv4 mask or netmask length
* local_network.broadcast_domain - Broadcast domain that is in use within the IPspace.
* local_network.gateway - The IPv4 or IPv6 address of the default router.
##### Additional information on network routes
It might happen that when creating LIFs the network route discovery mechanism could take additional time (1-5 seconds) to become visible in the network outside of the cluster. This delay in publishing the routes might cause an initial cluster peer "create" request to fail. This error disappears with a retry of the same request.
##### Example
```
curl -X POST "https://<mgmt-ip>/api/cluster/peers" -d body
```
where "<mgmt-ip>" is replaced by the IP address of the cluster management LIF,
and "body" is replaced by the JSON body of the POST,
containing the fields for the new peering relationship and local LIFs.
##### Example POST body
To create 4 intercluster LIFs on a 4-node cluster before creating a cluster peer relationship:
```
{
    "local_network":
    {
        "interfaces": [
            {"ip_address":"1.2.3.4"},
            {"ip_address":"1.2.3.5"},
            {"ip_address":"1.2.3.6"}
            ],
        "netmask": "255.255.0.0",
        "broadcast_domain": "Default",
        "gateway": "1.2.0.1"
    }
    "remote.ip_addresses": ["1.2.9.9"],
    "authentication.passphrase": "xyz12345"
}
```
## Retrieve a cluster peer
Peers in a cluster can be retrieved by issuing a GET request to /cluster/peers. It is also possible to retrieve a specific peer when qualified by its UUID to /cluster/peers/{uuid}.
### Overview of fields used for retrieving a cluster peer
A GET request might have no query parameters or a valid cluster UUID. The former retrieves all records while the latter retrieves the record for the cluster peer with that UUID.
#### Required fields
There are no required fields for GET requests.
#### Optional fields
The following fields are optional for GET requests

* UUID - uuid of the cluster peer
##### Examples
```
curl -X GET "https://<mgmt-ip>/api/cluster/peers/"
curl -X GET "https://<mgmt-ip>/api/cluster/peers/{uuid}"
curl -X GET "https://<mgmt-ip>/api/cluster/peers/{uuid}?fields=*"
```
## Update a cluster peer
A cluster peer relationship can be updated by issuing a PATCH request to /cluster/peers/{uuid}. As in the CLI mode, you can toggle the proposed encryption protocol, update the passphrase, or specify a new set of stable addresses.  All PATCH requests take the parameters that are to be updated in the request body. If the generate_passphrase is 'true', the passphrase is returned in the PATCH response.
### Fields overview
This sections highlights the parameters that control the modification of an existing cluster peering relationship.
#### Required fields
A PATCH request with an empty body has no effect on the cluster peer instance. All other fields and the combinations in which they are valid are indicated below:

* `encryption_proposed` - Toggle the proposed encryption protocol (from 'none' to 'tls-psk' or otherwise). Authentication must be true and a passphrase must be present in body.
* `passphrase`
* `passphrase` or `generate passphrase`
* `remote.ip_addresses`
#### Optional fields

* `expiration time` - Set the expiration time of the passphrase
##### Examples
```
# Update with an empty body
body = {}
# Update the proposed encryption protocol from tls-psk to none
body =
{
    "authentication":
      {
          "passphrase":"xyz12345",
          "in_use":"ok"
      },
    "encryption":
      {
          "proposed":"none"
      }
}
# Update the passphrase
body =
{
    "authentication":
     {
         "passphrase":"xyz12345",
         "in_use":"ok"
     }
}
# Set an auto-generated passphrase
body =
{
    "authentication":
     {
         "generate_passphrase": true,
         "in_use":"ok"
     }
}
# Update remote IP addresses
body =
{
    "remote":
      {
          "ip_addresses":["10.224.65.30"]
      }
}
```
##### Sample requests
```
# Set a passphrase
curl -X PATCH 'https://<mgmt-ip>/api/cluster/peers/73123071-d0b9-11e8-a686-005056a7179a' -d '{"authentication":{"passphrase":"xyz12345","in_use":"ok"}}'
# Update a peer address
curl -X PATCH 'https://<mgmt-ip>/api/cluster/peers/73123071-d0b9-11e8-a686-005056a7179a' -d '{"remote":{"ip_addresses":["1.2.3.4"]}}'
```
## Delete a cluster peer
This interface allows you to delete a cluster peer using the HTTP DELETE request.
#### Required fields
All delete operations must be performed on a valid peer UUID. Deleting an invalid peer returns 'HTTP 404' indicating an error.
#### Optional fields
The DELETE operation has no optional fields.
#### Request format
DELETE "https://<mgmt-ip>/api/cluster/peers/{uuid}"
##### Examples
The request -
```
curl -X DELETE "https://<mgmt-ip>/api/cluster/peers/8becc0d4-c12c-11e8-9ceb-005056bbd143"
```
deletes a peer with peer UUID '8becc0d4-c12c-11e8-9ceb-005056bbd143'
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["ClusterPeer", "ClusterPeerSchema"]
__pdoc__ = {
    "ClusterPeerSchema.resource": False,
    "ClusterPeerSchema.patchable_fields": False,
    "ClusterPeerSchema.postable_fields": False,
}


class ClusterPeerSchema(ResourceSchema):
    """The fields of the ClusterPeer object"""

    links = fields.Nested("ClusterPeerLinksSchema", unknown=EXCLUDE)
    r""" The links field of the cluster_peer.
 """
    authentication = fields.Nested("ClusterPeerAuthenticationSchema", unknown=EXCLUDE)
    r""" The authentication field of the cluster_peer.
 """
    encryption = fields.Nested("ClusterPeerEncryptionSchema", unknown=EXCLUDE)
    r""" The encryption field of the cluster_peer.
 """
    initial_allowed_svms = fields.List(fields.Nested("SvmSchema", unknown=EXCLUDE))
    r""" The local SVMs allowed to peer with the peer cluster's SVMs. This list can be modified until the remote cluster accepts this cluster peering relationship.
 """
    ipspace = fields.Nested("IpspaceSchema", unknown=EXCLUDE)
    r""" The ipspace field of the cluster_peer.
 """
    local_network = fields.Nested("ClusterPeerLocalNetworkSchema", unknown=EXCLUDE)
    r""" The local_network field of the cluster_peer.
 """
    name = fields.Str()
    r""" Optional name for the cluster peer relationship. By default it is the name of the remote cluster.

Example: cluster2 """
    remote = fields.Nested("ClusterPeerRemoteSchema", unknown=EXCLUDE)
    r""" The remote field of the cluster_peer.
 """
    status = fields.Nested("ClusterPeerStatusSchema", unknown=EXCLUDE)
    r""" The status field of the cluster_peer.
 """
    uuid = fields.Str()
    r""" UUID of the cluster peer relationship. For anonymous cluster peer offers, the UUID will change when the remote cluster accepts the relationship.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ClusterPeer

    @property
    def patchable_fields(self):
        return [
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "authentication",
            "encryption",
            "initial_allowed_svms",
            "ipspace",
            "local_network",
            "name",
            "remote",
            "status",
        ]

class ClusterPeer(Resource):
    """Allows interaction with ClusterPeer objects on the host"""

    _schema = ClusterPeerSchema
    _path = "/api/cluster/peers"
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

    get_collection.__func__.__doc__ = r"""Retrieve the collection of cluster peers.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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

    patch_collection.__func__.__doc__ = r"""Updates a cluster peer instance.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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

    delete_collection.__func__.__doc__ = r"""Deletes a cluster peer.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieve the collection of cluster peers.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves a specific cluster peer instance.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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

    post.__doc__ = r"""Creates a peering relationship and, optionally, the IP interfaces it will use. There are two ways to create a peering relationship.
### Provide remote IP
Here the user provides the remote IP address. Creating a new cluster peer relationship with a specific remote cluster requires at least one remote intercluster IP address from that cluster.
### Required properties
  * `remote.ip_addresses` - Addresses of the remote peers. The local peer must be able to reach and connect to these addresses for the request to succeed in creating a peer.
  * Either set `generate_passphrase` to true or provide a passphrase in the body of the request; only one of them is required.
### Optional properties
  The following fields are optional for a POST on /cluster/peer/. All fields must follow the structure in the cluster peer API definition.
  * `name` - Name of the peering relationship.
  * `passphrase` - User generated passphrase for use in authentication.
  * `generate_passphrase` (true/false) - When this option is true, ONTAP automatically generates a passphrase to authenticate cluster peers.
  * `ipspace` - IPspace of the local intercluster LIFs. Assumes Default IPspace if not provided.
  * `initial_allowed_svms` - the local SVMs allowed to peer with the peer cluster's SVMs. This list can be modified until the remote cluster accepts this cluster peering relationship.
  * `local_network` - fields to create a local intercluster LIF. See section on "Creating local intercluster lifs".
  * `expiry_time` - Duration in ISO 8601 format for which the user-supplied or auto-generated passphrase is valid. Expiration time must not be greater than seven days into the future. ISO 8601 duration format is "PnDTnHnMnS" or "PnW" where n is a positive integer. The nD, nH, nM and nS fields can be dropped if zero. "P" should always be present and "T" should be present if there are any hours, minutes or seconds fields.
  * `encryption_proposed` (none/tls-psk) - Encryption mechanism of the communication channel between the two peers.
### Do not provide remote IP
  This method is used when the remote IP address is not provided. This method is used when the filer is ready to accept peering request from foreign clusters.
### Required properties
  * `generate_passphrase` (true) - This option must be set to  true. ONTAP automatically generates a passphrase to authenticate cluster peers. Either set generate_passphrase to true or provide a passphrase in the body of the request; only one of them is required.
### Optional properties
  The following fields are optional for a POST on /cluster/peer/. All fields must follow the structure in the cluster peer API definition.
  * `name` - Name of the remote peer.
  * `ipspace` - IPspace of the local intercluster LIFs. Assumes Default IPspace if not provided.
  * `initial_allowed_svms` - Local SVMs allowed to peer with the peer cluster's SVMs. This list can be modified until the remote cluster accepts this cluster peering relationship.
  * `local_network` - Fields to create a local intercluster LIF. See section on "Creating local intercluster lifs".
  * `expiry_time` - Duration in ISO 8601 format for which the user-supplied or auto-generated passphrase is valid. Expiration time must not be greater than seven days into the future. ISO 8601 duration format is "PnDTnHnMnS" or "PnW" where n is a positive integer. The nD, nH, nM and nS fields can be dropped if zero. "P" should always be present and "T" should be present if there are any hours, minutes or seconds fields.
  * `encryption_proposed` (none/tls-psk) - Encryption mechanism of the communication channel between the two peers.
## Additional information
As with creating a cluster peer through the CLI, the combinations of options must be valid in order for the create operation to succeed. The following list shows the combinations that will succeed and those that will fail:
* a passphrase only (fail)
* a peer IP address (fail)
* a passphrase with an expiration time > 7 days into the future (fail)
* peer IP address and a passphrase (OK)
* generate_passphrase=true (OK)
* any proposed encryption protocol (OK)
* an IPspace name or UUID (OK)
* a passphrase, peer IP address, and any proposed encryption protocol (OK)
* a non empty list initial allowed vserver peer names or UUIDs. (OK)
## Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)

### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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

    patch.__doc__ = r"""Updates a cluster peer instance.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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

    delete.__doc__ = r"""Deletes a cluster peer.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



