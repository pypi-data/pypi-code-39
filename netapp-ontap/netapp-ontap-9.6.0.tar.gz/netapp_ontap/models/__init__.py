"""
Copyright &copy; 2019 NetApp Inc. All rights reserved.

All of the modules in this package define the supporting objects used to
organize the fields in the corresponding `netapp_ontap.resource.Resource`
types. These models are a subset of `netapp_ontap.resource.Resource` and
do not have any actions that can be performed on them.
"""

# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines

from netapp_ontap.models.volume_tiering import VolumeTiering
from netapp_ontap.models.vsi_on_san_new_igroups import VsiOnSanNewIgroups
from netapp_ontap.models.performance_metric_raw import PerformanceMetricRaw
from netapp_ontap.models.volume_space import VolumeSpace
from netapp_ontap.models.volume_qos import VolumeQos
from netapp_ontap.models.nfs_service_protocol import NfsServiceProtocol
from netapp_ontap.models.volume_guarantee import VolumeGuarantee
from netapp_ontap.models.software_package_download import SoftwarePackageDownload
from netapp_ontap.models.cluster_space_block_storage_medias import ClusterSpaceBlockStorageMedias
from netapp_ontap.models.snapmirror_policy_rule import SnapmirrorPolicyRule
from netapp_ontap.models.application_statistics_iops import ApplicationStatisticsIops
from netapp_ontap.models.fc_port_speed import FcPortSpeed
from netapp_ontap.models.raid_group_disk import RaidGroupDisk
from netapp_ontap.models.vsi_on_nas import VsiOnNas
from netapp_ontap.models.port_vlan import PortVlan
from netapp_ontap.models.security_saml_sp_certificate import SecuritySamlSpCertificate
from netapp_ontap.models.snapmirror_relationship_policy import SnapmirrorRelationshipPolicy
from netapp_ontap.models.vsi_on_nas_datastore_storage_service import VsiOnNasDatastoreStorageService
from netapp_ontap.models.ad_domain import AdDomain
from netapp_ontap.models.oracle_rac_on_nfs_oracle_crs import OracleRacOnNfsOracleCrs
from netapp_ontap.models.application_statistics_latency import ApplicationStatisticsLatency
from netapp_ontap.models.scope_ipspace import ScopeIpspace
from netapp_ontap.models.volume_efficiency import VolumeEfficiency
from netapp_ontap.models.lun_status import LunStatus
from netapp_ontap.models.version import Version
from netapp_ontap.models.node_cluster_interface import NodeClusterInterface
from netapp_ontap.models.svm_nis import SvmNis
from netapp_ontap.models.nvme_interface_fc_interface import NvmeInterfaceFcInterface
from netapp_ontap.models.nvme_subsystem_host_subsystem import NvmeSubsystemHostSubsystem
from netapp_ontap.models.oracle_rac_on_san_new_igroups import OracleRacOnSanNewIgroups
from netapp_ontap.models.maxdata_on_san import MaxdataOnSan
from netapp_ontap.models.nas_storage_service import NasStorageService
from netapp_ontap.models.nvme_namespace_space_guarantee import NvmeNamespaceSpaceGuarantee
from netapp_ontap.models.node_management_interface import NodeManagementInterface
from netapp_ontap.models.vdi_on_nas_hyper_v_access import VdiOnNasHyperVAccess
from netapp_ontap.models.oracle_on_nfs_ora_home import OracleOnNfsOraHome
from netapp_ontap.models.snapmirror_endpoint import SnapmirrorEndpoint
from netapp_ontap.models.application_links import ApplicationLinks
from netapp_ontap.models.lun_lun_maps import LunLunMaps
from netapp_ontap.models.sql_on_san_log import SqlOnSanLog
from netapp_ontap.models.application_nfs_properties_permissions import ApplicationNfsPropertiesPermissions
from netapp_ontap.models.ip_interface_svm_location import IpInterfaceSvmLocation
from netapp_ontap.models.iscsi_connection_interface import IscsiConnectionInterface
from netapp_ontap.models.autosupport_connectivity_issue import AutosupportConnectivityIssue
from netapp_ontap.models.node_setup_ip import NodeSetupIp
from netapp_ontap.models.maxdata_on_san_metadata import MaxdataOnSanMetadata
from netapp_ontap.models.shelf_frus import ShelfFrus
from netapp_ontap.models.cluster_peer_setup_response_authentication import ClusterPeerSetupResponseAuthentication
from netapp_ontap.models.maxdata_on_san_application_components_storage_service import MaxdataOnSanApplicationComponentsStorageService
from netapp_ontap.models.oracle_on_nfs_redo_log_storage_service import OracleOnNfsRedoLogStorageService
from netapp_ontap.models.application_rpo_components import ApplicationRpoComponents
from netapp_ontap.models.iscsi_credentials_chap_inbound import IscsiCredentialsChapInbound
from netapp_ontap.models.nfs_service_protocol_v40_features import NfsServiceProtocolV40Features
from netapp_ontap.models.iscsi_connection_interface_ip import IscsiConnectionInterfaceIp
from netapp_ontap.models.oracle_rac_on_nfs_oracle_crs_storage_service import OracleRacOnNfsOracleCrsStorageService
from netapp_ontap.models.fcp_service_target import FcpServiceTarget
from netapp_ontap.models.job_link import JobLink
from netapp_ontap.models.cluster_peer_encryption import ClusterPeerEncryption
from netapp_ontap.models.quota_report_qtree import QuotaReportQtree
from netapp_ontap.models.nvme_namespace_subsystem_map import NvmeNamespaceSubsystemMap
from netapp_ontap.models.plex_resync import PlexResync
from netapp_ontap.models.lun_space_guarantee import LunSpaceGuarantee
from netapp_ontap.models.svm_nfs import SvmNfs
from netapp_ontap.models.shelf_drawers import ShelfDrawers
from netapp_ontap.models.application_statistics_space1 import ApplicationStatisticsSpace1
from netapp_ontap.models.license_capacity import LicenseCapacity
from netapp_ontap.models.autosupport_message_error import AutosupportMessageError
from netapp_ontap.models.mongo_db_on_san_protection_type import MongoDbOnSanProtectionType
from netapp_ontap.models.application_statistics import ApplicationStatistics
from netapp_ontap.models.fc_login_initiator import FcLoginInitiator
from netapp_ontap.models.lun_map_igroup import LunMapIgroup
from netapp_ontap.models.cloud_storage_tier import CloudStorageTier
from netapp_ontap.models.cluster_peer_links import ClusterPeerLinks
from netapp_ontap.models.quota_report_space_used import QuotaReportSpaceUsed
from netapp_ontap.models.software_status_details_reference_node import SoftwareStatusDetailsReferenceNode
from netapp_ontap.models.nvme_subsystem_controller_interface import NvmeSubsystemControllerInterface
from netapp_ontap.models.software_status_details import SoftwareStatusDetails
from netapp_ontap.models.volume_encryption import VolumeEncryption
from netapp_ontap.models.application_san_access_iscsi_endpoint import ApplicationSanAccessIscsiEndpoint
from netapp_ontap.models.application_template1 import ApplicationTemplate1
from netapp_ontap.models.software_reference_metrocluster import SoftwareReferenceMetrocluster
from netapp_ontap.models.application_component_snapshot_component import ApplicationComponentSnapshotComponent
from netapp_ontap.models.schedule_cluster import ScheduleCluster
from netapp_ontap.models.schedule_cron import ScheduleCron
from netapp_ontap.models.svm_iscsi import SvmIscsi
from netapp_ontap.models.cluster_management_interface import ClusterManagementInterface
from netapp_ontap.models.application_rpo_remote import ApplicationRpoRemote
from netapp_ontap.models.autosupport_connectivity_corrective_action import AutosupportConnectivityCorrectiveAction
from netapp_ontap.models.application_snapshot_components import ApplicationSnapshotComponents
from netapp_ontap.models.oracle_rac_on_san_db_sids import OracleRacOnSanDbSids
from netapp_ontap.models.application_protection_groups import ApplicationProtectionGroups
from netapp_ontap.models.application_cifs_properties_share import ApplicationCifsPropertiesShare
from netapp_ontap.models.application_cifs_properties_permissions import ApplicationCifsPropertiesPermissions
from netapp_ontap.models.license_compliance import LicenseCompliance
from netapp_ontap.models.oracle_rac_on_nfs_grid_binary_storage_service import OracleRacOnNfsGridBinaryStorageService
from netapp_ontap.models.nvme_subsystem_subsystem_maps import NvmeSubsystemSubsystemMaps
from netapp_ontap.models.key_server_readcreate import KeyServerReadcreate
from netapp_ontap.models.security_certificate_sign import SecurityCertificateSign
from netapp_ontap.models.igroup_initiator_igroup import IgroupInitiatorIgroup
from netapp_ontap.models.quota_rule_space import QuotaRuleSpace
from netapp_ontap.models.vdi_on_nas import VdiOnNas
from netapp_ontap.models.volume_nas import VolumeNas
from netapp_ontap.models.volume_snaplock import VolumeSnaplock
from netapp_ontap.models.svm_fcp import SvmFcp
from netapp_ontap.models.quota_report_group import QuotaReportGroup
from netapp_ontap.models.software_update_details_reference_node import SoftwareUpdateDetailsReferenceNode
from netapp_ontap.models.quota_report_files import QuotaReportFiles
from netapp_ontap.models.security_key_manager_onboard import SecurityKeyManagerOnboard
from netapp_ontap.models.security_audit_log_svm import SecurityAuditLogSvm
from netapp_ontap.models.application_lun_mapping_object import ApplicationLunMappingObject
from netapp_ontap.models.broadcast_domain_reference_ipspace import BroadcastDomainReferenceIpspace
from netapp_ontap.models.oracle_on_nfs_db import OracleOnNfsDb
from netapp_ontap.models.nas import Nas
from netapp_ontap.models.application_component_svm import ApplicationComponentSvm
from netapp_ontap.models.vscan_on_access_scope import VscanOnAccessScope
from netapp_ontap.models.application_volume_object import ApplicationVolumeObject
from netapp_ontap.models.fpolicy_event_filters import FpolicyEventFilters
from netapp_ontap.models.snapmirror_transfer_relationship import SnapmirrorTransferRelationship
from netapp_ontap.models.maxdata_on_san_application_components import MaxdataOnSanApplicationComponents
from netapp_ontap.models.volume_space_snapshot import VolumeSpaceSnapshot
from netapp_ontap.models.lun_clone_source import LunCloneSource
from netapp_ontap.models.oracle_on_san_new_igroups import OracleOnSanNewIgroups
from netapp_ontap.models.volume_clone import VolumeClone
from netapp_ontap.models.sql_on_smb import SqlOnSmb
from netapp_ontap.models.aggregate_block_storage_mirror import AggregateBlockStorageMirror
from netapp_ontap.models.audit_schedule import AuditSchedule
from netapp_ontap.models.account_application import AccountApplication
from netapp_ontap.models.peer import Peer
from netapp_ontap.models.mongo_db_on_san_new_igroups import MongoDbOnSanNewIgroups
from netapp_ontap.models.key_server_no_records import KeyServerNoRecords
from netapp_ontap.models.qos_policy_adaptive import QosPolicyAdaptive
from netapp_ontap.models.nvme_namespace_clone import NvmeNamespaceClone
from netapp_ontap.models.aggregate_data_encryption import AggregateDataEncryption
from netapp_ontap.models.application_protection_groups_rpo_local import ApplicationProtectionGroupsRpoLocal
from netapp_ontap.models.snapmirror_error import SnapmirrorError
from netapp_ontap.models.node_controller_flash_cache import NodeControllerFlashCache
from netapp_ontap.models.application_rpo_local import ApplicationRpoLocal
from netapp_ontap.models.performance_metric import PerformanceMetric
from netapp_ontap.models.quota_rule_files import QuotaRuleFiles
from netapp_ontap.models.chassis_frus import ChassisFrus
from netapp_ontap.models.quota_rule_group import QuotaRuleGroup
from netapp_ontap.models.lun_map_lun import LunMapLun
from netapp_ontap.models.lun_map_lun_node import LunMapLunNode
from netapp_ontap.models.lun_movement import LunMovement
from netapp_ontap.models.sql_on_smb_access import SqlOnSmbAccess
from netapp_ontap.models.qos_policy_fixed import QosPolicyFixed
from netapp_ontap.models.snapshot_policy_schedule import SnapshotPolicySchedule
from netapp_ontap.models.svm_nvme import SvmNvme
from netapp_ontap.models.mongo_db_on_san_dataset_storage_service import MongoDbOnSanDatasetStorageService
from netapp_ontap.models.vsi_on_nas_datastore import VsiOnNasDatastore
from netapp_ontap.models.ip_interface_svm import IpInterfaceSvm
from netapp_ontap.models.aggregate_block_storage import AggregateBlockStorage
from netapp_ontap.models.license import License
from netapp_ontap.models.ems_destination_certificate import EmsDestinationCertificate
from netapp_ontap.models.shelf_bays import ShelfBays
from netapp_ontap.models.application_protection_groups_rpo_remote import ApplicationProtectionGroupsRpoRemote
from netapp_ontap.models.application_snapshot_restore import ApplicationSnapshotRestore
from netapp_ontap.models.application_statistics_components import ApplicationStatisticsComponents
from netapp_ontap.models.iscsi_credentials_chap_outbound import IscsiCredentialsChapOutbound
from netapp_ontap.models.ad_domain_svm import AdDomainSvm
from netapp_ontap.models.broadcast_domain_svm import BroadcastDomainSvm
from netapp_ontap.models.application_component_application import ApplicationComponentApplication
from netapp_ontap.models.collection_links import CollectionLinks
from netapp_ontap.models.oracle_rac_on_nfs import OracleRacOnNfs
from netapp_ontap.models.svm_cifs_service import SvmCifsService
from netapp_ontap.models.lun_clone import LunClone
from netapp_ontap.models.iscsi_session_initiator import IscsiSessionInitiator
from netapp_ontap.models.nvme_namespace_clone_source import NvmeNamespaceCloneSource
from netapp_ontap.models.application_lun_object import ApplicationLunObject
from netapp_ontap.models.aggregate_space import AggregateSpace
from netapp_ontap.models.snapshot_policy_copies import SnapshotPolicyCopies
from netapp_ontap.models.nvme_namespace_status import NvmeNamespaceStatus
from netapp_ontap.models.application_component_snapshot_svm import ApplicationComponentSnapshotSvm
from netapp_ontap.models.oracle_on_nfs import OracleOnNfs
from netapp_ontap.models.volume_space_logical_space import VolumeSpaceLogicalSpace
from netapp_ontap.models.application_rpo_rpo_remote import ApplicationRpoRpoRemote
from netapp_ontap.models.nvme_subsystem_controller_host import NvmeSubsystemControllerHost
from netapp_ontap.models.application_statistics_latency1 import ApplicationStatisticsLatency1
from netapp_ontap.models.application_rpo_rpo_local import ApplicationRpoRpoLocal
from netapp_ontap.models.maxdata_on_san_application_components_protection_type import MaxdataOnSanApplicationComponentsProtectionType
from netapp_ontap.models.disk_drawer import DiskDrawer
from netapp_ontap.models.iscsi_connection import IscsiConnection
from netapp_ontap.models.quota_rule_qtree import QuotaRuleQtree
from netapp_ontap.models.iscsi_credentials_initiator_address import IscsiCredentialsInitiatorAddress
from netapp_ontap.models.lun_space import LunSpace
from netapp_ontap.models.snapmirror_transfer_files import SnapmirrorTransferFiles
from netapp_ontap.models.application_rpo_rpo import ApplicationRpoRpo
from netapp_ontap.models.fc_interface_location import FcInterfaceLocation
from netapp_ontap.models.mongo_db_on_san import MongoDbOnSan
from netapp_ontap.models.nvme_namespace_location import NvmeNamespaceLocation
from netapp_ontap.models.software_node import SoftwareNode
from netapp_ontap.models.error_responses import ErrorResponses
from netapp_ontap.models.sql_on_san_new_igroups import SqlOnSanNewIgroups
from netapp_ontap.models.network_route_for_svm import NetworkRouteForSvm
from netapp_ontap.models.ems_event_parameter import EmsEventParameter
from netapp_ontap.models.quota_report_files_used import QuotaReportFilesUsed
from netapp_ontap.models.application_lun_mapping_object_igroup import ApplicationLunMappingObjectIgroup
from netapp_ontap.models.log_retention import LogRetention
from netapp_ontap.models.raid_group_recomputing_parity import RaidGroupRecomputingParity
from netapp_ontap.models.application_san_access_fcp_endpoint import ApplicationSanAccessFcpEndpoint
from netapp_ontap.models.aggregate_cloud_storage import AggregateCloudStorage
from netapp_ontap.models.ems_event_message import EmsEventMessage
from netapp_ontap.models.ip_interface_and_gateway import IpInterfaceAndGateway
from netapp_ontap.models.space_efficiency import SpaceEfficiency
from netapp_ontap.models.self_link import SelfLink
from netapp_ontap.models.ip_info import IpInfo
from netapp_ontap.models.ip_address_range import IpAddressRange
from netapp_ontap.models.igroup_lun import IgroupLun
from netapp_ontap.models.fpolicy_policy_scope import FpolicyPolicyScope
from netapp_ontap.models.application_component_storage_service import ApplicationComponentStorageService
from netapp_ontap.models.iscsi_credentials_chap import IscsiCredentialsChap
from netapp_ontap.models.nvme_subsystem_io_queue import NvmeSubsystemIoQueue
from netapp_ontap.models.node_ha import NodeHa
from netapp_ontap.models.fc_port_transceiver import FcPortTransceiver
from netapp_ontap.models.snapmirror_relationship_transfer import SnapmirrorRelationshipTransfer
from netapp_ontap.models.sql_on_san import SqlOnSan
from netapp_ontap.models.nvme_subsystem_controller_admin_queue import NvmeSubsystemControllerAdminQueue
from netapp_ontap.models.software_validation import SoftwareValidation
from netapp_ontap.models.raid_group import RaidGroup
from netapp_ontap.models.software_message_catalog import SoftwareMessageCatalog
from netapp_ontap.models.ems_filter_rule_message_criteria import EmsFilterRuleMessageCriteria
from netapp_ontap.models.fpolicy_event_file_operations import FpolicyEventFileOperations
from netapp_ontap.models.autosupport_issues import AutosupportIssues
from netapp_ontap.models.san_application_components import SanApplicationComponents
from netapp_ontap.models.software_update_details import SoftwareUpdateDetails
from netapp_ontap.models.application_protection_groups_rpo import ApplicationProtectionGroupsRpo
from netapp_ontap.models.cluster_peer_authentication import ClusterPeerAuthentication
from netapp_ontap.models.security_key_manager_external import SecurityKeyManagerExternal
from netapp_ontap.models.performance_metric_io_type import PerformanceMetricIoType
from netapp_ontap.models.application_component_snapshot_restore_application import ApplicationComponentSnapshotRestoreApplication
from netapp_ontap.models.igroup_initiator_no_records import IgroupInitiatorNoRecords
from netapp_ontap.models.quota_report_users import QuotaReportUsers
from netapp_ontap.models.raid_group_reconstruct import RaidGroupReconstruct
from netapp_ontap.models.application_cifs_properties_backing_storage import ApplicationCifsPropertiesBackingStorage
from netapp_ontap.models.application_snapshot_restore_application import ApplicationSnapshotRestoreApplication
from netapp_ontap.models.nvme_subsystem_namespace import NvmeSubsystemNamespace
from netapp_ontap.models.volume_quota import VolumeQuota
from netapp_ontap.models.vdi_on_san_new_igroups import VdiOnSanNewIgroups
from netapp_ontap.models.application_backing_storage import ApplicationBackingStorage
from netapp_ontap.models.nvme_namespace_space import NvmeNamespaceSpace
from netapp_ontap.models.related_link import RelatedLink
from netapp_ontap.models.lun_movement_paths import LunMovementPaths
from netapp_ontap.models.lun_igroup import LunIgroup
from netapp_ontap.models.volume_snaplock_retention import VolumeSnaplockRetention
from netapp_ontap.models.fc_port_fabric import FcPortFabric
from netapp_ontap.models.nfs_service_transport import NfsServiceTransport
from netapp_ontap.models.kerberos_realm_ad_server import KerberosRealmAdServer
from netapp_ontap.models.software_upload import SoftwareUpload
from netapp_ontap.models.aggregate_block_storage_primary import AggregateBlockStoragePrimary
from netapp_ontap.models.flexcache_relationship import FlexcacheRelationship
from netapp_ontap.models.lun_qos_policy import LunQosPolicy
from netapp_ontap.models.nvme_subsystem_map_namespace import NvmeSubsystemMapNamespace
from netapp_ontap.models.vsi_on_san import VsiOnSan
from netapp_ontap.models.application_cifs_properties import ApplicationCifsProperties
from netapp_ontap.models.layout_requirement import LayoutRequirement
from netapp_ontap.models.aggregate_block_storage_hybrid_cache import AggregateBlockStorageHybridCache
from netapp_ontap.models.rotation import Rotation
from netapp_ontap.models.sql_on_san_db_storage_service import SqlOnSanDbStorageService
from netapp_ontap.models.volume_autosize import VolumeAutosize
from netapp_ontap.models.application_nfs_properties_export_policy import ApplicationNfsPropertiesExportPolicy
from netapp_ontap.models.nas_application_components import NasApplicationComponents
from netapp_ontap.models.dr_node import DrNode
from netapp_ontap.models.cifs_service_delete import CifsServiceDelete
from netapp_ontap.models.shelf_remote import ShelfRemote
from netapp_ontap.models.application_statistics_snapshot import ApplicationStatisticsSnapshot
from netapp_ontap.models.cluster_peer_status import ClusterPeerStatus
from netapp_ontap.models.volume_error_state import VolumeErrorState
from netapp_ontap.models.ip_interface_reference_ip import IpInterfaceReferenceIp
from netapp_ontap.models.iscsi_service_target import IscsiServiceTarget
from netapp_ontap.models.cluster_peer_local_network_interfaces import ClusterPeerLocalNetworkInterfaces
from netapp_ontap.models.aggregate_space_block_storage import AggregateSpaceBlockStorage
from netapp_ontap.models.cifs_netbios import CifsNetbios
from netapp_ontap.models.iscsi_connection_initiator_address import IscsiConnectionInitiatorAddress
from netapp_ontap.models.lun_location import LunLocation
from netapp_ontap.models.href import Href
from netapp_ontap.models.quota_report_space import QuotaReportSpace
from netapp_ontap.models.svm_dns import SvmDns
from netapp_ontap.models.software_errors import SoftwareErrors
from netapp_ontap.models.application_nfs_properties import ApplicationNfsProperties
from netapp_ontap.models.license_keys import LicenseKeys
from netapp_ontap.models.cluster_peer_remote import ClusterPeerRemote
from netapp_ontap.models.application_rpo import ApplicationRpo
from netapp_ontap.models.maxdata_on_san_application_components_metadata import MaxdataOnSanApplicationComponentsMetadata
from netapp_ontap.models.lun_movement_progress import LunMovementProgress
from netapp_ontap.models.cluster_space_block_storage import ClusterSpaceBlockStorage
from netapp_ontap.models.application_component_snapshot_restore import ApplicationComponentSnapshotRestore
from netapp_ontap.models.ip_interface_svm_ip import IpInterfaceSvmIp
from netapp_ontap.models.aggregate_spare import AggregateSpare
from netapp_ontap.models.fc_port_reference_node import FcPortReferenceNode
from netapp_ontap.models.node_controller_frus import NodeControllerFrus
from netapp_ontap.models.kerberos_realm_kdc import KerberosRealmKdc
from netapp_ontap.models.log import Log
from netapp_ontap.models.oracle_rac_on_nfs_grid_binary import OracleRacOnNfsGridBinary
from netapp_ontap.models.application_statistics_iops1 import ApplicationStatisticsIops1
from netapp_ontap.models.port_reference_node import PortReferenceNode
from netapp_ontap.models.mongo_db_on_san_secondary_igroups import MongoDbOnSanSecondaryIgroups
from netapp_ontap.models.application_san_access import ApplicationSanAccess
from netapp_ontap.models.cluster_peer_local_network import ClusterPeerLocalNetwork
from netapp_ontap.models.application_svm import ApplicationSvm
from netapp_ontap.models.vdi_on_nas_desktops import VdiOnNasDesktops
from netapp_ontap.models.cluster_peer_setup import ClusterPeerSetup
from netapp_ontap.models.vdi_on_nas_desktops_storage_service import VdiOnNasDesktopsStorageService
from netapp_ontap.models.volume_movement import VolumeMovement
from netapp_ontap.models.svm_nsswitch import SvmNsswitch
from netapp_ontap.models.node_controller import NodeController
from netapp_ontap.models.nvme_subsystem_host_io_queue import NvmeSubsystemHostIoQueue
from netapp_ontap.models.cifs_target import CifsTarget
from netapp_ontap.models.volume_encryption_status import VolumeEncryptionStatus
from netapp_ontap.models.nvme_subsystem_controller_io_queue import NvmeSubsystemControllerIoQueue
from netapp_ontap.models.shelf_ports import ShelfPorts
from netapp_ontap.models.storage_port_error import StoragePortError
from netapp_ontap.models.application_statistics_storage_service import ApplicationStatisticsStorageService
from netapp_ontap.models.maxdata_on_san_new_igroups import MaxdataOnSanNewIgroups
from netapp_ontap.models.mongo_db_on_san_dataset import MongoDbOnSanDataset
from netapp_ontap.models.software_mcc import SoftwareMcc
from netapp_ontap.models.application_statistics_space import ApplicationStatisticsSpace
from netapp_ontap.models.oracle_on_san import OracleOnSan
from netapp_ontap.models.error_arguments import ErrorArguments
from netapp_ontap.models.oracle_on_nfs_archive_log import OracleOnNfsArchiveLog
from netapp_ontap.models.app_cifs_access import AppCifsAccess
from netapp_ontap.models.application_cifs_properties_server import ApplicationCifsPropertiesServer
from netapp_ontap.models.cluster_space_cloud_storage import ClusterSpaceCloudStorage
from netapp_ontap.models.ip_interface_location import IpInterfaceLocation
from netapp_ontap.models.port_lag import PortLag
from netapp_ontap.models.oracle_on_nfs_ora_home_storage_service import OracleOnNfsOraHomeStorageService
from netapp_ontap.models.vdi_on_san import VdiOnSan
from netapp_ontap.models.app_nfs_access import AppNfsAccess
from netapp_ontap.models.oracle_on_nfs_archive_log_storage_service import OracleOnNfsArchiveLogStorageService
from netapp_ontap.models.oracle_on_nfs_redo_log import OracleOnNfsRedoLog
from netapp_ontap.models.application_component_snapshot_restore_component import ApplicationComponentSnapshotRestoreComponent
from netapp_ontap.models.sql_on_san_db import SqlOnSanDb
from netapp_ontap.models.sql_on_san_log_storage_service import SqlOnSanLogStorageService
from netapp_ontap.models.error import Error
from netapp_ontap.models.volume_application import VolumeApplication
from netapp_ontap.models.nvme_subsystem_io_queue_default import NvmeSubsystemIoQueueDefault
from netapp_ontap.models.application_component_snapshot_application import ApplicationComponentSnapshotApplication
from netapp_ontap.models.layout_requirement_raid_group import LayoutRequirementRaidGroup
from netapp_ontap.models.vscan_on_demand_scope import VscanOnDemandScope
from netapp_ontap.models.sql_on_san_temp_db import SqlOnSanTempDb
from netapp_ontap.models.san import San
from netapp_ontap.models.shelf_cable import ShelfCable
from netapp_ontap.models.nvme_subsystem_host_no_records import NvmeSubsystemHostNoRecords
from netapp_ontap.models.san_new_igroups import SanNewIgroups
from netapp_ontap.models.nfs_service_protocol_v41_features import NfsServiceProtocolV41Features
from netapp_ontap.models.oracle_rac_on_san import OracleRacOnSan
from netapp_ontap.models.sql_on_san_temp_db_storage_service import SqlOnSanTempDbStorageService
from netapp_ontap.models.svm_ldap import SvmLdap
from netapp_ontap.models.aggregate_space_cloud_storage import AggregateSpaceCloudStorage
from netapp_ontap.models.audit_events import AuditEvents
from netapp_ontap.models.cifs_service_security import CifsServiceSecurity
from netapp_ontap.models.performance import Performance
from netapp_ontap.models.igroup_lun_maps import IgroupLunMaps
from netapp_ontap.models.volume_files import VolumeFiles
from netapp_ontap.models.service_processor import ServiceProcessor

__all__ = [
    "VolumeTiering",
    "VsiOnSanNewIgroups",
    "PerformanceMetricRaw",
    "VolumeSpace",
    "VolumeQos",
    "NfsServiceProtocol",
    "VolumeGuarantee",
    "SoftwarePackageDownload",
    "ClusterSpaceBlockStorageMedias",
    "SnapmirrorPolicyRule",
    "ApplicationStatisticsIops",
    "FcPortSpeed",
    "RaidGroupDisk",
    "VsiOnNas",
    "PortVlan",
    "SecuritySamlSpCertificate",
    "SnapmirrorRelationshipPolicy",
    "VsiOnNasDatastoreStorageService",
    "AdDomain",
    "OracleRacOnNfsOracleCrs",
    "ApplicationStatisticsLatency",
    "ScopeIpspace",
    "VolumeEfficiency",
    "LunStatus",
    "Version",
    "NodeClusterInterface",
    "SvmNis",
    "NvmeInterfaceFcInterface",
    "NvmeSubsystemHostSubsystem",
    "OracleRacOnSanNewIgroups",
    "MaxdataOnSan",
    "NasStorageService",
    "NvmeNamespaceSpaceGuarantee",
    "NodeManagementInterface",
    "VdiOnNasHyperVAccess",
    "OracleOnNfsOraHome",
    "SnapmirrorEndpoint",
    "ApplicationLinks",
    "LunLunMaps",
    "SqlOnSanLog",
    "ApplicationNfsPropertiesPermissions",
    "IpInterfaceSvmLocation",
    "IscsiConnectionInterface",
    "AutosupportConnectivityIssue",
    "NodeSetupIp",
    "MaxdataOnSanMetadata",
    "ShelfFrus",
    "ClusterPeerSetupResponseAuthentication",
    "MaxdataOnSanApplicationComponentsStorageService",
    "OracleOnNfsRedoLogStorageService",
    "ApplicationRpoComponents",
    "IscsiCredentialsChapInbound",
    "NfsServiceProtocolV40Features",
    "IscsiConnectionInterfaceIp",
    "OracleRacOnNfsOracleCrsStorageService",
    "FcpServiceTarget",
    "JobLink",
    "ClusterPeerEncryption",
    "QuotaReportQtree",
    "NvmeNamespaceSubsystemMap",
    "PlexResync",
    "LunSpaceGuarantee",
    "SvmNfs",
    "ShelfDrawers",
    "ApplicationStatisticsSpace1",
    "LicenseCapacity",
    "AutosupportMessageError",
    "MongoDbOnSanProtectionType",
    "ApplicationStatistics",
    "FcLoginInitiator",
    "LunMapIgroup",
    "CloudStorageTier",
    "ClusterPeerLinks",
    "QuotaReportSpaceUsed",
    "SoftwareStatusDetailsReferenceNode",
    "NvmeSubsystemControllerInterface",
    "SoftwareStatusDetails",
    "VolumeEncryption",
    "ApplicationSanAccessIscsiEndpoint",
    "ApplicationTemplate1",
    "SoftwareReferenceMetrocluster",
    "ApplicationComponentSnapshotComponent",
    "ScheduleCluster",
    "ScheduleCron",
    "SvmIscsi",
    "ClusterManagementInterface",
    "ApplicationRpoRemote",
    "AutosupportConnectivityCorrectiveAction",
    "ApplicationSnapshotComponents",
    "OracleRacOnSanDbSids",
    "ApplicationProtectionGroups",
    "ApplicationCifsPropertiesShare",
    "ApplicationCifsPropertiesPermissions",
    "LicenseCompliance",
    "OracleRacOnNfsGridBinaryStorageService",
    "NvmeSubsystemSubsystemMaps",
    "KeyServerReadcreate",
    "SecurityCertificateSign",
    "IgroupInitiatorIgroup",
    "QuotaRuleSpace",
    "VdiOnNas",
    "VolumeNas",
    "VolumeSnaplock",
    "SvmFcp",
    "QuotaReportGroup",
    "SoftwareUpdateDetailsReferenceNode",
    "QuotaReportFiles",
    "SecurityKeyManagerOnboard",
    "SecurityAuditLogSvm",
    "ApplicationLunMappingObject",
    "BroadcastDomainReferenceIpspace",
    "OracleOnNfsDb",
    "Nas",
    "ApplicationComponentSvm",
    "VscanOnAccessScope",
    "ApplicationVolumeObject",
    "FpolicyEventFilters",
    "SnapmirrorTransferRelationship",
    "MaxdataOnSanApplicationComponents",
    "VolumeSpaceSnapshot",
    "LunCloneSource",
    "OracleOnSanNewIgroups",
    "VolumeClone",
    "SqlOnSmb",
    "AggregateBlockStorageMirror",
    "AuditSchedule",
    "AccountApplication",
    "Peer",
    "MongoDbOnSanNewIgroups",
    "KeyServerNoRecords",
    "QosPolicyAdaptive",
    "NvmeNamespaceClone",
    "AggregateDataEncryption",
    "ApplicationProtectionGroupsRpoLocal",
    "SnapmirrorError",
    "NodeControllerFlashCache",
    "ApplicationRpoLocal",
    "PerformanceMetric",
    "QuotaRuleFiles",
    "ChassisFrus",
    "QuotaRuleGroup",
    "LunMapLun",
    "LunMapLunNode",
    "LunMovement",
    "SqlOnSmbAccess",
    "QosPolicyFixed",
    "SnapshotPolicySchedule",
    "SvmNvme",
    "MongoDbOnSanDatasetStorageService",
    "VsiOnNasDatastore",
    "IpInterfaceSvm",
    "AggregateBlockStorage",
    "License",
    "EmsDestinationCertificate",
    "ShelfBays",
    "ApplicationProtectionGroupsRpoRemote",
    "ApplicationSnapshotRestore",
    "ApplicationStatisticsComponents",
    "IscsiCredentialsChapOutbound",
    "AdDomainSvm",
    "BroadcastDomainSvm",
    "ApplicationComponentApplication",
    "CollectionLinks",
    "OracleRacOnNfs",
    "SvmCifsService",
    "LunClone",
    "IscsiSessionInitiator",
    "NvmeNamespaceCloneSource",
    "ApplicationLunObject",
    "AggregateSpace",
    "SnapshotPolicyCopies",
    "NvmeNamespaceStatus",
    "ApplicationComponentSnapshotSvm",
    "OracleOnNfs",
    "VolumeSpaceLogicalSpace",
    "ApplicationRpoRpoRemote",
    "NvmeSubsystemControllerHost",
    "ApplicationStatisticsLatency1",
    "ApplicationRpoRpoLocal",
    "MaxdataOnSanApplicationComponentsProtectionType",
    "DiskDrawer",
    "IscsiConnection",
    "QuotaRuleQtree",
    "IscsiCredentialsInitiatorAddress",
    "LunSpace",
    "SnapmirrorTransferFiles",
    "ApplicationRpoRpo",
    "FcInterfaceLocation",
    "MongoDbOnSan",
    "NvmeNamespaceLocation",
    "SoftwareNode",
    "ErrorResponses",
    "SqlOnSanNewIgroups",
    "NetworkRouteForSvm",
    "EmsEventParameter",
    "QuotaReportFilesUsed",
    "ApplicationLunMappingObjectIgroup",
    "LogRetention",
    "RaidGroupRecomputingParity",
    "ApplicationSanAccessFcpEndpoint",
    "AggregateCloudStorage",
    "EmsEventMessage",
    "IpInterfaceAndGateway",
    "SpaceEfficiency",
    "SelfLink",
    "IpInfo",
    "IpAddressRange",
    "IgroupLun",
    "FpolicyPolicyScope",
    "ApplicationComponentStorageService",
    "IscsiCredentialsChap",
    "NvmeSubsystemIoQueue",
    "NodeHa",
    "FcPortTransceiver",
    "SnapmirrorRelationshipTransfer",
    "SqlOnSan",
    "NvmeSubsystemControllerAdminQueue",
    "SoftwareValidation",
    "RaidGroup",
    "SoftwareMessageCatalog",
    "EmsFilterRuleMessageCriteria",
    "FpolicyEventFileOperations",
    "AutosupportIssues",
    "SanApplicationComponents",
    "SoftwareUpdateDetails",
    "ApplicationProtectionGroupsRpo",
    "ClusterPeerAuthentication",
    "SecurityKeyManagerExternal",
    "PerformanceMetricIoType",
    "ApplicationComponentSnapshotRestoreApplication",
    "IgroupInitiatorNoRecords",
    "QuotaReportUsers",
    "RaidGroupReconstruct",
    "ApplicationCifsPropertiesBackingStorage",
    "ApplicationSnapshotRestoreApplication",
    "NvmeSubsystemNamespace",
    "VolumeQuota",
    "VdiOnSanNewIgroups",
    "ApplicationBackingStorage",
    "NvmeNamespaceSpace",
    "RelatedLink",
    "LunMovementPaths",
    "LunIgroup",
    "VolumeSnaplockRetention",
    "FcPortFabric",
    "NfsServiceTransport",
    "KerberosRealmAdServer",
    "SoftwareUpload",
    "AggregateBlockStoragePrimary",
    "FlexcacheRelationship",
    "LunQosPolicy",
    "NvmeSubsystemMapNamespace",
    "VsiOnSan",
    "ApplicationCifsProperties",
    "LayoutRequirement",
    "AggregateBlockStorageHybridCache",
    "Rotation",
    "SqlOnSanDbStorageService",
    "VolumeAutosize",
    "ApplicationNfsPropertiesExportPolicy",
    "NasApplicationComponents",
    "DrNode",
    "CifsServiceDelete",
    "ShelfRemote",
    "ApplicationStatisticsSnapshot",
    "ClusterPeerStatus",
    "VolumeErrorState",
    "IpInterfaceReferenceIp",
    "IscsiServiceTarget",
    "ClusterPeerLocalNetworkInterfaces",
    "AggregateSpaceBlockStorage",
    "CifsNetbios",
    "IscsiConnectionInitiatorAddress",
    "LunLocation",
    "Href",
    "QuotaReportSpace",
    "SvmDns",
    "SoftwareErrors",
    "ApplicationNfsProperties",
    "LicenseKeys",
    "ClusterPeerRemote",
    "ApplicationRpo",
    "MaxdataOnSanApplicationComponentsMetadata",
    "LunMovementProgress",
    "ClusterSpaceBlockStorage",
    "ApplicationComponentSnapshotRestore",
    "IpInterfaceSvmIp",
    "AggregateSpare",
    "FcPortReferenceNode",
    "NodeControllerFrus",
    "KerberosRealmKdc",
    "Log",
    "OracleRacOnNfsGridBinary",
    "ApplicationStatisticsIops1",
    "PortReferenceNode",
    "MongoDbOnSanSecondaryIgroups",
    "ApplicationSanAccess",
    "ClusterPeerLocalNetwork",
    "ApplicationSvm",
    "VdiOnNasDesktops",
    "ClusterPeerSetup",
    "VdiOnNasDesktopsStorageService",
    "VolumeMovement",
    "SvmNsswitch",
    "NodeController",
    "NvmeSubsystemHostIoQueue",
    "CifsTarget",
    "VolumeEncryptionStatus",
    "NvmeSubsystemControllerIoQueue",
    "ShelfPorts",
    "StoragePortError",
    "ApplicationStatisticsStorageService",
    "MaxdataOnSanNewIgroups",
    "MongoDbOnSanDataset",
    "SoftwareMcc",
    "ApplicationStatisticsSpace",
    "OracleOnSan",
    "ErrorArguments",
    "OracleOnNfsArchiveLog",
    "AppCifsAccess",
    "ApplicationCifsPropertiesServer",
    "ClusterSpaceCloudStorage",
    "IpInterfaceLocation",
    "PortLag",
    "OracleOnNfsOraHomeStorageService",
    "VdiOnSan",
    "AppNfsAccess",
    "OracleOnNfsArchiveLogStorageService",
    "OracleOnNfsRedoLog",
    "ApplicationComponentSnapshotRestoreComponent",
    "SqlOnSanDb",
    "SqlOnSanLogStorageService",
    "Error",
    "VolumeApplication",
    "NvmeSubsystemIoQueueDefault",
    "ApplicationComponentSnapshotApplication",
    "LayoutRequirementRaidGroup",
    "VscanOnDemandScope",
    "SqlOnSanTempDb",
    "San",
    "ShelfCable",
    "NvmeSubsystemHostNoRecords",
    "SanNewIgroups",
    "NfsServiceProtocolV41Features",
    "OracleRacOnSan",
    "SqlOnSanTempDbStorageService",
    "SvmLdap",
    "AggregateSpaceCloudStorage",
    "AuditEvents",
    "CifsServiceSecurity",
    "Performance",
    "IgroupLunMaps",
    "VolumeFiles",
    "ServiceProcessor",
]
