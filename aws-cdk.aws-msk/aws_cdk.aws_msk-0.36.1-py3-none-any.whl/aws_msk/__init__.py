import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-msk", "0.36.1", __name__, "aws-msk@0.36.1.jsii.tgz")
class CfnCluster(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-msk.CfnCluster"):
    """A CloudFormation ``AWS::MSK::Cluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html
    Stability:
        stable
    cloudformationResource:
        AWS::MSK::Cluster
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, broker_node_group_info: typing.Union["BrokerNodeGroupInfoProperty", aws_cdk.core.IResolvable], cluster_name: str, kafka_version: str, number_of_broker_nodes: jsii.Number, client_authentication: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ClientAuthenticationProperty"]]]=None, configuration_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConfigurationInfoProperty"]]]=None, encryption_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EncryptionInfoProperty"]]]=None, enhanced_monitoring: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::MSK::Cluster``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            broker_node_group_info: ``AWS::MSK::Cluster.BrokerNodeGroupInfo``.
            cluster_name: ``AWS::MSK::Cluster.ClusterName``.
            kafka_version: ``AWS::MSK::Cluster.KafkaVersion``.
            number_of_broker_nodes: ``AWS::MSK::Cluster.NumberOfBrokerNodes``.
            client_authentication: ``AWS::MSK::Cluster.ClientAuthentication``.
            configuration_info: ``AWS::MSK::Cluster.ConfigurationInfo``.
            encryption_info: ``AWS::MSK::Cluster.EncryptionInfo``.
            enhanced_monitoring: ``AWS::MSK::Cluster.EnhancedMonitoring``.
            tags: ``AWS::MSK::Cluster.Tags``.

        Stability:
            experimental
        """
        props: CfnClusterProps = {"brokerNodeGroupInfo": broker_node_group_info, "clusterName": cluster_name, "kafkaVersion": kafka_version, "numberOfBrokerNodes": number_of_broker_nodes}

        if client_authentication is not None:
            props["clientAuthentication"] = client_authentication

        if configuration_info is not None:
            props["configurationInfo"] = configuration_info

        if encryption_info is not None:
            props["encryptionInfo"] = encryption_info

        if enhanced_monitoring is not None:
            props["enhancedMonitoring"] = enhanced_monitoring

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            props: -

        Stability:
            stable
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class.

        Stability:
            stable
        """
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        """
        Stability:
            stable
        """
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::MSK::Cluster.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-tags
        Stability:
            stable
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="brokerNodeGroupInfo")
    def broker_node_group_info(self) -> typing.Union["BrokerNodeGroupInfoProperty", aws_cdk.core.IResolvable]:
        """``AWS::MSK::Cluster.BrokerNodeGroupInfo``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-brokernodegroupinfo
        Stability:
            stable
        """
        return jsii.get(self, "brokerNodeGroupInfo")

    @broker_node_group_info.setter
    def broker_node_group_info(self, value: typing.Union["BrokerNodeGroupInfoProperty", aws_cdk.core.IResolvable]):
        return jsii.set(self, "brokerNodeGroupInfo", value)

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """``AWS::MSK::Cluster.ClusterName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-clustername
        Stability:
            stable
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: str):
        return jsii.set(self, "clusterName", value)

    @property
    @jsii.member(jsii_name="kafkaVersion")
    def kafka_version(self) -> str:
        """``AWS::MSK::Cluster.KafkaVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-kafkaversion
        Stability:
            stable
        """
        return jsii.get(self, "kafkaVersion")

    @kafka_version.setter
    def kafka_version(self, value: str):
        return jsii.set(self, "kafkaVersion", value)

    @property
    @jsii.member(jsii_name="numberOfBrokerNodes")
    def number_of_broker_nodes(self) -> jsii.Number:
        """``AWS::MSK::Cluster.NumberOfBrokerNodes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-numberofbrokernodes
        Stability:
            stable
        """
        return jsii.get(self, "numberOfBrokerNodes")

    @number_of_broker_nodes.setter
    def number_of_broker_nodes(self, value: jsii.Number):
        return jsii.set(self, "numberOfBrokerNodes", value)

    @property
    @jsii.member(jsii_name="clientAuthentication")
    def client_authentication(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ClientAuthenticationProperty"]]]:
        """``AWS::MSK::Cluster.ClientAuthentication``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-clientauthentication
        Stability:
            stable
        """
        return jsii.get(self, "clientAuthentication")

    @client_authentication.setter
    def client_authentication(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ClientAuthenticationProperty"]]]):
        return jsii.set(self, "clientAuthentication", value)

    @property
    @jsii.member(jsii_name="configurationInfo")
    def configuration_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConfigurationInfoProperty"]]]:
        """``AWS::MSK::Cluster.ConfigurationInfo``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-configurationinfo
        Stability:
            stable
        """
        return jsii.get(self, "configurationInfo")

    @configuration_info.setter
    def configuration_info(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConfigurationInfoProperty"]]]):
        return jsii.set(self, "configurationInfo", value)

    @property
    @jsii.member(jsii_name="encryptionInfo")
    def encryption_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EncryptionInfoProperty"]]]:
        """``AWS::MSK::Cluster.EncryptionInfo``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-encryptioninfo
        Stability:
            stable
        """
        return jsii.get(self, "encryptionInfo")

    @encryption_info.setter
    def encryption_info(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EncryptionInfoProperty"]]]):
        return jsii.set(self, "encryptionInfo", value)

    @property
    @jsii.member(jsii_name="enhancedMonitoring")
    def enhanced_monitoring(self) -> typing.Optional[str]:
        """``AWS::MSK::Cluster.EnhancedMonitoring``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-enhancedmonitoring
        Stability:
            stable
        """
        return jsii.get(self, "enhancedMonitoring")

    @enhanced_monitoring.setter
    def enhanced_monitoring(self, value: typing.Optional[str]):
        return jsii.set(self, "enhancedMonitoring", value)

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _BrokerNodeGroupInfoProperty(jsii.compat.TypedDict, total=False):
        brokerAzDistribution: str
        """``CfnCluster.BrokerNodeGroupInfoProperty.BrokerAZDistribution``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-brokerazdistribution
        Stability:
            stable
        """
        securityGroups: typing.List[str]
        """``CfnCluster.BrokerNodeGroupInfoProperty.SecurityGroups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-securitygroups
        Stability:
            stable
        """
        storageInfo: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.StorageInfoProperty"]
        """``CfnCluster.BrokerNodeGroupInfoProperty.StorageInfo``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-storageinfo
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.BrokerNodeGroupInfoProperty", jsii_struct_bases=[_BrokerNodeGroupInfoProperty])
    class BrokerNodeGroupInfoProperty(_BrokerNodeGroupInfoProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html
        Stability:
            stable
        """
        clientSubnets: typing.List[str]
        """``CfnCluster.BrokerNodeGroupInfoProperty.ClientSubnets``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-clientsubnets
        Stability:
            stable
        """

        instanceType: str
        """``CfnCluster.BrokerNodeGroupInfoProperty.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-instancetype
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.ClientAuthenticationProperty", jsii_struct_bases=[])
    class ClientAuthenticationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-clientauthentication.html
        Stability:
            stable
        """
        tls: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.TlsProperty"]
        """``CfnCluster.ClientAuthenticationProperty.Tls``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-clientauthentication.html#cfn-msk-cluster-clientauthentication-tls
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.ConfigurationInfoProperty", jsii_struct_bases=[])
    class ConfigurationInfoProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-configurationinfo.html
        Stability:
            stable
        """
        arn: str
        """``CfnCluster.ConfigurationInfoProperty.Arn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-configurationinfo.html#cfn-msk-cluster-configurationinfo-arn
        Stability:
            stable
        """

        revision: jsii.Number
        """``CfnCluster.ConfigurationInfoProperty.Revision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-configurationinfo.html#cfn-msk-cluster-configurationinfo-revision
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.EBSStorageInfoProperty", jsii_struct_bases=[])
    class EBSStorageInfoProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-ebsstorageinfo.html
        Stability:
            stable
        """
        volumeSize: jsii.Number
        """``CfnCluster.EBSStorageInfoProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-ebsstorageinfo.html#cfn-msk-cluster-ebsstorageinfo-volumesize
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.EncryptionAtRestProperty", jsii_struct_bases=[])
    class EncryptionAtRestProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionatrest.html
        Stability:
            stable
        """
        dataVolumeKmsKeyId: str
        """``CfnCluster.EncryptionAtRestProperty.DataVolumeKMSKeyId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionatrest.html#cfn-msk-cluster-encryptionatrest-datavolumekmskeyid
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.EncryptionInTransitProperty", jsii_struct_bases=[])
    class EncryptionInTransitProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionintransit.html
        Stability:
            stable
        """
        clientBroker: str
        """``CfnCluster.EncryptionInTransitProperty.ClientBroker``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionintransit.html#cfn-msk-cluster-encryptionintransit-clientbroker
        Stability:
            stable
        """

        inCluster: typing.Union[bool, aws_cdk.core.IResolvable]
        """``CfnCluster.EncryptionInTransitProperty.InCluster``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionintransit.html#cfn-msk-cluster-encryptionintransit-incluster
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.EncryptionInfoProperty", jsii_struct_bases=[])
    class EncryptionInfoProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptioninfo.html
        Stability:
            stable
        """
        encryptionAtRest: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.EncryptionAtRestProperty"]
        """``CfnCluster.EncryptionInfoProperty.EncryptionAtRest``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptioninfo.html#cfn-msk-cluster-encryptioninfo-encryptionatrest
        Stability:
            stable
        """

        encryptionInTransit: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.EncryptionInTransitProperty"]
        """``CfnCluster.EncryptionInfoProperty.EncryptionInTransit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptioninfo.html#cfn-msk-cluster-encryptioninfo-encryptionintransit
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.StorageInfoProperty", jsii_struct_bases=[])
    class StorageInfoProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-storageinfo.html
        Stability:
            stable
        """
        ebsStorageInfo: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.EBSStorageInfoProperty"]
        """``CfnCluster.StorageInfoProperty.EBSStorageInfo``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-storageinfo.html#cfn-msk-cluster-storageinfo-ebsstorageinfo
        Stability:
            stable
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnCluster.TlsProperty", jsii_struct_bases=[])
    class TlsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-tls.html
        Stability:
            stable
        """
        certificateAuthorityArnList: typing.List[str]
        """``CfnCluster.TlsProperty.CertificateAuthorityArnList``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-tls.html#cfn-msk-cluster-tls-certificateauthorityarnlist
        Stability:
            stable
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnClusterProps(jsii.compat.TypedDict, total=False):
    clientAuthentication: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.ClientAuthenticationProperty"]
    """``AWS::MSK::Cluster.ClientAuthentication``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-clientauthentication
    Stability:
        stable
    """
    configurationInfo: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.ConfigurationInfoProperty"]
    """``AWS::MSK::Cluster.ConfigurationInfo``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-configurationinfo
    Stability:
        stable
    """
    encryptionInfo: typing.Union[aws_cdk.core.IResolvable, "CfnCluster.EncryptionInfoProperty"]
    """``AWS::MSK::Cluster.EncryptionInfo``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-encryptioninfo
    Stability:
        stable
    """
    enhancedMonitoring: str
    """``AWS::MSK::Cluster.EnhancedMonitoring``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-enhancedmonitoring
    Stability:
        stable
    """
    tags: typing.Any
    """``AWS::MSK::Cluster.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-tags
    Stability:
        stable
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-msk.CfnClusterProps", jsii_struct_bases=[_CfnClusterProps])
class CfnClusterProps(_CfnClusterProps):
    """Properties for defining a ``AWS::MSK::Cluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html
    Stability:
        stable
    """
    brokerNodeGroupInfo: typing.Union["CfnCluster.BrokerNodeGroupInfoProperty", aws_cdk.core.IResolvable]
    """``AWS::MSK::Cluster.BrokerNodeGroupInfo``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-brokernodegroupinfo
    Stability:
        stable
    """

    clusterName: str
    """``AWS::MSK::Cluster.ClusterName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-clustername
    Stability:
        stable
    """

    kafkaVersion: str
    """``AWS::MSK::Cluster.KafkaVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-kafkaversion
    Stability:
        stable
    """

    numberOfBrokerNodes: jsii.Number
    """``AWS::MSK::Cluster.NumberOfBrokerNodes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-numberofbrokernodes
    Stability:
        stable
    """

__all__ = ["CfnCluster", "CfnClusterProps", "__jsii_assembly__"]

publication.publish()
