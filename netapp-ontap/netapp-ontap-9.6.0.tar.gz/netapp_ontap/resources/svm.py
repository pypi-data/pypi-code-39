# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.

## Managing SVMs
<br/>Cluster administrators can manage any SVM bound to the cluster. In addition, SVMs can also be managed by their SVM administrators. The SVM administrator manages the SVM resources, such as volumes, protocols and services, depending on the capabilities assigned by the cluster administrator. SVM administrators cannot create, modify, or delete SVMs. The cluster administrator manages SVM create, modify, or delete operations.<br/>
<br/>While configuring CIFS, you must also configure IP interfaces and DNS. No other protocol configuration is allowed when configuring NVMe. NFS, FCP, CIFS and iSCSI protocols can be configured together.<br/>
SVM administrators might have all or some of the following administration capabilities:
1. Data access protocol configuration
   Configures data access protocols, such as NFS, CIFS, iSCSI, and Fibre Channel (FC) protocol (Fibre Channel over Ethernet included).
2. Services configuration
   Configures services such as LDAP, NIS, and DNS.
3. Monitoring SVM
   Monitors jobs, network connections, network interfaces, and SVM health.
"""

import inspect
from typing import Iterable, Optional, Union

from marshmallow import EXCLUDE, fields  # type: ignore

from netapp_ontap.resource import Resource, ResourceSchema
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["Svm", "SvmSchema"]
__pdoc__ = {
    "SvmSchema.resource": False,
    "SvmSchema.patchable_fields": False,
    "SvmSchema.postable_fields": False,
}


class SvmSchema(ResourceSchema):
    """The fields of the Svm object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the svm.
 """
    aggregates = fields.List(fields.Nested("AggregateSchema", unknown=EXCLUDE))
    r""" List of allowed aggregates for SVM volumes. An administrator is allowed to create volumes on these aggregates.
 """
    cifs = fields.Nested("SvmCifsServiceSchema", unknown=EXCLUDE)
    r""" The cifs field of the svm.
 """
    comment = fields.Str(validate=len_validation(minimum=0, maximum=255))
    r""" Comment
 """
    dns = fields.Nested("SvmDnsSchema", unknown=EXCLUDE)
    r""" The dns field of the svm.
 """
    fcp = fields.Nested("SvmFcpSchema", unknown=EXCLUDE)
    r""" The fcp field of the svm.
 """
    ip_interfaces = fields.List(fields.Nested("IpInterfaceSvmSchema", unknown=EXCLUDE))
    r""" IP interfaces for the SVM
 """
    ipspace = fields.Nested("IpspaceSchema", unknown=EXCLUDE)
    r""" The ipspace field of the svm.
 """
    iscsi = fields.Nested("SvmIscsiSchema", unknown=EXCLUDE)
    r""" The iscsi field of the svm.
 """
    language = fields.Str(validate=enum_validation(['c', 'da', 'de', 'en', 'en_us', 'es', 'fi', 'fr', 'he', 'it', 'ja', 'ja_jp.pck', 'ko', 'nl', 'pt', 'sv', 'zh', 'zh.gbk', 'zh_tw', 'zh_tw.big5', 'c.utf_8', 'ar', 'ar.utf_8', 'cs', 'cs.utf_8', 'da.utf_8', 'de.utf_8', 'en.utf_8', 'en_us.utf_8', 'es.utf_8', 'fi.utf_8', 'fr.utf_8', 'he.utf_8', 'hr', 'hr.utf_8', 'hu', 'hu.utf_8', 'it.utf_8', 'ja.utf_8', 'ja_v1', 'ja_v1.utf_8', 'ja_jp.pck.utf_8', 'ja_jp.932', 'ja_jp.932.utf_8', 'ja_jp.pck_v2', 'ja_jp.pck_v2.utf_8', 'ko.utf_8', 'no.utf_8', 'nl.utf_8', 'pl', 'pl.utf_8', 'pt.utf_8', 'ro', 'ro.utf_8', 'ru', 'ru.utf_8', 'sk', 'sk.utf_8', 'sl', 'sl.utf_8', 'sv.utf_8', 'tr', 'tr.utf_8', 'zh.utf_8', 'zh.gbk.utf_8', 'zh_tw.utf_8', 'zh_tw.big5.utf_8', 'utf8mb4']))
    r""" Default volume language code. UTF-8 encoded languages are valid in POST or PATCH. Non UTF-8 language encodings are for backward compatibility and are not valid input for POST and PATCH requests.

Valid choices:

* c
* da
* de
* en
* en_us
* es
* fi
* fr
* he
* it
* ja
* ja_jp.pck
* ko
* nl
* pt
* sv
* zh
* zh.gbk
* zh_tw
* zh_tw.big5
* c.utf_8
* ar
* ar.utf_8
* cs
* cs.utf_8
* da.utf_8
* de.utf_8
* en.utf_8
* en_us.utf_8
* es.utf_8
* fi.utf_8
* fr.utf_8
* he.utf_8
* hr
* hr.utf_8
* hu
* hu.utf_8
* it.utf_8
* ja.utf_8
* ja_v1
* ja_v1.utf_8
* ja_jp.pck.utf_8
* ja_jp.932
* ja_jp.932.utf_8
* ja_jp.pck_v2
* ja_jp.pck_v2.utf_8
* ko.utf_8
* no.utf_8
* nl.utf_8
* pl
* pl.utf_8
* pt.utf_8
* ro
* ro.utf_8
* ru
* ru.utf_8
* sk
* sk.utf_8
* sl
* sl.utf_8
* sv.utf_8
* tr
* tr.utf_8
* zh.utf_8
* zh.gbk.utf_8
* zh_tw.utf_8
* zh_tw.big5.utf_8
* utf8mb4 """
    ldap = fields.Nested("SvmLdapSchema", unknown=EXCLUDE)
    r""" The ldap field of the svm.
 """
    name = fields.Str()
    r""" The name of the SVM.


Example: svm1 """
    nfs = fields.Nested("SvmNfsSchema", unknown=EXCLUDE)
    r""" The nfs field of the svm.
 """
    nis = fields.Nested("SvmNisSchema", unknown=EXCLUDE)
    r""" The nis field of the svm.
 """
    nsswitch = fields.Nested("SvmNsswitchSchema", unknown=EXCLUDE)
    r""" The nsswitch field of the svm.
 """
    nvme = fields.Nested("SvmNvmeSchema", unknown=EXCLUDE)
    r""" The nvme field of the svm.
 """
    routes = fields.List(fields.Nested("NetworkRouteForSvmSchema", unknown=EXCLUDE))
    r""" Optional array of routes for the SVM
 """
    snapshot_policy = fields.Nested("SnapshotPolicySchema", unknown=EXCLUDE)
    r""" The snapshot_policy field of the svm.
 """
    state = fields.Str(validate=enum_validation(['starting', 'running', 'stopping', 'stopped', 'deleting']))
    r""" SVM State

Valid choices:

* starting
* running
* stopping
* stopped
* deleting """
    subtype = fields.Str(validate=enum_validation(['default', 'dp_destination', 'sync_source', 'sync_destination']))
    r""" SVM subtype. The SVM subtype sync_destination is created automatically when an SVM of subtype sync_source is created on the source MetroCluster cluster. A POST request with sync_destination as SVM subtype is invalid.

Valid choices:

* default
* dp_destination
* sync_source
* sync_destination """
    uuid = fields.Str()
    r""" The unique identifier of the SVM.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return Svm

    @property
    def patchable_fields(self):
        return [
            "comment",
            "language",
            "name",
            "state",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "aggregates",
            "cifs",
            "comment",
            "dns",
            "fcp",
            "ip_interfaces",
            "ipspace",
            "iscsi",
            "language",
            "ldap",
            "name",
            "nfs",
            "nis",
            "nsswitch",
            "nvme",
            "routes",
            "snapshot_policy",
            "subtype",
        ]

class Svm(Resource):
    """Allows interaction with Svm objects on the host"""

    _schema = SvmSchema
    _path = "/api/svm/svms"
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

    get_collection.__func__.__doc__ = r"""Retrieves a list of SVMs and individual SVM properties. This includes protocol configurations such as CIFS and NFS, export policies, name service configurations, and network services.
### Important notes
* The SVM object includes a large set of fields and can be expensive to retrieve. Use this API to list the collection of SVMs, and to retrieve only the full details of individual SVMs as needed.
* It is not recommended to create or delete more than five SVMs in parallel.
* REST APIs only expose a data SVM as an SVM.
### Related ONTAP commands
* `vserver show`
### Examples
1. Retrieves a list of SVMs in the cluster sorted by name
    <br/>
    ```
    GET "/api/svm/svms?order_by=name"
    ```
    <br/>
2. Retrieves a list of SVMs in the cluster that have the NFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?nfs.enabled=true"
    ```
    <br/>
3. Retrieves a list of SVMs in the cluster that have the CIFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?cifs.enabled=true"
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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

    patch_collection.__func__.__doc__ = r"""Updates one or more of the following properties of an individual SVM: SVM name, SVM default volume language code, SVM comment, and SVM state.
### Related ONTAP commands
* `vserver modify`
* `vserver rename`
* `vserver start`
* `vserver stop`
### Examples
1.  Stops an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"stopped", "comment":"This SVM is stopped."}'
    ```
    <br/>
2.  Starts an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"running", "comment":"This SVM is running."}'
    ```
    <br/>
3.  Updates the "language" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"language":"en.UTF-8"}'
    ```
    <br/>
4.  Updates the "name" field for an SVM or renames the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"name":"svm_new"}'
    ```
    <br/>
5.  Updates the aggregates for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"aggregates":{"name":["aggr1","aggr2","aggr3"]}}'
    ```
    <br/>
6.  Updates the Snapshot copy policy for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"snapshot_policy":{"name":"custom1"}}'
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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

    delete_collection.__func__.__doc__ = r"""Deletes an SVM. As a prerequisite, SVM objects must be deleted first. SnapMirror relations must be deleted and data volumes must be offline and deleted.
The number of parallel SVMs that can be deleted should not be greater than 5. When the sixth SVM DELETE request is issued, the error message "Maximum allowed SVM jobs exceeded. Wait for the existing SVM jobs to complete and try again." will be returned.
### Related ONTAP commands
* `vserver delete`
### Example
Deletes an individual SVM in the cluster.
  <br/>
  ```
  DELETE "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485"
  ```
  <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
"""
    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    # pylint: disable=missing-docstring
    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ = r"""Retrieves a list of SVMs and individual SVM properties. This includes protocol configurations such as CIFS and NFS, export policies, name service configurations, and network services.
### Important notes
* The SVM object includes a large set of fields and can be expensive to retrieve. Use this API to list the collection of SVMs, and to retrieve only the full details of individual SVMs as needed.
* It is not recommended to create or delete more than five SVMs in parallel.
* REST APIs only expose a data SVM as an SVM.
### Related ONTAP commands
* `vserver show`
### Examples
1. Retrieves a list of SVMs in the cluster sorted by name
    <br/>
    ```
    GET "/api/svm/svms?order_by=name"
    ```
    <br/>
2. Retrieves a list of SVMs in the cluster that have the NFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?nfs.enabled=true"
    ```
    <br/>
3. Retrieves a list of SVMs in the cluster that have the CIFS protocol enabled
    <br/>
    ```
    GET "/api/svm/svms?cifs.enabled=true"
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
"""
    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    # pylint: disable=missing-docstring
    def get(self, **kwargs) -> NetAppResponse:
        return super()._get(**kwargs)

    get.__doc__ = r"""Retrieves the properties for an individual SVM. This includes protocol configurations such as CIFS and NFS, export policies, name service configurations, and network services.
### Important note
* The SVM object includes a large set of fields and can be expensive to retrieve.
* REST APIs only expose a data SVM as an SVM.
### Example
    Retrieves an individual SVM in the cluster
    <br/>
    ```
    GET "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485"
    ```
    <br/>

### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)"""
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

    post.__doc__ = r"""Creates and provisions an SVM. If no IPspace is provided, then the SVM is created on the `Default` IPspace.
The number of parallel SVMs that can be created should not be greater than 5. When the sixth SVM POST request is issued, the error message "Maximum allowed SVM jobs exceeded. Wait for the existing SVM jobs to complete and try again." will be returned.
### Required properties
* `name` - Name of the SVM to be created.
### Recommended optional properties
* `ipspace.name` or `ipspace.uuid` - IPspace of the SVM
  * `ip_interfaces` - If provided, the following fields are required:
  * `ip_interfaces.name` - Name of the interface
  * `ip_interfaces.ip.address` - IP address
  * `ip_interfaces.ip.netmask` - Netmask length or IP address
  * `ip_interfaces.location.broadcast_domain.uuid` or `ip_interfaces.location.broadcast_domain.name` - Broadcast domain name or UUID belonging to the same IPspace of the SVM.
* `routes` - If provided, the following field is required:
  * `routes.gateway` - Gateway IP address
* `cifs` - If provided, interfaces, routes and DNS must be provided. The following fields are also required:
  * `cifs.name` - Name of the CIFS server to be created for the SVM.
  * `cifs.ad_domain.fqdn` - Fully qualified domain name
  * `cifs.ad_domain.user` - Administrator username
  * `cifs.ad_domain.password` - User password
* `ldap` - If provided, the following fields are required:
  * `ldap.servers` or `ldap.ad_domain` - LDAP server list or Active directory domain
  * `ldap.bind_dn` - Bind DN
  * `ldap.base_dn` - Base DN
* `nis` - If provided, the following fields are required:
  * `nis.servers` - NIS servers
  * `nis.domain` - NIS domain
* `dns` - If provided, the following fields are required:
  * `dns.servers` - Name servers
  * `dns.domains` - Domains
### Default property values
If not specified in POST, the following default property values are assigned:
* `language` - _C.UTF-8_
* `ipspace.name` - _Default_
* `snapshot_policy.name` - _Default_
* `subtype` - _Default_ ( _sync-source_ if MetroCluster configuration )
### Related ONTAP commands
* `vserver create`
* `vserver add-aggregates`
* `network interface create`
* `network route create`
* `vserver services name-service dns create`
* `vserver nfs create`
* `vserver services name-service ldap client create`
* `vserver cifs create`
* `vserver services name-service nis-domain create`
* `vserver iscsi create`
* `vserver nvme create`
* `vserver fcp create`
* `vserver services name-service ns-switch create`
### Examples
1. Creates an SVM with default "snapshot_policy"
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}}'
    ```
    <br/>
2. Creates an SVM and configures NFS, ISCSI and FCP
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nfs":{"enabled":"true"}, "fcp":{"enabled":"true"}, "iscsi":{"enabled":"true"}}'
    ```
    <br/>
3. Creates an SVM and configures NVMe
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "nvme":{"enabled":"true"}}'
    ```
    <br/>
4. Creates an SVM and configures LDAP
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "ldap":{"servers":["10.140.101.1","10.140.101.2"], "ad_domain":"abc.com", "base_dn":"dc=netapp,dc=com", "bind_dn":"dc=netapp,dc=com"}}'
    ```
    <br/>
5. Creates an SVM and configures NIS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "nis":{"enabled":"true", "domain":"def.com","servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
6. Creates an SVM and configures DNS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "snapshot_policy":{"name":"default"}, "dns":{"domains":["abc.com","def.com"], "servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
7. Creates an SVM and configures a LIF
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ip_interfaces": [{"name":"lif1", "ip":{"address":"10.10.10.7", "netmask": "255.255.255.0"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}]}'
    ```
    <br/>
8. Creates an SVM and configures a LIF with IPV6 address
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "ip_interfaces": [{"name":"lif2", "ip":{"address":"fd22:8b1e:b255:202:2a0:98ff:fe01:7d5b", "netmask":"24"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}]}'
    ```
    <br/>
9. Creates an SVM and configures CIFS
    <br/>
    ```
    POST "/api/svm/svms" '{"name":"testVs", "cifs":{"name":"CIFDOC", "ad_domain":{"fqdn":"abc.def.com", "organizational_unit":"CN=Computers", "user":"cif_admin", "password":"abc123"}}, "ip_interfaces":[{"name":"lif1", "ip":{"address":"10.10.10.7", "netmask": "255.255.255.0"}, "location":{"broadcast_domain":{"name":"bd1"}, "home_node":{"name":"node1"}}, "service_policy": "default-management"}],"routes": [{"destination": {"address": "0.0.0.0", "netmask": "0"}, "gateway": "10.10.10.7"}], "dns":{"domains":["abc.def.com", "def.com"], "servers":["10.224.223.130", "10.224.223.131"]}}'
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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

    patch.__doc__ = r"""Updates one or more of the following properties of an individual SVM: SVM name, SVM default volume language code, SVM comment, and SVM state.
### Related ONTAP commands
* `vserver modify`
* `vserver rename`
* `vserver start`
* `vserver stop`
### Examples
1.  Stops an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"stopped", "comment":"This SVM is stopped."}'
    ```
    <br/>
2.  Starts an SVM and updates the "comment" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"state":"running", "comment":"This SVM is running."}'
    ```
    <br/>
3.  Updates the "language" field for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"language":"en.UTF-8"}'
    ```
    <br/>
4.  Updates the "name" field for an SVM or renames the SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"name":"svm_new"}'
    ```
    <br/>
5.  Updates the aggregates for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"aggregates":{"name":["aggr1","aggr2","aggr3"]}}'
    ```
    <br/>
6.  Updates the Snapshot copy policy for an individual SVM
    <br/>
    ```
    PATCH "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485" '{"snapshot_policy":{"name":"custom1"}}'
    ```
    <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
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

    delete.__doc__ = r"""Deletes an SVM. As a prerequisite, SVM objects must be deleted first. SnapMirror relations must be deleted and data volumes must be offline and deleted.
The number of parallel SVMs that can be deleted should not be greater than 5. When the sixth SVM DELETE request is issued, the error message "Maximum allowed SVM jobs exceeded. Wait for the existing SVM jobs to complete and try again." will be returned.
### Related ONTAP commands
* `vserver delete`
### Example
Deletes an individual SVM in the cluster.
  <br/>
  ```
  DELETE "/api/svm/svms/f16f0935-5281-11e8-b94d-005056b46485"
  ```
  <br/>
### Learn more
* [`DOC /svm/svms`](#docs-svm-svm_svms)
"""
    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)



